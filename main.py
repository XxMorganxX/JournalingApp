import uvicorn
import os
from src.APIs.server import app
from dotenv import load_dotenv

load_dotenv("constants.env")

if __name__ == "__main__":
    # Get environment variables or use defaults
    HOST = os.getenv("INTERNAL_HOST", "0.0.0.0")
    PORT = int(os.getenv("INTERNAL_PORT", 8000))
    RELOAD = os.getenv("API_RELOAD", "True").lower() == "true"

    uvicorn.run(
        "src.APIs.server:app",
        host=HOST,
        port=PORT,
        reload=RELOAD
    ) 