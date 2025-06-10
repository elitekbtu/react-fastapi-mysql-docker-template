from fastapi import FastAPI
from dotenv import load_dotenv
import os
import pymysql

load_dotenv()

app = FastAPI()

# Database configuration
def get_db_connection():
    return pymysql.connect(
        host="mysql",
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test-db")
async def test_db():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION() as version")
            result = cursor.fetchone()
        return {"database_status": "connected", "version": result["version"]}
    except Exception as e:
        return {"database_status": "error", "details": str(e)}
    finally:
        connection.close()