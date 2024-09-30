import json
from fastapi import APIRouter, HTTPException, Request
from src.schema.sentence_api import PhraseData
from src.genai.gemini import mood_model
from src.service.rate_limiter import pt_limiter

router = APIRouter()


@router.post("/phrase/")
@pt_limiter.limit("15/minute")
def analyze_phrase(request: Request, phrase_data: PhraseData):
    """
    Analyzes the given phrase and returns a motivating reaction along with a mood.

    Args:
        phrase_data (PhraseData): A Pydantic model containing the title, body, and author of the phrase.

    Returns:
        dict: A dictionary containing the reaction and mood.
    """
    title = phrase_data.title
    body = phrase_data.body
    author = phrase_data.author

    # Construct the prompt
    prompt = f"""
        Role: You are a Text-based NFT analyzer and motivator to Mint the given Phrase into an NFT.
        
        Task: Your task is to:
        1. Analyze the given phrase.
        2. Generate a short motivational reaction under 15 words, based on the phrase so that the User Mints it.
        3. Do include the author's first name and call to action. 
        4. Identify the mood from the available options.
        5. Return the result in proper JSON format, without any additional characters or backticks.
        
        Context: The provided phrase represents a sentiment or situation that requires motivational feedback. Based on this, craft a short motivational reaction and select the most appropriate mood for the phrase.
        
        Make sure your response uses this exact JSON structure and nothing else:
        {{
            "Motivation": "<Your motivational reaction here>",
            "Mood": "<One of: Happy, Amazed, Wow, Smiling, Cheering>"
        }}
        
        Important: Return only the JSON object, without any other text or formatting. 
        Important: In the response strictly avoid any single quotes and double quotes.
        
        Phrase: "{body}"
        Author: "{author}"
        """

    try:
        # Use the Gemini API to get the response with retry logic
        response = mood_model.generate_content(
            prompt
        )  # This assumes the model has been initialized properly.
        response_text = response.text
        print(response_text)

        # Convert to JSON
        json_response = json.loads(response_text)
        return json_response

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating response: {str(e)}"
        )
