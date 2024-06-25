from typing_extensions import Annotated
from fastapi import Request,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
import time
import jwt
from decouple import config

JWT_KEY=config("secret")
JWT_ALGO=config("algorithm")
CUserID=0
CVendorID=0
CDBConnectionstring=""
CDbName=""

class jwtBearer(HTTPBearer):
    def __init__(self,auto_error: bool = True):
        super(jwtBearer,self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) :
        credentails: HTTPAuthorizationCredentials=await super(jwtBearer,self).__call__(request)
        if credentails:            
            if not credentails.scheme=="Bearer":                
                raise HTTPException(status_code=403,detail="Invalid or Expired Token ..!")
            if  (jwtBearer.verify_jwt(credentails.credentials)== False):
                raise HTTPException(status_code=403,detail="Invalid or Expired Token ..!")
            return credentails.credentials
        else:            
            raise HTTPException(status_code=403,detail="Invalid or Expired Token ..!")
    
    def verify_jwt(jwtToken:str):        
        isTokenValid:bool=False
        payload=jwtBearer.decodeJWT(jwtToken)
        if payload:
            global CUserID
            global CVendorID
            global CDBConnectionstring
            global CDbName
            CUserID=payload['UserID']
            CVendorID=payload['VendorID']
            CDBConnectionstring=payload['ConnectionString']
            CDbName=payload['DbName']
            print('payload',CDBConnectionstring)
            isTokenValid=True
        print(isTokenValid)
        return isTokenValid

    def decodeJWT(token:str):
        try:
          decode_token=jwt.decode(token,JWT_KEY,algorithm=JWT_ALGO)
          return decode_token if decode_token['expiry']>=time.time() else None
        except:
          return None