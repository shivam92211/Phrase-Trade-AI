from fastapi import APIRouter, status
from fastapi import HTTPException
from schema.sentence_api import SentenceInput
from service.embeddings import add_sentence, sentence_exists
from genai.gemini import genai_model


router = APIRouter()


# API route to handle the sentence input
@router.post(
    "/add-sentence/",
    status_code=status.HTTP_201_CREATED,
    description="""
    ### Create a new Market 
    - Pass a social handle and platform
    - It will process a social handle and platform, returns a market id
    - Use this market id to buy a share
    """,
)
async def process_sentence(input_sentence: SentenceInput):
    sentence = input_sentence.sentence

    try:
        # Check if the sentence already exists with a distance less than 0.1
        exists, existing_sentence = sentence_exists(sentence)

        if exists:
            return {
                "message": "Sentence already exists",
                "existing_sentence": existing_sentence,
            }

        # If it doesn't exist, generate its embedding and add it to the database
        embedding = genai_model.embed_documents([sentence])[0]
        add_sentence(sentence, embedding)

        return {"message": "Sentence added successfully"}
    except Exception as e:
        # Log the exception and return a 500 error
        print(f"Error processing sentence: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
