from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = f"postgresql://postgres:{os.getenv("POSTGRES_PQ")}@localhost:5432/CommunicationLayer"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()
