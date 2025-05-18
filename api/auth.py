from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-for-development")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Router
router = APIRouter()

# Models
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        print(f"User {username} not found in DB")
        return False
    if not verify_password(password, user.hashed_password):
        print(f"Password verification failed for {username}")
        return False
    print(f"User {username} authenticated successfully")
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Initialize with a test user
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "hashed_password": get_password_hash("testpassword"),
        "disabled": False
    }
}

# Routes
@router.post("/register", response_model=User)
def register_user(user: UserCreate):
    print(f"Registration attempt for username: {user.username}")
    print(f"Received user data: {user.dict()}")
    
    # Check if username already exists
    if user.username in fake_users_db:
        print(f"Username {user.username} already exists")
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # Hash the password
    hashed_password = get_password_hash(user.password)
    
    # Store user in database
    user_data = user.dict()
    user_data.pop("password")  # Remove raw password
    user_data["hashed_password"] = hashed_password
    user_data["disabled"] = False
    
    fake_users_db[user.username] = user_data
    print(f"User {user.username} successfully registered")
    print(f"Current users in DB: {list(fake_users_db.keys())}")
    
    return user_data

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"Login attempt with username: {form_data.username}")
    print(f"Available users in DB: {list(fake_users_db.keys())}")
    
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        print(f"Authentication failed for {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    print(f"Login successful for {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# Debug endpoint - remove in production
@router.get("/debug/users")
async def debug_users():
    # Return just the usernames for debugging
    return {"users": list(fake_users_db.keys()), "count": len(fake_users_db)}

# Test registration with explicit data for debugging
@router.post("/debug/register")
async def debug_register():
    test_user = {
        "username": "debuguser",
        "password": "password123",
        "email": "debug@example.com",
        "full_name": "Debug User"
    }
    print(f"Debug registration with data: {test_user}")
    
    # Create a UserCreate model
    try:
        user_create = UserCreate(**test_user)
        print(f"Validation successful: {user_create.dict()}")
        return {"status": "valid", "data": user_create.dict(exclude={"password"})}
    except Exception as e:
        print(f"Validation error: {str(e)}")
        return {"status": "invalid", "error": str(e)}