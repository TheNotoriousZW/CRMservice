from database import base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

class Company(base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    phone_number = Column(String)
    company_number = Column(Integer, ForeignKey("company_numbers.id"), unique=True, nullable=False, )
    email = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    country = Column(String, default="US")
    subscription_status = Column(String)
    


class Customer(base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now)
    
    # Relationship
    company_id = Column(Integer, ForeignKey("companies.id"))
    appointments = Column(String, ForeignKey("appointments.id"))

class Appointment(base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    service_name = Column(String)
    appointment_date = Column(DateTime)
    duration = Column(Integer)  # in minutes
    status = Column(String, default="scheduled")  # scheduled, completed, cancelled
    notes = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now)
    
    # Relationship
    customer =  Column(String, ForeignKey("customers.id"))     

class CompanyNumber(base):
    __tablename__ = "company_numbers"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    number = Column(String, unique=True, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"))
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now)
    