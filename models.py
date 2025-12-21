from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    maternal_records = relationship("MaternalRecord", back_populates="patient")

class MaternalRecord(Base):
    __tablename__ = "maternal_records"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    age = Column(Integer, nullable=False)
    systolic_bp = Column(Integer, nullable=False)
    diastolic_bp = Column(Integer, nullable=False)
    bs = Column(Float, nullable=False)
    body_temp = Column(Float, nullable=False)
    heart_rate = Column(Integer, nullable=False)
    risk_level = Column(String, nullable=False)
    model_used = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="maternal_records")
