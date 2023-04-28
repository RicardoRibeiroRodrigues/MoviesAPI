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
SQLALCHEMY_SERVER_URL = f"mysql://{user}:{password}@{host}"

# Codigo para criar o schema no banco de dados
engine = create_engine(SQLALCHEMY_SERVER_URL)
with engine.connect() as conn:
    if not conn.dialect.has_schema(conn, database):
        conn.execute(CreateSchema(database))

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
