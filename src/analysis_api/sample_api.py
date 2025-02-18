from fastapi import APIRouter
from dotenv import load_dotenv
from openai import OpenAI
import os
from google import genai



load_dotenv("../../.env")
load_dotenv("../../constants.env")


# Test Parameters ------------------------------------------------------------

client_type = os.getenv("CLIENT_TYPE")
test_content = "Explain how AI works"

# Models ------------------------------------------------------------

client = None

if client_type is None:
        raise ValueError("Client type is not set")

elif client_type == "OPENAI":
        # Not sure if this works
        client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
        )

        completion = client.chat.completions.create(
                model="gpt-4o-mini",
                store=True,
                messages=[
                {"role": "user", "content": test_content}
                ]
        )

elif client_type == "GEMINI":
        client = genai.Client(
                api_key=os.getenv("GEMINI_API_KEY")
        )
        
        print("Waiting on Gemini response...")
        
        response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents= test_content,
        )

        
        print(response.text)
                
        

# ROUTES ------------------------------------------------------------

router = APIRouter()

@router.get("/")
def get_users():
    return [{"username": "alice"}, {"username": "bob"}]

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "username": f"user{user_id}"}
