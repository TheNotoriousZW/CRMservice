from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from fastapi import FastAPI
from fastapi import Request


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