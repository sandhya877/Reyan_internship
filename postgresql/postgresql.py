from fastapi import FastAPI, HTTPException
import psycopg2
from pydantic import BaseModel

app = FastAPI()

# Database connection parameters
db_config = {
    'dbname': 'DATA1',
    'user': 'postgres',
    'password': 'Postgresql@678',
    'host': 'localhost',  # Replace with your database host
    'port': '5432',       # Replace with your database port
}

# Function to establish a database connection
def get_db_connection():
    return psycopg2.connect(**db_config)

# Pydantic model for your data (replace with your table structure)
class DataModel(BaseModel):
    name: str
    age: int

# Create operation
@app.post("/data/", response_model=DataModel)
def create_data(data: DataModel):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO csv (name, age) VALUES (%s, %s) RETURNING id, name, age",
                (data.name, data.age),
            )
            result = cursor.fetchone()
            data_id, name, age = result
            return {"id": data_id, "name": name, "age": age}  # Corrected "description" to "age"
    finally:
        connection.close()
def create_database(database_name):
    try:
        # Connect to the 'postgres' database for administrative tasks
        connection = psycopg2.connect(**db_config)

        # Create a new database
        with connection.cursor() as cursor:
            cursor.execute(f'CREATE DATABASE {database_name}')
    except psycopg2.errors.DuplicateDatabase:
        raise Exception(f"Database '{database_name}' already exists")
    finally:
        connection.close()

# ... Other CRUD operations ...

if __name__ == "__main__":
    new_database_name = 'NEW_DATABASE_NAME'  # Replace with your desired database name
    create_database(new_database_name)
    print(f"Database '{new_database_name}' created successfully.")

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    