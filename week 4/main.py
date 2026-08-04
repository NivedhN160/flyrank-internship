import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-supabase-anon-key")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class AuthCredentials(BaseModel):
    email: str = Field(..., example="user@example.com")
    password: str = Field(..., example="password123")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server running and connected to Supabase")
    yield

app = FastAPI(
    title="Auth API (Supabase Integration)",
    description="A secure FastAPI service handling user authentication with Supabase Auth.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {"message": "Auth API Server running and connected to Supabase"}

@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}

@app.get("/protected/profile")
def protected_profile_verified(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"error": "Access token required"}
        )
    token = authorization.split("Bearer ")[1].strip()
    if not token:
        return JSONResponse(
            status_code=401,
            content={"error": "Access token required"}
        )
    
    try:
        user_response = supabase.auth.get_user(token)
        user = user_response.user
        if not user:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid or expired token"}
            )
        return {
            "id": user.id,
            "email": user.email,
            "created_at": str(user.created_at) if hasattr(user, "created_at") else None,
            "role": getattr(user, "role", "authenticated")
        }
    except Exception:
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid or expired token"}
        )

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
async def signup(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid or missing JSON body"}
        )
    
    if not isinstance(data, dict):
        return JSONResponse(
            status_code=400,
            content={"error": "Request body must be a JSON object"}
        )
        
    email = data.get("email")
    password = data.get("password")
    
    if not email or not isinstance(email, str) or not email.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Email is required"}
        )
    if not password or not isinstance(password, str) or not password.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Password is required"}
        )

    try:
        response = supabase.auth.sign_up({
            "email": email.strip(),
            "password": password.strip()
        })
        user = response.user
        user_data = {
            "id": user.id if user else None,
            "email": user.email if user else email.strip(),
            "created_at": str(user.created_at) if user and hasattr(user, "created_at") else None
        }
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "User registered successfully", "user": user_data}
        )
    except Exception as e:
        error_msg = str(e)
        return JSONResponse(
            status_code=400,
            content={"error": error_msg}
        )

@app.post("/auth/login")
async def login(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid or missing JSON body"}
        )
        
    if not isinstance(data, dict):
        return JSONResponse(
            status_code=400,
            content={"error": "Request body must be a JSON object"}
        )

    email = data.get("email")
    password = data.get("password")
    
    if not email or not isinstance(email, str) or not email.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Email and password are required"}
        )
    if not password or not isinstance(password, str) or not password.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Email and password are required"}
        )

    try:
        response = supabase.auth.sign_in_with_password({
            "email": email.strip(),
            "password": password.strip()
        })
        session = response.session
        user = response.user
        
        if not session or not session.access_token:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid login credentials"}
            )
            
        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id if user else None,
                "email": user.email if user else email.strip()
            }
        }
    except Exception:
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid login credentials"}
        )
