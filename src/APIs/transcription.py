from fastapi import APIRouter, HTTPException
from openai import OpenAI
from dotenv import load_dotenv
from google import genai
import os


load_dotenv(".env")
load_dotenv("constants.env")


transcription_model = os.getenv("TRANSCRIPTION_MODEL")

CLIENT = None



if transcription_model == "GEMINI":
    CLIENT = genai.Client(
                api_key=os.getenv("GEMINI_API_KEY")
        )
router = APIRouter()

            
    
@router.get("/")
def transcribe_audio(UploadFileName: str, file_type: str):
    try:
        
        file_path_from_root = "data/recording_data/"
        
        print("Current working directory:", os.getcwd())
        # Use a relative path or get the path from environment variables
        file_path = os.path.join(os.getenv("RECORDING_DATA_PATH", "data/recording_data"), 
                                f"{UploadFileName}.{file_type}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        myfile = CLIENT.files.upload(file=f"{file_path_from_root}{UploadFileName}.{file_type}")
    
        transcript = CLIENT.models.generate_content(
            model="gemini-2.0-flash",
            contents=['Generate a transcript of the speech.', myfile]
        )
        return transcript.text
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
