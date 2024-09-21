from pydantic import BaseModel


# Pydantic model to validate input data
class SentenceInput(BaseModel):
    sentence: str
