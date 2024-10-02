from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from src.service.create_required_tables import create_required_tables
from src.config.settings import env

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
    allow_origins=env.ALLOWED_ORIGINS,  # important for setting session cookies
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    create_required_tables()
    print("Starting up...")


app.include_router(add_sentence_router, tags=["add-sentence"])
app.include_router(tell_mood_router, tags=["tell-mood"])

app.setup()
