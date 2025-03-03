from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI
import os
from google import genai
from google.genai import types
from datetime import datetime


# Router ----------------------------------------------------------------------

router = APIRouter(prefix="/insights", tags=["insights"])



# Create a Pydantic model for the request body
class InsightRequest(BaseModel):
    text: str
    options: Optional[dict] = None

load_dotenv("../../.env")
load_dotenv("../../constants.env")


# Test Parameters ------------------------------------------------------------

client_type = os.getenv("CLIENT_TYPE")

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
        
        




@router.post("/generate_insights")
async def generate_insights(request: InsightRequest):
    """
    Generate insights from the provided text
    
    Example request body:
    {
        "text": "Your transcription text here",
        "options": {
            "max_length": 100,
            "format": "bullet_points"
        }
    }
    """
    
    Audio_transcription = request.text
    
    response_schema = {
        "description": "A list of responses, each with a headline and subtext",
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "headline": {
                    "type": "string",
                    "description": "The main headline."
                },
                "subtext": {
                    "type": "string",
                    "description": "Supporting subtext."
                }
            },
            "required": ["headline", "subtext"]
        }
    }
    
    try:
        if client_type == "GEMINI":
                response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[
                            "Pull out the most important insights to be stored as headers and summarize them in a concise manner.",
                            Audio_transcription
                        ],
                        config=types.GenerateContentConfig(
                                system_instruction="You are a helpful therapist assistant that generates insights from a users journal entry audio transcription.",
                                temperature= 0.7,        # 0.0 to 1.0: Lower = more focused, Higher = more creative
                                top_p= 0.95,            # 0.0 to 1.0: Nucleus sampling threshold
                                top_k= 40,              # Top K tokens to consider
                                max_output_tokens= 2048,
                                response_mime_type= "application/json",
                                response_schema= response_schema,
                        ),
                )
                return response
            
    except Exception as e:
        return {"error": str(e), "datatime": datetime.now().isoformat()}





