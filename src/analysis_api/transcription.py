from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_items():
    return [{"item": "book"}, {"item": "pen"}]

@router.get("/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "item": f"Item {item_id}"}
