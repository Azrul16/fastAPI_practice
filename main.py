from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Course(BaseModel):
    name: str
    instructor: str | None = None
    duration: float
    website: HttpUrl
    
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="practice",
            user="postgres",
            password="1234",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Database connection failed!")
        print("Error:", error)
        time.sleep(2)  # Wait for 2 seconds before retrying
    
@app.get("/")
def read_root():
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    return { "courses": courses}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.post("/courses/")
def create_course(course: Course):
    return course