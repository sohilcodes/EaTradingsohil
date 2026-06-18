from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class BrokerAccountRequest(BaseModel):
    user_id: str
    broker_name: str = "quotex"
    broker_email: str | None = None
    broker_user_id: str | None = None
    session_token: str | None = None
