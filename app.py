import streamlit as st
from datetime import datetime

from api.flight_search import get_flight_info
from api.web_search import duckduckgo_search
from memory.memory_manager import get_past_context, save_to_memory
from memory.training_manager import TrainingManager
from memory.chat_manager import (
    create_new_chat_session,
    get_all_chat_sessions,
    get_session_messages,
    add_message_to_session,
    delete_chat_session
)
from db.setup import init_db
from llm.setup_llm import get_llm_response

# Initialize database and training manager
init_db()
training_manager = TrainingManager()

# Initialize session state
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None

# UI Setup
st.set_page_config(page_title="🛫 Flight Info Assistant", layout="wide")

# Sidebar for chat sessions
with st.sidebar:
    st.title("Chat Sessions")
    
    # New chat button
    if st.button("New Chat"):
        new_session_id = create_new_chat_session()
        st.session_state.current_session_id = new_session_id
        st.rerun()
    
    # List of chat sessions
    sessions = get_all_chat_sessions()
    for session in sessions:
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(
                f"Chat {session['id']} - {session['created_at'].strftime('%Y-%m-%d %H:%M')}",
                key=f"session_{session['id']}"
            ):
                st.session_state.current_session_id = session['id']
                st.rerun()
        with col2:
            if st.button("🗑️", key=f"delete_{session['id']}"):
                delete_chat_session(session['id'])
                if st.session_state.current_session_id == session['id']:
                    st.session_state.current_session_id = None
                st.rerun()

# Main chat interface
st.title("🛫 AI Flight Info Assistant")

# Display chat messages if a session is selected
if st.session_state.current_session_id:
    messages = get_session_messages(st.session_state.current_session_id)
    for message in messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask about flights..."):
        # Add user message
        add_message_to_session(st.session_state.current_session_id, "user", prompt)
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Get AI response
        past_context = get_past_context()
        context_prompt = "\n".join([f"User: {u}\nAI: {r}" for u, r in past_context])
        full_prompt = context_prompt + f"\nUser: {prompt}\nAI:"

        try:
            llm_response = get_llm_response(
                full_prompt,
                site_url="https://yourprojectsite.com",
                site_title="Flight Assistant"
            )
        except Exception as e:
            llm_response = f"I apologize, but I encountered an error while processing your request. Please try again."

        # Save to memory
        save_to_memory(prompt, llm_response)

        # Get additional data
        flight_data = get_flight_info(prompt)
        web_data = duckduckgo_search(prompt)

        # Add AI response
        add_message_to_session(st.session_state.current_session_id, "assistant", llm_response)
        
        # Display AI response
        with st.chat_message("assistant"):
            st.write(llm_response)

            # Only show flight data if it's not an error
            if flight_data and not flight_data.get("error"):
                st.write("✈️ Flight Information:")
                st.json(flight_data)

            # Only show web data if it contains useful information
            if web_data and (web_data.get("Abstract") or web_data.get("Results")):
                st.write("🌐 Additional Information:")
                if web_data.get("Abstract"):
                    st.write(web_data["Abstract"])
                if web_data.get("Results"):
                    for result in web_data["Results"][:2]:  # Show only first 2 results
                        st.write(f"- {result.get('Text', '')}")
            
            # Add feedback collection
            st.write("---")
            st.write("Was this response helpful?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Yes"):
                    training_manager.save_feedback(
                        user_input=prompt,
                        response=llm_response,
                        feedback_score=5.0,
                        is_helpful=True
                    )
                    st.success("Thank you for your feedback!")
            with col2:
                if st.button("👎 No"):
                    feedback = st.text_area("What could be improved?", key="feedback")
                    if st.button("Submit Feedback"):
                        training_manager.save_feedback(
                            user_input=prompt,
                            response=llm_response,
                            feedback_score=1.0,
                            feedback_comment=feedback,
                            is_helpful=False
                        )
                        st.success("Thank you for your feedback!")

else:
    st.info("👈 Select a chat session from the sidebar or create a new one to start chatting!")
