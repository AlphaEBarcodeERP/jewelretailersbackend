from pydantic import BaseModel,Field

class CommonResult:
    def __init__(self):
        self.Message = []
        self.HasError = False


class AuthenticationResult(CommonResult):
    def __init__(self):
        super().__init__()
        self.Token:str
        self.UserName:str 
        

class LoginResult(CommonResult):
    def __init__(self):
        super().__init__()
        self.UserName:str

class UserAddEditResult(CommonResult):
    def __init__(self):
        super().__init__()
        
class CommanListingResult(CommonResult):
    def __init__(self):
        super().__init__()
        self.lstResult:[]    
        
class CommanChartFilterResult(CommonResult):
    def __init__(self):
        super().__init__()
        self.lstResult:[] 