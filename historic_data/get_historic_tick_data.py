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
    
    
############################### 틱 차트 조회 #########################################
# TR 요청 (연속조회)

def get_tick_data(code):
    dfs = []
    df = kiwoom.block_request("opt10079",
                            종목코드 = code,
                            틱범위 = 3,
                            수정주가구분 =1,
                            output="주식틱차트조회",
                            next=0)
    dfs.append(df)
    while kiwoom.tr_remained:
        df = kiwoom.block_request("opt10079",
                            종목코드 = code,
                            틱범위 = 3,
                            수정주가구분 =1,
                            output="주식틱차트조회",
                            next=2)
        dfs.append(df)
        time.sleep(1)


    df = pd.concat(dfs)
    df = df[['체결시간','현재가','거래량']]
    return df[::-1]


df_kodex200 =  get_tick_data('069500')
df_kodexinv =  get_tick_data(114800)
df_kodex200.to_pickle('historic_data/kodex200_'+today)
df_kodexinv.to_pickle('historic_data/kodexinv_'+today)