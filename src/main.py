from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database.postgres import get_db_connection
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from src.service.rate_limiter import pt_limiter


# all api routers
from api.add_sentence import router as add_sentence_router
from api.tell_mood import router as tell_mood_router

# FastAPI initialization
app = FastAPI(
    title="Phrase.Trade",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # important for setting session cookies
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach the rate limit exceeded handler to FastAPI
app.state.limiter = pt_limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Middleware for rate limiting
@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    try:
        response = await call_next(request)
    except RateLimitExceeded as exc:
        return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)
    return response


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
            phrase VARCHAR(512) NOT NULL,
            hash VARCHAR(64) NOT NULL,
            embedding VECTOR(768)  --Adjust the dimension as needed
        );    
        
        -- Create an index on the hash column
        CREATE INDEX IF NOT EXISTS idx_hash ON new_embedding(hash);
    """
    cursor.execute(sql_query)
    connection.commit()
    cursor.close()
    connection.close()

    print("Starting up...")


app.include_router(add_sentence_router, tags=["add-sentence"])
app.include_router(tell_mood_router, tags=["tell-mood"])

app.setup()
