import streamlit as st
from sql import fetch_data
from dotenv import load_dotenv
import os 
import pandas as pd
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def generate_sql_query(book_title):
    prompt = f"""
    Generate a SQL query to retrieve the title,author , rack and shelf number from the books table where the title is '{book_title}'
    and the table books contains multiple columns as [title,author,year,rack,shelf].only generate sql query without ''' quotation mark.
    example -->  sql_query = f"SELECT title,author,rack, shelf FROM books WHERE title = '[book_title]';" 
    Generate a PostgreSQL full-text search query to retrieve the title,author, rack and shelf number from the books table where the title is similar to '{book_title}'.
    Use the to_tsvector and to_tsquery functions.only generate sql query without ''' quotation mark"""

#    prompt = f""" 
 #   Generate a PostgreSQL full-text search query to retrieve the rack and shelf number from the books table where the title is similar to '{book_title}'.
 #   Use the to_tsvector and to_tsquery functions. """

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text

# Custom CSS for gradient background
def set_gradient_background():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            background-size: cover;
            background-attachment: fixed;
            color: black;
        }
        .stTextInput>div>div>input, .stButton>button {
            background-color: rgba(255, 255, 255, 0.9);
            color: black;
        }
        .stTable {
            background-color: rgba(255, 255, 255, 0.9);
            color: black;
            border: 1px solid black;
        }
        .stTable th, .stTable td {
            border: 1px solid black;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Set gradient background
set_gradient_background()


st.title("Library Assistant ChatBot")
user_input = st.text_input("Enter Book Title Here : ")
total = "select count(*) from books;"
st.write = fetch_data(total)
st.button("Submit")

if user_input:
    sql_query = generate_sql_query(user_input)
    results = fetch_data(sql_query)


    if results:
        st.write("Location of the Book")
        df = pd.DataFrame(results, columns=["Title","Author","Rack", "Shelf"])
        st.dataframe(df)
    else:
        st.write("Currently Unavailable")
