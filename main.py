from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import FRONTEND_URL
from app.routes.auth import router as auth_router
from app.routes.profile import router as profile_router
from app.routes.health import router as health_router

app = FastAPI(title="Sohil EA Trading Backend", version="1.0.0")

origins = [FRONTEND_URL] if FRONTEND_URL else ["https://sohileatrading.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(profile_router, prefix="/api")
