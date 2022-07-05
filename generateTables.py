import pandas as pd

def _pivot(baseSV, alternativeSV):
    # RMSFE : relative error of alternative model's error against base model's error.
    # base model's error / alternative model's error
    # when larger than 1, it implies that alternative one is better (smaller error)     
    baseSV['relativeError'] = baseSV['valError_RMSE'] / alternativeSV['valError_RMSE']
    # to pivot table
    pivoted_0 =  baseSV.pivot(index = ["targetArea", "targetHorizon"] , columns = ["slidingWindow"], values = "relativeError").reset_index(level= 1)
    return pivoted_0.pivot(columns= ['targetHorizon'])

def pivot():

    rawTables = pd.read_csv("./results.csv")[['targetHorizon', 'nDistrict', 'EPU', 'slidingWindow', 'targetArea', 'valError_RMSE']]

    # nan process
    rawTables['EPU'] = rawTables['EPU'].apply(lambda x: "Base" if x != x else x)


    for nDisctrict in [8, 9]:
        table = rawTables[rawTables["nDistrict"] == nDisctrict]

        base = table.loc[table['EPU'] == "Base"].reset_index(drop=True)
        own = table.loc[table['EPU'] == "Own"].reset_index(drop=True)
        all = table.loc[table['EPU'] == "All"].reset_index(drop=True)

        # compare with base & own SV
        _pivoted = _pivot(base, own)
        _pivoted = _pivoted.reset_index()
        _pivoted.index = pd.Series(["Base vs. Base + own EPU"] * len(_pivoted), name = "Model Combination")

        pivoted = _pivoted
        
        # compare with own SV & all SVs
        _pivoted = _pivot(own, all)
        _pivoted = _pivoted.reset_index()
        _pivoted.index = pd.Series(["Base + own EPU vs. Base + all EPUs"] * len(_pivoted), name = "Model Combination")

        pivoted = pd.concat([pivoted, _pivoted], axis = 0)

        pivoted.to_csv(f"./results_pivot_{nDisctrict}.csv")
