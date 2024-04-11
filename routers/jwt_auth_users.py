from fastapi import FastAPI, Depends , HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime,timedelta


ALGORITHM = "HS256"

ACCESS_TOKEN_DURATION = 1

SECRET = "dfb70721b09422f29824491df0cde9d77cfd0d59643c48b230481c9ed073dcab"

router = APIRouter()

oauth2 =  OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username : str
    full_name: str
    email : str
    disabled : bool
    
class UserDB(User):
    password : str

users_db = {
    "cargi": {
        "username" : "cargi",
        "full_name": "Carlos Angulo",
        "email" : "giova123@gmail.com",
        "disabled": False,
        "password": "$2a$12$F8yIWTwBVufJF23lirYMZ.8p0pi1t.qjRfXwbCU5zvo6AUMPe1IgW",
        
    },
        "cargi2": {
        "username" : "nico",
        "full_name": "Giovanni Angulo",
        "email" : "giova123@hotmail.com",
        "disabled": True,
        "password": "$2a$12$a2uB5kMm0TMABHecJn3wceHySpLIkteGvtPyANtTnQSzLHKeMKXc6",
        
    },
    
    
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    



async def auth_user(token: str =Depends(oauth2)):
    
    exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail="Authentication Credentials Invalid ",
                              headers={"WWW-Authenticate": "Bearer"})
    
    try:
        username = jwt.decode(token,SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        
    except JWTError:
         raise exception 
    
    return search_user(username)


async def current_user(user : User = Depends(auth_user)):

    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User", headers={"WWW-Authenticate": "Bearer"}) 

        
    return user

    

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="User don't found ")  
    
    
    user = search_user_db(form.username)
    
    crypt.verify(form.password,user.password)
    
    if not  crypt.verify(form.password,user.password):
        raise HTTPException(status_code=400, detail="Password is incorrect")  
    
    #expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION) manera para dictar que despues de un minuto tu validacion va a expirar 
    
    access_token = {"sub":user.username ,"exp":datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
    return {"access_token":jwt.encode(access_token,SECRET,algorithm=ALGORITHM),"token_type": "bearer"}

@router.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user