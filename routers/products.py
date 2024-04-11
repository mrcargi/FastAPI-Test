from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router  = APIRouter(prefix="/products",
                    tags=["Products"], 
                    responses={404:{"message":"Not Found"}}) #con esto ya no necesito ir repitiendo y le doy contexton al router

products_list = ["producto 1","producto 1","producto 3","producto 4","producto 5" ]


@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id:int):
    return products_list[id]