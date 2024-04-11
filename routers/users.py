from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router  = APIRouter(tags= ["Users"])



#entity user 
class User(BaseModel):
    id : int
    name : str
    surname : str
    url : str
    age : int

users_list = [User(id=1, name = "Cargi" , surname= "Angi", url="https://youtube.com", age= 20),
              User(id=2, name = "filin" , surname= "as", url="https:facebook.com", age= 20),
              User(id=3, name = "Cargi" , surname= "Angi", url="https:twitter.com", age= 20),]

@router.get("/usersjson")
async def usersjson():
    return [{"Name":"Cargi", "surname":"Angi", "url":"youtube.com","age":20},
            {"Name":"filin", "surname":"As ","url":"facebook.com","age":24},
            {"Name":"Caca", "surname":"coca", "url":"twitter.com","age":27}]



@router.get("/users")
async def users():
    return users_list

# Path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)

# Query
@router.get("/user/")
async def user(id: int):
    return search_user(id)

    
@router.post("/user/", response_model=User ,  status_code=201)
async def user(user:User):
    if type(search_user(user.id)) ==User:
        raise   HTTPException(status_code=204, detail="El Usuario no existe")  #correct form to show errors

    else:    
        users_list.append(user)    
        return user

    
    
    
@router.put("/user/")
async def user(user: User):
    
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    
    if not found:
        return {"Error":"User has not been update "}
    
    else:
        return user
            
@router.delete("/user/{id}")
async def user(id:int):
    
    found  = False
    
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            
    if not found:
        return {"Error":"User has not been eliminate"} 

      





def search_user(id : int):
    users  = filter(lambda user:user.id== id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error":"User doesn't exist"}
    