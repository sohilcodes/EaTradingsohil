from fastapi import APIRouter, HTTPException
from app.supabase_client import supabase_admin

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/{user_id}")
def get_profile(user_id: str):
    response = supabase_admin.table("profiles").select("*").eq("id", user_id).single().execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Profile not found")

    return response.data
