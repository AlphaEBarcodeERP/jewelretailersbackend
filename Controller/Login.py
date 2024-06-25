import os
from fastapi import APIRouter,Body,Depends,HTTPException

from Entity.DTO.WsInput import Login
from Services import AuthenticationService
LoginController=APIRouter()

@LoginController.post('/login')
async def login(input:Login): 
       result=AuthenticationService.Authentication(input)
       return result