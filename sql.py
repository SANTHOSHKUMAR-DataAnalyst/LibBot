import psycopg2
from dotenv import load_dotenv
import os
import streamlit as st

# Load environment variables
load_dotenv()

# Function to connect to PostgreSQL
def connect_to_db():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        sslmode="require"
    )
    return conn

# Function to execute a query and fetch data
def fetch_data(query):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# Function to insert data into PostgreSQL
def insert_data(query, data):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    conn.close()

# Function to clear and update the database with new data
def update_database(df):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Clear existing data in the table
    cursor.execute("DELETE FROM books;")

    # Insert new data
    for _, row in df.iterrows():
        insert_query = """
        INSERT INTO books (title, author, year, rack, shelf, image)
        VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, tuple(row))

    conn.commit()
    cursor.close()
    conn.close()
    print("Database updated with latest data.")
