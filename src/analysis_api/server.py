from fastapi import FastAPI
from transcription import router as transcription_router
from sample_api import router as sample_router
from dotenv import load_dotenv
import os

# Load environment variables from the project root
load_dotenv(dotenv_path="../../constants.env")

INTERNAL_HOST = os.getenv("INTERNAL_HOST")
INTERNAL_PORT = os.getenv("INTERNAL_PORT")

app = FastAPI()

# Include the routers with optional prefixes
app.include_router(sample_router, prefix="/test_dev", tags=["test_dev"])
app.include_router(transcription_router, prefix="/transcript", tags=["transcript"])


# Run the application if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=INTERNAL_HOST, 
        port=INTERNAL_PORT,
        reload=True
    )
