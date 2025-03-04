from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import Optional
from google import genai
from google.generativeai import types

from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
import os

# Router ----------------------------------------------------------------------

router = APIRouter(prefix="/insights", tags=["insights"])



# Create a Pydantic model for the request body
class InsightRequest(BaseModel):
    text: str
    options: Optional[dict] = None

load_dotenv(".env")
load_dotenv("constants.env")


# Test Parameters ------------------------------------------------------------

client_type = os.getenv("CLIENT_TYPE")

# Models ------------------------------------------------------------

CLIENT = None

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
        CLIENT = genai.Client(
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
        "description": "A list of responses containing insights and reminders",
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["insight", "reminder"],
                    "description": "Whether this item is an insight or a reminder"
                },
                "headline": {
                    "type": "string",
                    "description": "The main headline or reminder title"
                },
                "subtext": {
                    "type": "string",
                    "description": "Supporting subtext or reminder details"
                },
                "date": {
                    "type": "string",
                    "description": "ISO format date for reminders, if mentioned",
                    "format": "date-time"
                }
            },
            "required": ["type", "headline", "subtext"]
        }
    }
    
    try:
        if client_type == "GEMINI":
                response = CLIENT.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[
                            """Analyze this text for two types of information:
                            1. Important psychological insights and themes
                            2. Any mentioned future events, appointments, or tasks that should be remembered
                            
                            For insights: Pull out the most important psychological insights and summarize them.
                            For reminders: If any future events, tasks, or appointments are mentioned, extract them with their dates/times.
                            """,
                            Audio_transcription
                        ],
                        config=types.GenerateContentConfig(
                                system_instruction="""You are a helpful therapist assistant that:
                                1. Generates psychological insights from journal entries
                                2. Identifies and extracts any mentioned future events or tasks
                                Be precise with dates and times when mentioned.""",
                                temperature=0.7,
                                top_p=0.95,
                                top_k=40,
                                max_output_tokens=2048,
                                response_mime_type="application/json",
                                response_schema=response_schema,
                        ),
                )
                return response
            
    except Exception as e:
        return {"error": str(e), "datatime": datetime.now().isoformat()}





