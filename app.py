from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import warnings
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
import jwt
from sqlalchemy import create_engine, text
from utils.utils import *


load_dotenv(".env.development") 
# TODO: There is no point in having to write the .env that needs to be accessed. This is fixed using docker. 

PORT = os.environ["PORT"]
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
URL_DB = os.environ["URL_DB"]


# Session database
engine = create_engine(URL_DB)


warnings.filterwarnings("ignore", category=DeprecationWarning)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# OAuth2PasswordBearer will be used to get the JWT token from the request header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Model User
class User(BaseModel):
    id: str
    name: str
    email: str
    role: str

# Model to get token
class TokenRequest(BaseModel):
    email: str


# Dependency to check user role
def authorize_role(required_role: list):
    async def role_verifier(user: User = Depends(get_current_user)):
        if not user.role in required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return user
    return role_verifier

# Function to verify JWT token and extract user
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return User(id=payload.get("id"),
                    name=payload.get("name"),
                    email=payload.get("email"),
                    role=payload.get("role"))
    
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Dependency to get the authenticated user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)


@app.post("/token")
async def login(request: TokenRequest):
    """
    Get token
    """

    email = request.email
    user_data = get_user_role(engine=engine, email=email)
    token = jwt.encode(user_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/user/by_id/{user_id}")
async def get_user_by_id(user_id: str, user: User = Depends(authorize_role(["user", "admin"]))):
    """
    Get user data filtered by user ID -> Can be accessed by users with "users" and "admin" role.
    """

    info_user = get_user_by_id_db(engine = engine, user_id=user_id)

    print(user)

    return info_user


@app.get("/user/by_username/{username}")
async def get_user_by_username(username: str, user: User = Depends(authorize_role(["user", "admin"]))):
    """
    Get user data filtered by username -> Can be accessed by users with role "users" and "administrators".
    """

    info_user = get_user_by_username_db(engine = engine, username=username)

    print(user)

    return info_user

@app.get("/policies/by_username/{username}")
async def get_policies_by_username(username: str, user: User = Depends(authorize_role(["admin"]))):
    """
    Get the list of policies linked to a username -> Can be accessed by users with the "administrators" role.
    """

    info_policies = get_policies_by_username_db(engine = engine, username=username)

    print(user)

    return info_policies


@app.get("/user/by_policie/{policy_id}")
async def get_policies_by_username(policy_id: str, user: User = Depends(authorize_role(["admin"]))):
    """
   # Get the user linked to a policy number -> It can be accessed by users with the "admin" role.
    """

    info_user = get_usere_by_policie_id_db(engine = engine, policy_id=policy_id)

    print(user)

    return info_user

@app.get("/")
def root():
    return {"message": "API TEST"}


# if __name__ == "__main__":
#     port = int(PORT)

#     uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True, workers=3)
#     # uvicorn.run("main:app", host="0.0.0.0", port=port, workers=3)