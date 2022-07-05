import pandas as pd
#preprocess 

from config import CONFIG
def refineData(df):
    col = df.columns[0]
    headerRow = df.loc[ df[col] == "date" ].index[0]
    refined = df.iloc[headerRow + 1 : , : ].reset_index(drop = True)
    refined.columns = df.iloc[headerRow, :]
    return refined


def getData(nDisctrict, targetVariable, regionVariantFeatures = []):
    assert nDisctrict in [8, 9], "Invalid number of District. Choose among 8 and 9."
    

    if nDisctrict == 9:
        f = pd.ExcelFile("./data/Composite_panel_9_districts_cut_M.xlsx")
    else:
        f = pd.ExcelFile("./data/Composite_panel_8_bea_region_cut_M.xlsx")
    
    result = None
    for name in f.sheet_names:
        df = refineData(pd.read_excel(f, name))
        df = df[['date', targetVariable] + regionVariantFeatures]
        df.columns = ['date'] + [ f'{col}_{name}'  for col in df.columns[1:]]
        
        if result is not None:
            result = pd.merge(result, df, on = "date")
        else:
            result = df

    return result


def preprocess():
    baseRate = refineData(pd.read_excel("./data/Base Rate & Shadow Rate_M_.xlsx"))[['date', 'Federal Funds Rate']]
    CPI = refineData(pd.read_excel("./data/Controls_M.xlsx"))
    CPI.columns = ["date", "CPI", "logCPI", "logCPIDiff", "NFCI", "TMU", "TFU", "TRU"]
    CPI = CPI[["date"] + CONFIG['commonFeatures']]

    data = getData(8, CONFIG['targetFeature'], CONFIG['regionVariantFeatures'])
    data = pd.merge(baseRate, data, on = "date")
    data = pd.merge(CPI, data, on = "date")
    data.to_csv("./data/mergedData8.csv", encoding= "utf-8", index = False)

    data = getData(9, CONFIG['targetFeature'], CONFIG['regionVariantFeatures'])
    data = pd.merge(baseRate, data, on = "date")
    data = pd.merge(CPI, data, on = "date")
    data.to_csv("./data/mergedData9.csv", encoding= "utf-8", index = False)

