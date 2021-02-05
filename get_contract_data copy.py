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
    
    
############################### daily 종목 #########################################

codes = ['삼성전자','SK하이닉스','LG화학','삼성전자우','NAVER','삼성바이오로직스','현대차','삼성SDI','셀트리온','기아차','TIGER TOP10']


############################### 체결강도 조회 함수 #########################################
# TR 요청 (연속조회)

def get_contract_data(code):
    dfs = []
    df = kiwoom.block_request("opt10046",
                            종목코드 = code,
                            틱범위 = 1,
                            체결강도구분 =1,
                            output="체결강도시간별",
                            next=0)
    dfs.append(df)
    while kiwoom.tr_remained:
        df = kiwoom.block_request("opt10046",
                            종목코드 = code,
                            틱범위 = 1,
                            수정주가구분 =1,
                            output="체결강도시간별",
                            next=2)
        dfs.append(df)
        print(df['체결시간'].iloc[0])
        time.sleep(1)
    df = pd.concat(dfs)
    df = df[['체결시간','전일대비','등락율','체결강도','체결강도5분','체결강도20분','체결강도60분']]
    return df[::-1]



############################### main #########################################

### get data ###

print('--- start getting strength data ---')

for name in codes:
    df =  get_contract_data(name_to_code[name])
    df.to_pickle('strength/'+ name +'(S)_'+today)
    print(name,'completed')

print('--- task completed --- ')
