from fastapi import FastAPI
from database.postgres import get_db_connection

# all api routers
from api.add_sentence import router as add_sentence_router

# FastAPI initialization
app = FastAPI(
    title="Phrase.Trade",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.on_event("startup")
async def startup_event():
    # check if vector extension is loaded
    # and table exists
    connection = get_db_connection()
    cursor = connection.cursor()

    # SQL query to find similar sentences
    sql_query = """
        -- Load vector extension if not loaded
        CREATE EXTENSION IF NOT EXISTS vector;

        -- Create table with columns for phrase and embedding
        CREATE TABLE IF NOT EXISTS new_embedding (
            id SERIAL PRIMARY KEY,
            phrase VARCHAR(521) NOT NULL,
            embedding VECTOR(768)  --Adjust the dimension as needed
        );    
    """
    cursor.execute(sql_query)
    connection.commit()
    cursor.close()

    print("Starting up")


app.include_router(add_sentence_router, tags=["add-sentence"])

app.setup()
