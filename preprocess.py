import pandas as pd

def refineData(df):
    col = df.columns[0]
    headerRow = df.loc[ df[col] == "date" ].index[0]
    refined = df.iloc[headerRow + 1 : , : ].reset_index(drop = True)
    refined.columns = df.iloc[headerRow, :]
    return refined


def getData(nDisctrict):
    assert nDisctrict in [8, 9], "Invalid number of District. Choose among 8 and 9."

    if nDisctrict == 9:
        f = pd.ExcelFile("./data/data_panel_gdp_9district_nocon.xlsx")
    else:
        f = pd.ExcelFile("./data/data_panel_gdp_bea_nocon.xlsx")
    
    result = None
    for name in f.sheet_names:
        df = refineData(pd.read_excel(f, name))
        df = df[['date', 'STOCHVOL', 'GROWTH RATE']]
        df.columns = ['date'] + [ f'{col}_{name}'  for col in df.columns[1:]]
        
        if result is not None:
            result = pd.merge(result, df, on = "date")
        else:
            result = df

    return result


def preprocess():
    baseRate = refineData(pd.read_excel("./data/Base Rate & Shadow Rate.xlsx"))
    CPI = refineData(pd.read_excel("./data/CPI.xlsx"))
    CPI.columns = ["date", "CPI", "logCPI", "logCPIDiff"]

    data = getData(8)
    data = pd.merge(baseRate, data, on = "date")
    data = pd.merge(CPI, data, on = "date")
    data.to_csv("./data/mergedData8.csv", encoding= "utf-8", index = False)

    data = getData(9)
    data = pd.merge(baseRate, data, on = "date")
    data = pd.merge(CPI, data, on = "date")
    data.to_csv("./data/mergedData9.csv", encoding= "utf-8", index = False)

# 1) log(CPI)를 차분하면 분산이 매우 작아진다고 하셨는데 지금은 log(CPI)를 차분하는 것 외에는 마땅한 대안이 없을 것 같습니다. 그래서 우선은 랜덤포레스트 모델에서 CPI를 중요하지 않는 변수로 분류를 하는지에 따라서 값을 조정할까 합니다. 대신 Federal Funds Rate나 Growth Rate 모두 %로 하지 않고 소수점으로 변경해놓았습니다. Stochastic Volatility도 그대로 두려고 합니다. 
# 2) 주요 도시 관련해서는 데이터가 갑자기 많아져서 정리하는 데에 시간이 걸릴 것 같은데 최대한 빨리 (늦게는 수요일 오전) 보내드리도록 하겠습니다. 
# 3) sliding window 관련해서 학습가능한 데이터가 만약 줄어들게 된다면 보통 머신러닝 분야에서 어떤 방식으로 해결을 하는지 궁금한지, 어떤 방법으로 해결이 가능한지 궁금합니다. 
# 4) 교수님께서 새로운 변수를 제안하셔서 파일에 넣었습니다. "NFCI"라는 변수인데, 미국이 전반적 금융시장의 상태에 대해 정리한 인덱스입니다. 혹시 설명변수로 추가해주실 수 있을까 해서 여쭤봅니다. 
