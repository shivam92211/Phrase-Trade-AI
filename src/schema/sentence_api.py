from pydantic import BaseModel


# Pydantic model to validate input data
class SentenceHashInput(BaseModel):
    sentence: str
    hash: str


class SentenceInput(BaseModel):
    sentence: str


class HashInput(BaseModel):
    hash: str


class PhraseData(BaseModel):
    title: str
    body: str
    author: str
