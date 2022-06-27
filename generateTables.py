import pandas as pd

def _pivot(baseSV, alternativeSV):
    baseSV['relativeError'] = baseSV['valError_RMSE'] / alternativeSV['valError_RMSE']
    pivoted_0 =  baseSV.pivot(index = ["target", "targetHorizon"] , columns = ["slidingWindow"], values = "relativeError").reset_index(level= 1)
    return pivoted_0.pivot(columns= ['targetHorizon'])

def pivot():

    rawTables = pd.read_csv("./results.csv")

    # nan process
    rawTables['StochVol'] = rawTables['StochVol'].apply(lambda x: "Base" if x != x else x)


    for nDisctrict in [8, 9]:
        table = rawTables[rawTables["nDistrict"] == nDisctrict]

        base = table.loc[table['StochVol'] == "Base"].reset_index(drop=True)
        own = table.loc[table['StochVol'] == "Own"].reset_index(drop=True)
        all = table.loc[table['StochVol'] == "All"].reset_index(drop=True)


        # RMSFE : relative error of alternative model's error against base model's error.
        # base model's error / alternative model's error
        # when larger than 1, it implies that alternative one is better (smaller error) 

        _pivoted = _pivot(base, own)
        _pivoted = _pivoted.reset_index()
        _pivoted.index = pd.Series(["Base vs. Base + own SV"] * len(_pivoted), name = "Model Combination")

        pivoted = _pivoted

        _pivoted = _pivot(own, all)
        _pivoted = _pivoted.reset_index()
        _pivoted.index = pd.Series(["Base + own SV vs. Base + all SVs"] * len(_pivoted), name = "Model Combination")

        pivoted = pd.concat([pivoted, _pivoted], axis = 0)

        pivoted.to_csv(f"./results_pivot_{nDisctrict}.csv")