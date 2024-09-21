from fastapi import APIRouter, status
from fastapi import HTTPException
from schema.sentence_api import HashInput, SentenceInput, SentenceHashInput
from service.embeddings import add_sentence, remove_sentence, sentence_exists
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
async def process_sentence(input_sentence: SentenceHashInput):
    sentence = input_sentence.sentence
    hash = input_sentence.hash

    try:
        # Check if the sentence already exists with a distance less than 0.1
        exists, existing_sentence, oldHash = sentence_exists(sentence)

        if exists:
            return {
                "message": "Sentence already exists",
                "existing_sentence": existing_sentence,
                "hash": oldHash,
            }

        # If it doesn't exist, generate its embedding and add it to the database
        embedding = genai_model.embed_documents([sentence])[0]
        add_sentence(hash, sentence, embedding)

        return {"message": "Sentence added successfully"}
    except Exception as e:
        # Log the exception and return a 500 error
        print(f"Error processing sentence: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# API route to handle the sentence input
@router.post(
    "/check-sentence/",
    status_code=status.HTTP_200_OK,
    description="""
    ### Check if a sentence exists
    - This checks into the vector database if a sentence exists
    """,
)
async def check_sentence(input_sentence: SentenceInput):
    sentence = input_sentence.sentence

    try:
        # Check if the sentence already exists with a distance less than 0.1
        exists, existing_sentence, hash = sentence_exists(sentence)

        if exists:
            return {
                "message": "Sentence already exists",
                "existing_sentence": existing_sentence,
                "hash": hash,
            }

        return {"message": "Sentence does not exist"}
    except Exception as e:
        # Log the exception and return a 500 error
        print(f"Error processing sentence: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete(
    "/delete-sentence/",
    status_code=status.HTTP_200_OK,
    description="""
    ### Delete a sentence
    - This deletes a sentence from the vector database
    """,
)
async def delete_sentence(input_sentence: HashInput):
    hash = input_sentence.hash

    try:
        remove_sentence(hash)
        return {"message": "Sentence deleted successfully", "done": True}
    except Exception as e:
        # Log the exception and return a 500 error
        print(f"Error processing sentence: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
