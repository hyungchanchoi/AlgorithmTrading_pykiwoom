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

daily = ['KODEX 200','KODEX 인버스','KODEX 혁신기술테마액티브','TIGER 200','TIGER 인버스','TIGER AI코리아그로스액티브',
         'KODEX 삼성그룹','KODEX 삼성그룹밸류']

############################### 틱/분 차트 조회 함수 #########################################
# TR 요청 (연속조회)

def get_bidask_data(code):
    dfs = []
    df = kiwoom.block_request("opt10004",
                            종목코드 = code,
                            output="주식호가",
                            next=0)
    dfs.append(df)
    print(df)
    while kiwoom.tr_remained:
        df = kiwoom.block_request("opt10004",
                            종목코드 = code,
                            output="주식호가",
                            next=2)
        dfs.append(df)
        time.sleep(1)


    df = pd.concat(dfs)
    df = df[['매도최우선호가','매수최우선호가']]
    return df[::-1]
               
df = get_bidask_data('069500')
print(df)
############################### main #########################################

# command = 'continue'
# data = None
# codes = []


# ### input data type ###
# while True:   

#     data = input('data type / tick or min ? : ')
    
#     if data not in ['tick','min','daily'] :
#         print('wrong data type')
#         continue
#     else:
#         break


# ### input code name ###
# while command != 'stop':

#     name = input('종목명 :')
    
#     if name not in name_to_code.keys():
#         print('wrong name')
#         continue
#     else:
#         code = name_to_code[name]
#         codes.append(code)
#         command = input('continue or stop? : ')

# print('--- start getting historic data ---')

# ### get data ###
# if data == 'tick':
#     for code in codes:
#         df =  get_tick_data(code)
#         df.to_pickle('data analysis/'+code_to_name[code]+'(T)_'+today)
#         print(code_to_name[code],'completed')
# elif data == 'min':
#     for code in codes:
#         df =  get_min_data(code)
#         df.to_pickle('data analysis/'+code_to_name[code]+'(m)_'+today)
#         print(code_to_name[code],'completed')
# elif data == 'daily':
#     print('--- daily data ---')
#     for name in daily:
#         df1 =  get_min_data(name_to_code[daily])
#         df2 =  get_min_data(name_to_code[daily])
#         df.to_pickle('data analysis/'+name+'(m)_'+today)
#         print(name,'completed')

# print('--- task completed --- ')