from fastapi import APIRouter,Body,Depends
from Services import SalesEfficiencyService
from Entity.DTO.WsInput import CardandChartInput
Chart=APIRouter()



@Chart.post('/GetCommanChart')
def GetCommanChart(input:CardandChartInput):
    return SalesEfficiencyService.GetCommanChart(input)

@Chart.post('/GetDetailCommanChart')
def GetDetailCommanChart(input:CardandChartInput):
    return SalesEfficiencyService.GetDetailCommanChart(input)