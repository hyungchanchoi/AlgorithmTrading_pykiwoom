from pykiwoom.kiwoom import *
import pandas as pd
import time
from datetime import datetime,timedelta
today = datetime.today().strftime("%Y%m%d") 

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

state = kiwoom.GetConnectState()
if state == 0:
    print("미연결")
elif state == 1:
    print("연결완료")


############################### 종목명,종목코드 딕셔너리 #########################################
name_to_code = {}
code_to_name = {}

kospi = kiwoom.GetCodeListByMarket(0)
kodaq = kiwoom.GetCodeListByMarket(10)
etf = kiwoom.GetCodeListByMarket(8)

for code in kospi:
    name = kiwoom.GetMasterCodeName(code)
    name_to_code[name] = code
    code_to_name[code] = name
for code in kodaq:
    name = kiwoom.GetMasterCodeName(code)
    name_to_code[name] = code
    code_to_name[code] = name
for code in etf:
    name = kiwoom.GetMasterCodeName(code)
    name_to_code[name] = code
    code_to_name[code] = name
    
    
############################### 틱/분 차트 조회 #########################################
# TR 요청 (연속조회)

def get_tick_data(code):
    dfs = []
    df = kiwoom.block_request("opt10079",
                            종목코드 = code,
                            틱범위 = 1,
                            수정주가구분 =1,
                            output="주식틱차트조회",
                            next=0)
    dfs.append(df)
    while kiwoom.tr_remained:
        df = kiwoom.block_request("opt10079",
                            종목코드 = code,
                            틱범위 = 1,
                            수정주가구분 =1,
                            output="주식틱차트조회",
                            next=2)
        dfs.append(df)
        time.sleep(1)


    df = pd.concat(dfs)
    df = df[['체결시간','현재가','거래량']]
    return df[::-1]

def get_min_data(code):
    dfs = []
    df = kiwoom.block_request("opt10080",
                            종목코드 = code,
                            틱범위 = 1,
                            수정주가구분 =1,
                            output="주식틱차트조회",
                            next=0)
    dfs.append(df)
    while kiwoom.tr_remained:
        df = kiwoom.block_request("opt10080",
                            종목코드 = code,
                            틱범위 = 1,
                            수정주가구분 =1,
                            output="주식틱차트조회",
                            next=2)
        dfs.append(df)
        time.sleep(1)


    df = pd.concat(dfs)
    df = df[['체결시간','현재가','거래량']]
    return df[::-1]


############################### main #########################################

command = 'continue'
data = None
codes = []


### input data type ###
while True:   

    data = input('data type / tick or min ? : ')
    
    if data not in ['tick','min'] :
        print('wrong data type')
        continue
    else:
        break


### input code name ###
while command != 'stop':

    name = input('종목명 :')
    
    if name not in name_to_code.keys():
        print('wrong name')
        continue
    else:
        code = name_to_code[name]
        codes.append(code)
        command = input('continue or stop? : ')

print('--- start getting historic tick data ---')

### get data ###
if data == 'tick':
    for code in codes:
        df =  get_tick_data(code)
        df.to_pickle('data analysis/'+code_to_name[code]+'(T)_'+today)
        print(code_to_name[code],'completed')
elif data == 'min':
    for code in codes:
        df =  get_min_data(code)
        df.to_pickle('data analysis/'+code_to_name[code]+'(m)_'+today)
        print(code_to_name[code],'completed')

print('--- task completed --- ')
