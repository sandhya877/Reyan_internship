from datetime import datetime, timedelta 
from typing import Annotated, Union, Optional

from fastapi import Depends, FastAPI, HTTPException, status,Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Annotated
from datetime import datetime, timezone, timedelta
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from rback_config import *
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
auth_scheme = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}
app=FastAPI()

class Token(BaseModel):
    access_token: str
    token_type: str

class Document(BaseModel):
    name: str
    author: str
class TokenData(BaseModel):
    username: Union[str, None] = None
    role: Optional[str] = None  # Add a role attribute


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    role: Optional[str] = None  # Add a role attribute

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
   
    role: Optional[str] = None  # Add a role attribute

class UserSignup(UserCreate):
    confirm_password: str

class Document(BaseModel):
    title:str
    content:str

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
# Your existing code...
def get_password_hash(password):
    return pwd_context.hash(password)

@app.post("/signup", response_model=User)
async def signup(user: UserSignup):
    # Check if the passwords match
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )

    # Check if the username is already taken
    existing_user = get_user(fake_users_db, username=user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create user data
    user_data = user.dict(exclude={'password', 'confirm_password'})
    user_data['hashed_password'] = hashed_password

    # Save user data to the database
    fake_users_db[user.username] = user_data

    # Return the created user
    return user_data



def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "role": data.get("role", "user")})  
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(authorization: str = Header(...)):
    print(authorization)
    if not authorization or not authorization.startswith("Bearer "):
        # If no Authorization header is provided or it doesn't start with "Bearer ", return a default user
        return {"username": "anonymous", "role": "guest"}

    token = authorization.split()[1]  # Extract token part after "Bearer "
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        expiry_time = payload.get("exp")
        if expiry_time is None or expiry_time < datetime.now(timezone.utc).timestamp():
            raise credentials_exception

        return {"username": username, "role": payload.get("role", "user")}
    except JWTError:
        raise credentials_exception

    
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def decode_access_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload



async def get_current_user(authorization: str = Header(...)):
    print(authorization)
    if not authorization or not authorization.startswith("Bearer "):
        # If no Authorization header is provided or it doesn't start with "Bearer ", return a default user
        return {"username": "anonymous", "role": "guest"}

    token = authorization.split()[1]  # Extract token part after "Bearer "
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        username: str = payload.get("username")
        role: str=payload.get("role")
        if username is None:
            raise credentials_exception

        expiry_time = payload.get("exp")
        if expiry_time is None or expiry_time < datetime.now(timezone.utc).timestamp():
            raise credentials_exception

        return {"username": username, "role": payload.get("role")}
    except JWTError:
        raise credentials_exception



@app.post("/signup", response_model=User)
async def signup(user: UserSignup):
    # Check if the passwords match
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )

    # Check if the username is already taken
    existing_user = get_user(fake_users_db, username=user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create user data
    user_data = user.dict(exclude={'password', 'confirm_password'})
    user_data['hashed_password'] = hashed_password

    # Save user data to the database
    fake_users_db[user.username] = user_data

    # Return the created user
    return user_data


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.dict(), expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    # Use the current_user directly without expecting it as a parameter
    return current_user
documents=[]
@app.post('/document')
def create_document(document:Document,current_user:User=Depends(get_current_user)):
    try:
        print(current_user)
        print(FastApiRBACMaster().RBAC([ROLES.MODERATOR,ROLES.ADMIN],current_user["role"]) == True)
        if FastApiRBACMaster().RBAC([ROLES.MODERATOR,ROLES.ADMIN],current_user["role"]) == True:
            documents.append(document)
            print(document)
            return document
    except:
        return JSONResponse(
            status_code=401,
            content={"message": "UnAuthorized Access"},
        )

@app.get('/documents',)
def all_documents():
    return documents