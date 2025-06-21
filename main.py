from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from fastapi import FastAPI, Depends, HTTPException
from fastapi import Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import engine, session, base
from schema import AddCompany
from typing import Annotated
from models import Company
from vonage import Auth, Vonage
from vonage_numbers import NumberParams, NumbersStatus

# Create all tables
base.metadata.create_all(bind=engine)

app = FastAPI(title="CRM Service API")

# Dependency to get database session
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

db = Annotated[Session, Depends(get_db)]
@app.get("/")
def read_root():
    return {"message": "Welcome to CRM Service API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}

@app.post("/create_company")
async def create_company(company: AddCompany, db: db):
    db_company = Company(**company.model_dump())
    db.add(db_company)
    db.commit()
    return {"message": "Company created successfully"}

@app.get("/listener")
async def listen():
    return [
        {
            "action": "talk",
            "text": "This is Zaphon and im here to make your life better"
        }
    ]

@app.post("/input")
async def input(event: Request):
    return event