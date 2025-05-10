from sqlalchemy.orm import Session
from db.models import ChatSession, ChatMessage, init_db
from datetime import datetime

def create_new_chat_session():
    """Create a new chat session"""
    engine = init_db()
    session = Session(engine)
    try:
        chat_session = ChatSession(created_at=datetime.utcnow())
        session.add(chat_session)
        session.commit()
        session.refresh(chat_session)  # Refresh to get the ID
        session_id = chat_session.id  # Get the ID before closing
        return session_id
    finally:
        session.close()

def get_all_chat_sessions():
    """Get all chat sessions"""
    engine = init_db()
    session = Session(engine)
    try:
        sessions = session.query(ChatSession).order_by(ChatSession.created_at.desc()).all()
        # Convert to list of dictionaries to avoid detached instance issues
        return [{"id": s.id, "created_at": s.created_at} for s in sessions]
    finally:
        session.close()

def get_session_messages(session_id):
    """Get all messages for a specific session"""
    engine = init_db()
    session = Session(engine)
    try:
        messages = session.query(ChatMessage)\
            .filter(ChatMessage.session_id == session_id)\
            .order_by(ChatMessage.timestamp)\
            .all()
        return [{"role": msg.role, "content": msg.content} for msg in messages]
    finally:
        session.close()

def add_message_to_session(session_id, role, content):
    """Add a message to a chat session"""
    engine = init_db()
    session = Session(engine)
    try:
        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
            timestamp=datetime.utcnow()
        )
        session.add(message)
        session.commit()
    finally:
        session.close()

def delete_chat_session(session_id):
    """Delete a chat session and all its messages"""
    engine = init_db()
    session = Session(engine)
    try:
        # Delete all messages in the session
        session.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()
        # Delete the session
        session.query(ChatSession).filter(ChatSession.id == session_id).delete()
        session.commit()
    finally:
        session.close() 