from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import engine, session, base
from schema import AddCompany
from typing import Annotated
from models import Company, CompanyNumber
from vonage import Auth, Vonage
from vonage_numbers import NumberParams, NumbersStatus
from utils import find_number
from schema import AddCompany

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
async def create_company(company: AddCompany, db: db, number: CompanyNumber):
    db_company = Company(name=company.name,
                         phone_number=company.phone_number,
                         company_number=find_number(),
                         email=company.email,
                         address=company.address,
                         city=company.city,
                         state=company.state,
                         zip_code=company.zip_code,
                         country=company.country)
    db.add(db_company)
    number = CompanyNumber(number=db_company.company_number, company_id=db_company.id)
    db.add(number)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Company created successfully"})

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