import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config.settings import env


if not env.GOOGLE_API_KEY:
    raise ValueError("Gemini environment variable is not set.")

# Configure Google API
genai.configure(api_key=env.GOOGLE_API_KEY)

# Initialize GoogleGenerativeAIEmbedding
genai_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

generation_config = {
    "temperature": 0.3,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 30,
}
mood_model = genai.GenerativeModel("gemini-1.5-flash")
