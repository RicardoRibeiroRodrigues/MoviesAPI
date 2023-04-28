from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema
from dotenv import load_dotenv
import os


load_dotenv()
# Replace the following variables with your MySQL server details
user = os.getenv("MD_DB_USERNAME")
password = os.getenv("MD_DB_PASSWORD")
host = os.getenv("MD_DB_SERVER")
database = "moviesProj"
SQLALCHEMY_DATABASE_URL = f"mysql://{user}:{password}@{host}/{database}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
