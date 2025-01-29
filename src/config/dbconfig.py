import os
import psycopg2  # type: ignore
from dotenv import load_dotenv  # type: ignore

load_dotenv()

connection = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DBNAME"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
)

cursor = connection.cursor()
