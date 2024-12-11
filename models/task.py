from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime
import enum

class TaskStatus(enum.Enum):
    TODO = "To-do"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class TaskPriority(enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    due_date = Column(DateTime)
    reminder_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)

    # Foreign Keys
    assigned_to_id = Column(Integer, ForeignKey('users.id'))
    contact_id = Column(Integer, ForeignKey('contacts.id'))

    # Relationships
    assigned_to = relationship("User", back_populates="tasks")
    contact = relationship("Contact", back_populates="tasks")
