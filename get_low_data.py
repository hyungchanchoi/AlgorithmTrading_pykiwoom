from pykiwoom.kiwoom import *
import pandas as pd
import numpy as np
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
kosdaq = kiwoom.GetCodeListByMarket(10)

for code in kospi:
    name = kiwoom.GetMasterCodeName(code)
    name_to_code[name] = code
    code_to_name[code] = name
for code in kosdaq:
    name = kiwoom.GetMasterCodeName(code)
    name_to_code[name] = code
    code_to_name[code] = name
    

############################### 전 종목 분 차트 조회 함수 #########################################
# TR 요청 (연속조회)


def one_day(temp,test_day):        
    begin = np.where( np.array(temp['체결시간']) > str(test_day))[0][0]
    end = np.where( str(test_day+1) > np.array(temp['체결시간']) )[0][-1]
    df = temp.iloc[begin-1:end]
    return df


def get_min_data(low_lists,code):
    dfs = []
    df = kiwoom.block_request("opt10080",
                            종목코드 = code,
                            틱범위 = 1,
                            수정주가구분 =1,
                            output="주식분봉차트조회",
                            next=0)
    dfs.append(df)    
    i = 0
    while kiwoom.tr_remained:
        df = kiwoom.block_request("opt10080",
                            종목코드 = code,
                            틱범위 = 1,
                            수정주가구분 =1,
                            output="주식분봉차트조회",
                            next=2)
        dfs.append(df)
        print(df['체결시간'].iloc[0][:8])
        time.sleep(3.7)
        i +=1
        if i ==1:
            break
    df = pd.concat(dfs)
    df = df[['체결시간','현재가']]
    df = df[::-1]

    for date in range(int(df['체결시간'].iloc[0][:8]),int(df['체결시간'].iloc[-1][:8])+1):
        print(date)
        if 20201231 < date < 20210101:
            continue
        temps = pd.DataFrame()
        temps = one_day(df,date)  

        if len(temps) != 0:
            temps['현재가'] = abs(pd.to_numeric(temps['현재가']))
            temps['등락률'] = (temps['현재가'] - temps['현재가'].iloc[0]) / temps['현재가'].iloc[0]
        else:
            continue

        if len(np.where(np.array(temps['등락률']) < -0.29)[0]) > 0 :
            low_lists.append((code_to_name[code],str(date)))
            print(code_to_name[code],str(date))



############################### main #########################################


print('--- start getting historic data ---')

### get data ###
if __name__ == '__main__':

    low_lists = []
    i = 1

    for code in kosdaq:
        print(code_to_name[code],'start','(',i,'/',len(kosdaq),')')

        get_min_data(low_lists,code)

        print(code_to_name[code],'completed','(',i,'/',len(kosdaq),')')
        i += 1

    print(low_lists)

    print('--- task completed --- ')
