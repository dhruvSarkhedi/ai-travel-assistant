import json
from sqlalchemy.orm import Session
from db.models import ChatMemory, init_db
from datetime import datetime, timedelta

def save_to_memory(user_input: str, response_text: str):
    engine = init_db()
    session = Session(engine)
    try:
        entry = ChatMemory(
            user_input=user_input,
            response=response_text,
            timestamp=datetime.utcnow()
        )
        session.add(entry)
        session.commit()
    finally:
        session.close()

def get_past_context(limit: int = 5):
    """Get the last N conversations from memory"""
    engine = init_db()
    session = Session(engine)
    try:
        recent_messages = session.query(ChatMemory)\
            .order_by(ChatMemory.timestamp.desc())\
            .limit(limit)\
            .all()
        return [(msg.user_input, msg.response) for msg in reversed(recent_messages)]
    finally:
        session.close()
