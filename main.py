from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from fastapi import FastAPI, Depends, HTTPException
from fastapi import Request
from sqlalchemy.orm import Session
from database import engine, session, base
import models

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

@app.get("/")
def read_root():
    return {"message": "Welcome to CRM Service API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}

app = FastAPI()

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