from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai


app = FastAPI()

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API with API key from environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
generation_config = {
    "temperature": 0.3,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 30   
}
model = genai.GenerativeModel("gemini-1.5-flash")
#model = genai.GenerativeModel("gemini-1.5-pro-latest")

class PhraseData(BaseModel):
    title: str
    body: str
    author: str


@app.post("/phrase/")
def analyze_phrase(phrase_data: PhraseData):
    """
    Analyzes the given phrase and returns a motivating reaction along with a mood.
    
    Args:
        phrase_data (PhraseData): A Pydantic model containing the title, body, and author of the phrase.
        
    Returns:
        dict: A dictionary containing the reaction and mood.
    """
    body = phrase_data.body

    # Construct the prompt
    prompt = f"""
        Role: You are a motivational coach who analyzes phrases and provides emotionally encouraging responses.

        Task: Your task is to:
        1. Analyze the given phrase.
        2. Generate a short motivational reaction based on the phrase.
        3. Identify the mood from the available options.
        4. Return the result in proper JSON format, without any additional characters or backticks.

        Context: The provided phrase represents a sentiment or situation that requires motivational feedback. Based on this, craft a short motivational reaction and select the most appropriate mood for the phrase.

        Make sure your response uses this exact JSON structure and nothing else:
        {{
            "Motivation": "<Your motivational reaction here>",
            "Mood": "<One of: Happy, Amazed, Wow, Smiling, Cheering>"
        }}

        Important: Return only the JSON object, without any other text or formatting. 
        Important: In the response strictly avoid any single quotes and double quotes.

        Phrase: "{body}"
        """


    try:
        # Use the Gemini API to get the response with retry logic
        response = model.generate_content(prompt)  # This assumes the model has been initialized properly.
        response_text = response.text
        print(response_text)

        # Convert to JSON
        json_response = json.loads(response_text)
        return json_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")
