from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120))
    phone = Column(String(20))
    company = Column(String(100))
    position = Column(String(100))
    address = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    owner_id = Column(Integer, ForeignKey('users.id'))
    
    # Relationships
    owner = relationship("User", back_populates="contacts")
    tasks = relationship("Task", back_populates="contact")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
