
from Crypto.Cipher import AES
from DBConnection import SQLManager
from io import BytesIO
import base64
import time
from Crypto.Hash import SHA256
import jwt
from fastapi import HTTPException
# import pprp.crypto
from Crypto import Random
from Entity.DTO.WsInput import Login,UserAddEditInput,GetUserInput
from Entity.DTO.WsResponse import LoginResult,AuthenticationResult
from decouple import config

JWT_KEY=config("secret")
JWT_ALGO=config("algorithm")
ENCRYPTION_ALGORITHM_NAME = 'Rijndael'
ENCRYPTION_INIT_VECTOR = '!#@%IVAPO0SP&UHK'
ENCRYPTION_KEY = 'T@#r$t~145S^$%^&*()_+'
ENCRYPTION_KEY_BYTES = 16 

# def decrypt(value):
#     memory_stream_in = BytesIO()
#     memory_stream_out = BytesIO()
#     byte_buffer = bytearray(2048)
#     result = ''
#     try:
#         # Write base64 decoded value to input memory stream
#         memory_stream_in.write(base64.b64decode(value))
#         memory_stream_in.seek(0)

#         # Create symmetric algorithm (AES) with IV and key
#         symmetric_algorithm = AES.new(
#             GetKey(ENCRYPTION_KEY),
#             AES.MODE_CBC,
#             ENCRYPTION_INIT_VECTOR.encode('utf-8')
#         )

#         # Create crypto stream
#         crypto_stream = AESStream(memory_stream_in, symmetric_algorithm)

#         # Read and decrypt data
#         while True:
#             value_length = crypto_stream.readinto(byte_buffer)
#             if value_length == 0:
#                 break
#             memory_stream_out.write(byte_buffer[:value_length])

#         # Convert decrypted data to string
#         result = memory_stream_out.getvalue().decode('utf-8').rstrip('\0')
#     except Exception as e:
#         raise e
#     finally:
#         memory_stream_in.close()
#         memory_stream_out.close()
#     print(result,'decrption')
#     return result.strip()

class AESStream:
    def __init__(self, memory_stream, cipher):
        self.memory_stream = memory_stream
        self.cipher = cipher

    def readinto(self, buffer):
        chunk = self.memory_stream.read(len(buffer))
        decrypted_chunk = self.cipher.decrypt(chunk)
        buffer[:len(decrypted_chunk)] = decrypted_chunk
        return len(decrypted_chunk)

def GetKey(key):
    result_key = key[:ENCRYPTION_KEY_BYTES] if len(key) >= ENCRYPTION_KEY_BYTES else key.ljust(ENCRYPTION_KEY_BYTES, '0')
    return result_key.encode('utf-8')


def LoginServi(input:Login):
    result=LoginResult()
    if(input.LoginID == ""):
      result.Message.append("Please enter LoginID")
    elif(input.PassWord == ""):
      result.Message.append("Enter Your Password")
    if(len(result.Message)==0):
      try:
        lstresult=[]
        param=""
        param=DBConfig.spParam(input)
        lstresult=DBConfig.ExecuteDataReader(param,"WR_mstuser_GetByID","LoginServi")
        if(len(lstresult)>0):
          for row in lstresult:
            result.UserName=row
        else:
          result.HasError=True
          result.Message.append("Enter Correct LoginID and Password")
      except Exception as E:
        result.Message.append(str(E))
        result.HasError=True
    return result
  
def Authentication(input:Login):
    result=AuthenticationResult()
    if(input.LoginID == ""):
      result.Message.append("Please enter LoginID")
    elif(input.PassWord == ""):
      result.Message.append("Enter Your Password")
    if(len(result.Message)==0):
      try:
        lstresult=[]
        param=f"@LoginID='{input.LoginID}'"  
        
        lstresult=SQLManager.ExecuteDataReader(param,"WR_mstuser_GetAuth","Authentication")       
        print(lstresult,'**')      
        if(len(lstresult)>0):
          # for row in lstresult[0]:
            obj=lstresult[0]
            print('obj',input.PassWord)
            print('decrobj',decryptPass(lstresult[0]['Password']))
            if(input.PassWord==str(decryptPass(lstresult[0]['Password']))):                
                result.Token=TokenGenrater(lstresult[0])
                result.UserName=lstresult[0]['UserName']
                
            else:
              result.HasError=True
              result.Message.append("Invalid Password....!")
              
        else:
            result.HasError=True
            result.Message.append("Invalid User....!")
      except Exception as E:
        result.HasError=True
        result.Message.append(str(E))
    else:
        pass
    return result
  
def TokenGenrater(input):
      print(input,'Token Gen')
      payload={
        "UserID":input['UserID'],
        "VendorID":input['VendorID'],
        "ConnectionString":input['Connectionstring'],
        "DbName":input['DbName'],
        "expiry":time.time()+600000        
      }
      token=jwt.encode(payload,JWT_KEY,algorithm=JWT_ALGO)
      return token
    
    
def get_key(key):
    if len(key) >= ENCRYPTION_KEY_BYTES:
        print(key[:ENCRYPTION_KEY_BYTES])
        return key[:ENCRYPTION_KEY_BYTES].encode('utf-8')        
    else:
        return key.ljust(ENCRYPTION_KEY_BYTES, b'0')

def encrypt(value):
    try:
        cipher = AES.new(get_key(ENCRYPTION_KEY), AES.MODE_CBC, ENCRYPTION_INIT_VECTOR.encode('utf-8'))
       
        padded_value = value + (ENCRYPTION_KEY_BYTES - len(value) % ENCRYPTION_KEY_BYTES) * b'\0'
        ciphertext = cipher.encrypt(padded_value)
        return base64.b64encode(ciphertext).decode()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      
def encryptPass(source, encode=True):
    key = SHA256.new( str.encode(ENCRYPTION_KEY)).digest()  # use SHA-256 over our key to get a proper-sized AES key
    # IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, str.encode(ENCRYPTION_INIT_VECTOR))
    source=str.encode(source)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
       
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = str.encode(ENCRYPTION_INIT_VECTOR) + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return base64.b64encode(data).decode("latin-1") if encode else data


def decryptPass(source, decode=True):
    if decode:
        source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(str.encode(ENCRYPTION_KEY)).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, str.encode(ENCRYPTION_INIT_VECTOR))
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])    
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding].decode("utf-8")
  
  
def AddEditUser(input:UserAddEditInput):
    result=UserAddEditResult()
    if(input.LoginID==''):
        result.Message.append("LoginID is Required")
    elif(input.UserName==''):
        result.Message.append("UserName is Required")
    # elif(input.VendorID<=0):
    #     result.Message.append("VendorID is Required")    
    if(len(result.Message)==0):
        try:
          ID=0          
          input.Password=encryptPass(input.Password)
          ID=SQLManager.CDBExecuteNonQuery(input,"WR_mstUser_AddEdit","AddEditUser")
          if(ID>0):
            result.Message.append("User Detail Fill sucessfully")
          elif(ID==-1):
            result.Message.append("LoginID IS already Exists")
            result.HasError=True
          else:
            result.Message.append("Something went wrong.....")
            result.HasError=True
        except Exception as e:
            print("Error",e)
            result.HasError=True
            result.Message.append(str(e))
    else:
        result.HasError=True
    return result
  
def GetUserData(input:GetUserInput):
    result=CommanListingResult()        
    if(len(result.Message)==0):
        try:
            param=""
            if(input.VendorID>0):
                param=f"@VendorID={input.VendorID}"          
                
            if(input.UserID>0):
                param=f"@UserID={input.UserID}"
            
            result.lstResult=SQLManager.CDBExecuteDataReader(param,"WR_mstUser_GetUserData","VendorchartDetailScreen")
        except  Exception as E:                    
            result.HasError=True
            result.Message.append(str(E))
    else:
        result.HasError=True
    return result