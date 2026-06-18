from fastapi import APIRouter, HTTPException
from app.schemas import SignupRequest, LoginRequest
from app.supabase_client import supabase, supabase_admin

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(payload: SignupRequest):
    try:
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

        user_id = response.user.id

        # Now insert into profiles table
        profile_response = supabase_admin.table("profiles").insert({
            "id": user_id,
            "email": payload.email,
            "full_name": payload.full_name
        }).execute()

        return {
            "message": "Signup successful",
            "user_id": user_id,
            "email": payload.email
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(payload: LoginRequest):
    try:
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

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
