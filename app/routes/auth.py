from fastapi import APIRouter, HTTPException
from app.schemas import SignupRequest, LoginRequest
from app.supabase_client import supabase

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(payload: SignupRequest):
    response = supabase.auth.sign_up({
        "email": payload.email,
        "password": payload.password,
        "options": {
            "data": {
                "full_name": payload.full_name
            }
        }
    })

    if not response.user:
        raise HTTPException(status_code=400, detail="Signup failed")

    return {
        "message": "Signup successful",
        "user_id": response.user.id,
        "email": response.user.email
    }

@router.post("/login")
def login(payload: LoginRequest):
    response = supabase.auth.sign_in_with_password({
        "email": payload.email,
        "password": payload.password
    })

    if not response.user or not response.session:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "user": {
            "id": response.user.id,
            "email": response.user.email
        }
      }
