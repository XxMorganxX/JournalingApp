from fastapi import FastAPI
from file_storage_s3 import router as storage_router

app = FastAPI(
    title="File Storage API",
    description="API for handling file uploads and downloads with S3",
    version="1.0.0"
)

# Include the storage router
app.include_router(storage_router)

# Optional: Add a root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the File Storage API"}

# This is important - uvicorn needs this to run with hot reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True) 