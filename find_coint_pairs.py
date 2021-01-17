##### 대신증권 연결 확인
import win32com.client

instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
print(instCpCybos.IsConnect)

import pandas as pd
import numpy as np
import math
from datetime import datetime,timedelta
import time
today = datetime.today().strftime("%Y%m%d") 


############ CYBOS API CHART METHOD ##################
def CheckVolumn(instStockChart, code,finish, start):
    # SetInputValue
    instStockChart.SetInputValue(0, code)
    instStockChart.SetInputValue(1, ord('1'))
    instStockChart.SetInputValue(2,finish )
    instStockChart.SetInputValue(3,start)
    instStockChart.SetInputValue(4, 60)
    instStockChart.SetInputValue(5, 8)
    instStockChart.SetInputValue(6, ord('D'))
    instStockChart.SetInputValue(9, ord('1'))

    # BlockRequest
    instStockChart.BlockRequest()

    # GetData
    volumes = []
    numData = instStockChart.GetHeaderValue(3)
    for i in range(numData):
        volume = instStockChart.GetDataValue(0, i)
        volumes.append(volume)
    if len(volumes) == 0:
        return 0
    
    # Calculate average volume
    averageVolume = (sum(volumes) - volumes[0]) / (len(volumes) -1)

    if(averageVolume > 1000000 ):
        return 1
    else:
        return 0

# 분 차트 받아오기
def get_min(code,today,start,time):  # 종목, 기간, 오늘, 시점, 분, 시간간격
#     print(start, today)
    instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    instStockChart.SetInputValue(0, code )
    instStockChart.SetInputValue(1, ord('1'))
    instStockChart.SetInputValue(2, today)
    instStockChart.SetInputValue(3, start)
    # instStockChart.SetInputValue(4, 1000)
    instStockChart.SetInputValue(5, (0,1,5))
    instStockChart.SetInputValue(6, ord('m'))  # 'D':일 'm' : 분, 'T' : 틱
    instStockChart.SetInputValue(7, time)      # 데이터 주기
    instStockChart.SetInputValue(9, ord('1'))
    instStockChart.SetInputValue(10, 3)

    instStockChart.BlockRequest()

    numData = instStockChart.GetHeaderValue(3)
    numField = instStockChart.GetHeaderValue(1) 

    temp = {}
    for i in range(numData):
        temp[str(instStockChart.GetDataValue(0, i)) +'.'+ str(instStockChart.GetDataValue(1, i))] = [instStockChart.GetDataValue(2, i)]
    temp = pd.DataFrame(temp).transpose()
    temp.index.names = ['time']
    return temp

def merge(temp,data ):
    temp =  pd.merge(left = temp , right = data, how = "inner", on = "time")
    return temp


#############  MAIN ##################
if __name__ == '__main__':

    finish = int(input('What Date to search?(YYYYMMDD) :'))
    start = finish - 10000

    ############ SAVE CODE, NAME AS DICTIONARY ##################
    instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
    codeList = instCpCodeMgr.GetStockListByMarket(1)

    code_to_name = {}
    name_to_code = {}
    for code in codeList:
        name = instCpCodeMgr.CodeToName(code)
        code_to_name[code] = name
        name_to_code[name] = code


    ############ GET CODE WHICH EXCEED CERTAIN VOLUME ##################
    instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
    codeList = instCpCodeMgr.GetStockListByMarket(1)

    buyList = []
    buyName= []

    i = 0 ; j= 0
    start = time.time()

    for code in codeList:        
        j+=1
        if CheckVolumn(instStockChart, code,finish,start) == 1:
            buyList.append(code)
            buyName.append(code_to_name[code])
            print(code, code_to_name[code],' ----',j,'/',len(codeList))     
        i+=1
        if  i > 58  and time.time() - start < 15:
            time.sleep( 16 - (time.time() - start))
            start = time.time()
            i=0

    ############ GET MIN DATA ##################
    buyDict = {}

    for code in buyList : #buyList
        buyDict[code] = [np.log(get_min(code,finish,start,1))]


    ############ SAVE AS DATAFRAME ##################
    data = pd.DataFrame(buyDict[buyList[0]][0])
    buyCode = buyList

    for code in buyList[1:] :
        temp = buyDict[code][0]
        if  len(merge(data,temp)) < 6600 or int(temp.isnull().sum()) > 0:
            buyCode.remove(code)  
            buyName.remove(code_to_name[code])
            continue        
        data = merge(data,temp)

    data.columns = buyName

    data.to_pickle('data_coint_pairs.xlsx')