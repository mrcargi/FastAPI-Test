from fastapi import FastAPI, Depends , HTTPException, status,APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 =  OAuth2PasswordBearer(tokenUrl="login")


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
        "password": "09876",
        
    },
        "cargi2": {
        "username" : "nico",
        "full_name": "Giovanni Angulo",
        "email" : "giova123@hotmail.com",
        "disabled": True,
        "password": "12345",
        
    },
    
    
}


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])



def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
    

    
async def current_user(token : str  = Depends(oauth2)):
    user =  search_user(token)
    if not user :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Authentication Credentials Invalid ", headers={"WWW-Authenticate": "Bearer"}) 
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User", headers={"WWW-Authenticate": "Bearer"}) 

        
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="User don't found ")  
    
    
    user = search_user_db(form.username)
    
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="Password is incorrect")  
    
    
    return {"access_token": user.username,"token_type": "bearer"}

@router.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user