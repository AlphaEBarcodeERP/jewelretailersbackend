import uvicorn
from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from Controller import Login,SalesEfficiency
# from Controller import StockToSalesController,MinStockController,ScheduleController,DynamicController,DashboardCard,DashboardChart,DashboardFilter,CommonController
import os
from fastapi.staticfiles import StaticFiles
from Services.jwtBearer import jwtBearer
app=FastAPI()


app.include_router(Login.LoginController,prefix='/Login')
app.include_router(SalesEfficiency.Chart,prefix='/SalesChart', dependencies=[Depends(jwtBearer())])
origins=['*']
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=['*'],allow_headers=['*'],)

FilePath="Utility/Logfile"
path="Utility/Image"
PDFPath="Utility/PDF"

if(os.path.exists(FilePath)):
    pass
else:
    os.makedirs(FilePath)

if(os.path.exists(path)):
    pass
else:
    os.makedirs(path)
    
if(os.path.exists(PDFPath)):
    pass
else:
    os.makedirs(PDFPath)

app.mount("/image", StaticFiles(directory="Utility/Image"), name="image")
app.mount("/PDF", StaticFiles(directory="Utility/PDF"), name="PDF")
app.mount("/Logfile", StaticFiles(directory="Utility/Logfile"), name="Logfile")
    

@app.post("/Demo",dependencies=[Depends(jwtBearer())])
def Demo():
    return{"msg":"Welcome to Fast"}