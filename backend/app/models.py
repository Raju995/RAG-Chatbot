

from sqlalchemy import Column, Integer, Text, String, DateTime
from datetime import datetime
from .database import Base

class Document(Base):
    __tablename__ = "document_name"

    id = Column(Integer, primary_key=True)
    doc_id = Column(String, index=True)
    doc_name = Column(Text)
   
class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    role = Column(String)  # user / assistant
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True)
    doc_id = Column(String, index=True)
    content = Column(Text)
    embedding = Column(Text) 