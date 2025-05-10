from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('chat_sessions.id'))
    role = Column(String(10))  # 'user' or 'assistant'
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("ChatSession", back_populates="messages")

class ChatMemory(Base):
    __tablename__ = 'chat_memory'
    
    id = Column(Integer, primary_key=True)
    user_input = Column(String)
    response = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    searches = relationship("SearchHistory", back_populates="user")
    preferences = relationship("UserPreferences", back_populates="user")

class SearchHistory(Base):
    __tablename__ = 'search_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    search_type = Column(String(20))  # flight, hotel, restaurant
    origin = Column(String(100))
    destination = Column(String(100))
    departure_date = Column(DateTime)
    return_date = Column(DateTime)
    search_results = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="searches")

class UserPreferences(Base):
    __tablename__ = 'user_preferences'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    preferred_airlines = Column(JSON)
    preferred_hotel_chains = Column(JSON)
    preferred_cuisines = Column(JSON)
    budget_range = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="preferences")

class TrainingData(Base):
    __tablename__ = 'training_data'
    
    id = Column(Integer, primary_key=True)
    user_input = Column(String)
    response = Column(String)
    feedback_score = Column(Float)  # User rating of response quality (1-5)
    feedback_comment = Column(String)  # Optional user feedback
    is_helpful = Column(Boolean)  # Whether the response was helpful
    created_at = Column(DateTime, default=datetime.utcnow)
    used_for_training = Column(Boolean, default=False)  # Track if this data has been used for training

class ModelVersion(Base):
    __tablename__ = 'model_versions'
    
    id = Column(Integer, primary_key=True)
    version = Column(String)  # Model version identifier
    training_data_count = Column(Integer)  # Number of examples used for training
    performance_metrics = Column(JSON)  # Store accuracy, loss, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=False)  # Whether this is the currently active model

def init_db():
    engine = create_engine('sqlite:///travel_planner.db')
    Base.metadata.create_all(engine)
    return engine
