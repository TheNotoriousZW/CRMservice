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
        },
        # {
        #     "action": "input",
        #     "eventUrl": ["http://127.0.0.1:8000/input"],
        #     "type": ["dtmf", "speech"],
        #     "dtmf": {
        #         "maxDigits": 1,
        #         "timeout": 10,
        #         "terminator": "#"
        #     },
        #     "speech": {
        #         "context": "You are a helpful assistant that can answer questions and help with tasks."
        #     }
        # }
    ]

@app.post("/input")
async def input(event: Request):
    return event