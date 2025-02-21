from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import boto3
from botocore.exceptions import ClientError
import os
from typing import Optional
import io

from dotenv import load_dotenv

load_dotenv("../../.env")

router = APIRouter(prefix="/storage", tags=["storage"])

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'us-east-2')
)

BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

@router.post("/upload")
async def upload_file(file: UploadFile) -> dict:
    """
    Upload a file to S3 bucket
    """
    try:
        # Read file content
        file_content = await file.read()
        
        # Upload to S3
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=file.filename,
            Body=file_content
        )
        
        return {
            "message": "File uploaded successfully",
            "filename": file.filename
        }
    except ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading file to S3: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@router.get("/download/{filename}")
async def download_file(filename: str) -> StreamingResponse:
    """
    Download a file from S3 bucket
    """
    try:
        # Get file from S3
        response = s3_client.get_object(
            Bucket=BUCKET_NAME,
            Key=filename
        )
        
        # Create an in-memory bytes buffer
        file_stream = io.BytesIO(response['Body'].read())
        
        # Return streaming response
        return StreamingResponse(
            iter([file_stream.getvalue()]),
            media_type='application/octet-stream',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"'
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise HTTPException(
                status_code=404,
                detail=f"File {filename} not found"
            )
        raise HTTPException(
            status_code=500,
            detail=f"Error downloading file from S3: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@router.delete("/{filename}")
async def delete_file(filename: str) -> dict:
    """
    Delete a file from S3 bucket
    """
    try:
        s3_client.delete_object(
            Bucket=BUCKET_NAME,
            Key=filename
        )
        return {
            "message": "File deleted successfully",
            "filename": filename
        }
    except ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting file from S3: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@router.get("/list")
async def list_files(prefix: Optional[str] = None) -> dict:
    """
    List all files in the S3 bucket
    """
    try:
        if prefix:
            response = s3_client.list_objects_v2(
                Bucket=BUCKET_NAME,
                Prefix=prefix
            )
        else:
            response = s3_client.list_objects_v2(
                Bucket=BUCKET_NAME
            )
        
        files = []
        if 'Contents' in response:
            files = [obj['Key'] for obj in response['Contents']]
            
        return {
            "files": files
        }
    except ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing files from S3: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )
