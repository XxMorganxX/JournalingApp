from fastapi import APIRouter
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv("../../.env")
load_dotenv("../../constants.env")


client_type = os.getenv("CLIENT_TYPE")



router = APIRouter()

@router.get("/")
def get_items():
    return [{"item": "book"}, {"item": "pen"}]

@router.get("/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "item": f"Item {item_id}"}
