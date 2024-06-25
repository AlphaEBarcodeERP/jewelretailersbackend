from decouple import config
import pyodbc 
from enum import Enum
from Entity.DTO import WsInput
from Services import jwtBearer

server=config('dbconnection')
database=config("DBName")
username=config("DBUser")
password=config("DBPass")
password2="Garment"


class Connection(Enum):
    LiveConnection=f'DRIVER=ODBC Driver 18 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;Encrypt=no;Connection Timeout=30;'    
    Connection=f'DRIVER=SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password};'
   
   
   
DBLive =False


DBConnection =Connection.LiveConnection

def DBSelection():
    connection =""
    if(DBLive == True):
        if(jwtBearer.CDBConnectionstring !=""):
            connection=(f'DRIVER=ODBC Driver 18 for SQL Server;SERVER={jwtBearer.CDBConnectionstring};DATABASE={jwtBearer.CDbName};UID={username};PWD={password2};TrustServerCertificate=yes;Encrypt=no;Connection Timeout=30;')
        else:
            connection=Connection.LiveConnection.value
    else:
        print(jwtBearer.CDbName)
        if(jwtBearer.CDBConnectionstring !=""):            
            connection=(f'DRIVER=SQL Server;SERVER={jwtBearer.CDBConnectionstring};DATABASE={jwtBearer.CDbName};UID={username};PWD={password2};')
        else:
            connection=Connection.Connection.value    
            # print(connection,'..')
    return connection

def spParam(input):
    newParam=""    
    result=""
    try:
        for i in input:
            print(i)
            if(type(i[1]) is int):
                if(i[1] > 0):              
                    newParam+=f"@{i[0]}={i[1]},"                    
            elif(type(i[1]) is str):
                if(i[1]!=""):
                    newParam+=f"@{i[0]}='{i[1]}',"                    
            elif(type(i[1]) is bool):
                if(i[1]==False or i[1]==True):
                    newParam+=f"@{i[0]}={i[1]},"                            
        result=','.join([s for s in newParam.split(',') if s])
    except Exception as e:        
        print("Param Method Error :- ",e)    
    return result

def ExecuteNonQuery(input,spname,MethodNname):    
    param=""
    param=spParam(input)  
    print(param)  
    ID=0
    drivers = [item for item in pyodbc.drivers()]
  
    wconnection=pyodbc.connect(DBSelection())
  
    try:
        cursor=wconnection.cursor()             
        cursor.execute(f"EXEC {spname} {param}")        
        rows = cursor.fetchone() 
        print(rows)
        ID=rows[0]        
        cursor.commit()
    except Exception as e:        
        print(MethodNname + 'Error :- ',e)
        print('SQL Query',f"EXEC {spname} {param}")
        print('driver',drivers)
        cursor.rollback()   
    finally:
        cursor.close()
        wconnection.close()
        jwtBearer.CDBConnectionstring=''
    return ID

def ExecuteDataReader(param,spname,MethodNname):    
    key_value_pairs=[]
    drivers = [item for item in pyodbc.drivers()]     
    print(DBSelection()) 
    print(drivers)
    connection=pyodbc.connect(DBSelection())
    
    print(connection)
    try:
        cursor=connection.cursor()       
        print(f"EXEC {spname} {param}")            
        cursor.execute(f"EXEC {spname} {param}")
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()  
        
        for row in rows:
            key_value_pairs.append(dict(zip(columns, row)))        
        cursor.close()
        connection.close()
    except Exception as e:
        print(MethodNname + 'Error :- ',e)
        print('SQL Query',f"EXEC {spname} {param}")
        print('driver',drivers)
        connection.close()
    return key_value_pairs

def  CommonParam(input:WsInput.CardandChartInput):
    param=""
    if(input.strBranch!=''):
        param +=f" @strBranchID='{input.strBranch}',"
    if(input.strCity!=''):
        param +=f" @strCity='{input.strCity}',"
    if(input.strDayBook!=''):
        param +=f" @strDayBookID='{input.strDayBook}',"
    if(input.strDesignCatalogue!=''):
        param +=f" @strDesignCatalogue='{input.strDesignCatalogue}',"
    if(input.FromDate!=''):
        param +=f" @FromDate='{input.FromDate}',"
    if(input.ToDate!=''):
        param +=f" @ToDate='{input.ToDate}',"
    if(input.strItem!=''):
        param +=f" @strItemID='{input.strItem}',"
    if(input.strSubItem!=''):
        param +=f" @strSubItemID='{input.strSubItem}',"
    if(input.strItemGroup!=''):
        param +=f" @strItemGroupID='{input.strItemGroup}',"
    if(input.strItemSubitem!=''):
        param +=f" @strItemSubitemID='{input.strItemSubitem}',"
    if(input.strMetalType!=''):
        param +=f" @strMetalType='{input.strMetalType}',"
    if(input.strPurchaseParty!=''):
        param +=f" @strPurchaseParty='{input.strPurchaseParty}',"
    if(input.strProduct!=''):
        param +=f" @strProductID='{input.strProduct}',"
    if(input.strSaleman!=''):
        param +=f" @strSalemanID='{input.strSaleman}',"
    if(input.strSaleAging!=''):
        param +=f" @strSaleAging='{input.strSaleAging}',"
    if(input.strSalesParty!=''):
        param +=f" @strSalesParty='{input.strSalesParty}'," 
    if(input.strRegionID!=''):
        param +=f" @strRegionID='{input.strRegionID}',"         
    if(input.strMonth!=''):
        param +=f" @strMonth='{input.strMonth}',"
    if(input.strFinYear!=''):
        param +=f" @strFinYear='{input.strFinYear}',"  
    if(input.strState!=''):
        param +=f" @strState='{input.strState}'"
    else:
        param = param[:len(param)-1]
    
    return param