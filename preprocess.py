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