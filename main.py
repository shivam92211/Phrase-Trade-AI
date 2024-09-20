from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not set in environment variables.")
genai.configure(api_key=google_api_key)

# Initialize GoogleGenerativeAIEmbedding
model = GoogleGenerativeAIEmbeddings(
    model='models/embedding-001'
)

# Connect to the PostgreSQL database
def get_db_connection():
    try:
        connection = psycopg2.connect(
            dbname="vector_db",
            user="postgres",
            password="great",
            host="localhost",
            port="5432"
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        raise

# FastAPI initialization
app = FastAPI()

# Pydantic model to validate input data
class SentenceInput(BaseModel):
    sentence: str

# Function to check if a similar sentence exists with a distance less than 0.1
def sentence_exists(query_sentence):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Generate the embedding for the query sentence
        query_embedding = model.embed_documents([query_sentence])[0]  # Get the embedding as a list
        query_embedding_str = ','.join(map(str, query_embedding))
        query_embedding_literal = f'[{query_embedding_str}]'

        # SQL query to find similar sentences
        sql_query = """
        SELECT phrase, embedding <=> %s::vector AS distance
        FROM new_embedding
        ORDER BY distance
        LIMIT 1;
        """

        cursor.execute(sql_query, (query_embedding_literal,))
        result = cursor.fetchone()

        if result:
            # result = (phrase, distance)
            phrase = result[0]
            distance = result[1]
            if distance < 0.1:
                return True, phrase  # Sentence exists
        return False, None  # Sentence doesn't exist
    except Exception as e:
        print(f"Error in sentence_exists: {e}")
        return False, None
    finally:
        cursor.close()
        connection.close()

# Function to add a new sentence to the database
def add_sentence(sentence, embedding):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Convert embedding to string in the format 'x1, x2, ...'
        embedding_str = ','.join(map(str, embedding))
        embedding_literal = f'[{embedding_str}]'  # Ensure it starts and ends with brackets

        # SQL query to insert the new sentence
        insert_query = """
        INSERT INTO new_embedding (phrase, embedding)
        VALUES (%s, %s::vector);
        """
        cursor.execute(insert_query, (sentence, embedding_literal))
        connection.commit()
    except Exception as e:
        print(f"Error in add_sentence: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

# API route to handle the sentence input
@app.post("/add-sentence/")
async def process_sentence(input_sentence: SentenceInput):
    sentence = input_sentence.sentence

    try:
        # Check if the sentence already exists with a distance less than 0.1
        exists, existing_sentence = sentence_exists(sentence)

        if exists:
            return {"message": "Sentence already exists", "existing_sentence": existing_sentence}
        
        # If it doesn't exist, generate its embedding and add it to the database
        embedding = model.embed_documents([sentence])[0]
        add_sentence(sentence, embedding)

        return {"message": "Sentence added successfully"}
    except Exception as e:
        # Log the exception and return a 500 error
        print(f"Error processing sentence: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
