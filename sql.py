import psycopg2
from dotenv import load_dotenv
import os
import streamlit as st

# Load environment variables
load_dotenv()
# Access secrets
DB_HOST = st.secrets["DB_HOST"]
DB_NAME = st.secrets["DB_NAME"]
DB_USER = st.secrets["DB_USER"]
DB_PASSWORD = st.secrets["DB_PASSWORD"]
DB_PORT = st.secrets["DB_PORT"]

# Connect to the database
def connect_to_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        sslmode="require"  # Enable SSL
    )
    return conn

@st.cache_data(ttl=60)
def fetch_all_titles():
    query = "SELECT title FROM books;"
    results = fetch_data(query)
    return [row[0] for row in results]

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
        INSERT INTO books (title, author, year, rack, shelf)
        VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, tuple(row))

    conn.commit()
    cursor.close()
    conn.close()
    print("Database updated with latest data.")
