from pydantic import BaseModel,Field

class Login(BaseModel):
    LoginID:str
    PassWord:str

class UserAddEditInput(BaseModel):
    UserID:int | None= Field(default=0)
    LoginID:str  | None= Field(default="")
    Password:str | None= Field(default="")
    UserName:str | None= Field(default="")
    VendorID:int | None= Field(default=0)
    IsActive:bool| None= Field(default=True)


class GetUserInput(BaseModel):
    VendorID:int    
    UserID:int
    
    
class CardandChartInput(BaseModel):
    strBranch:str | None= Field(default="")
    strCompanyID:str | None= Field(default="")
    strState:str| None= Field(default="")
    strCity:str| None= Field(default="")
    strItem:str| None= Field(default="")
    strSubItem:str| None= Field(default="")
    strItemGroup:str| None= Field(default="")
    strRegionID:str| None= Field(default="")
    strItemSubitem:str| None= Field(default="")
    strPurchaseParty:str| None= Field(default="")
    strSalesParty:str| None= Field(default="")
    strSaleman:str| None= Field(default="")
    strProduct:str| None= Field(default="")
    strDesignCodeID:str| None= Field(default="")
    strDesignCatalogue:str| None= Field(default="")
    strSaleAging:str| None= Field(default="")        
    FromDate:str| None= Field(default="")
    ToDate:str| None= Field(default="")
    strMetalType:str| None= Field(default="")
    strDayBook:str| None= Field(default="")
    PageNo:int| None= Field(default=1)
    PageSize:int| None= Field(default=10)
    SortBy:str|None= Field(default="wt")
    SortByLabel:str|None= Field(default="")
    Search:str| None= Field(default="")
    Grouping:str| None= Field(default="")
    strMonth:str| None= Field(default="")
    strFinYear:str| None= Field(default="")
    Unity:str| None=Field(default="G")