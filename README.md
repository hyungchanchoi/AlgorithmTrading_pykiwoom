# AlgorithmTrading_pykiwoom
### COMPONENTS
### 1. GET_HISTORIC_TICK_DATA.PY 
### 2. DATA ANALYSIS
### 3. BACKTEST

# 키움 API로부터 종목 과거 틱 데이터 저장하기 - GET_HISTORIC_TICK_DATA.PY

### 터미널에서 파일 실행 시,
### 1. 주식시장 내 모든 종목 코드와, 종목명 딕셔너리 형태로 저장
### 2. 틱 데이터를 구하고자 하는 종목명 입력
###    (만약 잘못된 종목명인 경우 재입력 요구)
### 3. 종목명 입력 시, continue or stop? 입력
###    (stop인 경우, 입력한 종목에 대한 틱 데이터 저장 시작, 그 외 command일 경우 그 다음 종목명 입력)
### 4. 틱 데이터를 구하고자 하는 종목명 입력 후 stop 입력 시, 데이터 저장 문구와 함께 키움서버로부터 데이터 저장 시작
### 5. 원하는 경로로 'pickle'의 형태로 저장