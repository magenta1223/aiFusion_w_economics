from copy import deepcopy
import pandas as pd
import re
from metric import *
import numpy as np

def toarray(_str):
    _str = re.sub(" +", " ", _str).replace("\n", "").replace(",", "").replace("[", "").replace("]", "").strip().split(" ")

    return np.array([ float(s)  for s in _str])


def _pivot(nullTable, altTable, metric = "RMSFE"):
    # RMSFE : relative error of base model's error against alternative model's error.
    # base model's error / alternative model's error
    # when larger than 1, it implies that alternative one is better (smaller error)     

    assert metric in ['RMSFE', "CW"], "Invalid mode."

    if metric == "RMSFE":
        nullTable['relativeError'] = nullTable['valError_RMSE'] / altTable['valError_RMSE']

        # to pivot table
        pivoted_0 =  nullTable.pivot(index = ["targetArea", "targetHorizon"] , columns = ["slidingWindow"], values = "relativeError").reset_index(level= 1)
        return pivoted_0.pivot(columns= ['targetHorizon'])
    else:
        nullTable['alt_pred'] = altTable['predictions']
        nullTable['clark_west'] = nullTable.apply(lambda x: clarkwest(x['predictions'], x['alt_pred'], x['targets'])[-1], axis = 1)

        # to pivot table
        pivoted_0 =  nullTable.pivot(index = ["targetArea", "targetHorizon"] , columns = ["slidingWindow"], values = "clark_west").reset_index(level= 1)
        return pivoted_0.pivot(columns= ['targetHorizon'])       

def pivot():

    rawTables = pd.read_csv("./results.csv")[['targetHorizon', 'nDistrict', 'mode', 'slidingWindow', 'targetArea', 'valError_RMSE', 'model', 'predictions', 'targets']]

    # nan process
    #rawTables['EPU'] = rawTables['EPU'].apply(lambda x: "Base" if x != x else x)
    rawTables['predictions'] = rawTables['predictions'].apply(toarray)
    rawTables['targets'] = rawTables['targets'].apply(toarray)

    for nDisctrict in [8, 9]:

        for model in rawTables['model']:
            
            # table = rawTables.loc[(rawTables["nDistrict"] == nDisctrict) & (rawTables['model'] == model)]

            # base = table.loc[table['EPU'] == "Base"].reset_index(drop=True)
            # own = table.loc[table['EPU'] == "Own"].reset_index(drop=True)
            # all = table.loc[table['EPU'] == "All"].reset_index(drop=True)
        
            # # RMSFE 
            
            # # compare with base & own SV
            # _pivoted = _pivot(base, own, "RMSFE")
            # _pivoted = _pivoted.reset_index()
            # _pivoted.index = pd.Series(["Base vs. Base + own EPU"] * len(_pivoted), name = "Model Combination")

            # pivoted = _pivoted
            
            # # compare with own SV & all SVs
            # _pivoted = _pivot(own, all, "RMSFE")
            # _pivoted = _pivoted.reset_index()
            # _pivoted.index = pd.Series(["Base + own EPU vs. Base + all EPUs"] * len(_pivoted), name = "Model Combination")

            # pivoted = pd.concat([pivoted, _pivoted], axis = 0)

            # pivoted.to_csv(f"./results_pivot_{nDisctrict}_{model}_RMSFE.csv")
            
            # # Clark & West

            # # compare with base & own SV
            # _pivoted = _pivot(base, own, "CW")
            # _pivoted = _pivoted.reset_index()
            # _pivoted.index = pd.Series(["Base vs. Base + own EPU"] * len(_pivoted), name = "Model Combination")

            # pivoted = _pivoted
            
            # # compare with own SV & all SVs
            # _pivoted = _pivot(own, all, "CW")
            # _pivoted = _pivoted.reset_index()
            # _pivoted.index = pd.Series(["Base + own EPU vs. Base + all EPUs"] * len(_pivoted), name = "Model Combination")

            # pivoted = pd.concat([pivoted, _pivoted], axis = 0)

            # pivoted.to_csv(f"./results_pivot_{nDisctrict}_{model}_CW.csv")

            # table = rawTables.loc[(rawTables["nDistrict"] == nDisctrict) & (rawTables['model'] == model)]

            # base = table.loc[table['mode'] == "base"].reset_index(drop=True)
            # alternative = table.loc[table['mode'] == "alternative"].reset_index(drop=True)
            
        
            # # RMSFE 
            
            # # compare with base & own SV
            # _pivoted = _pivot(base, alternative, "RMSFE")
            # _pivoted = _pivoted.reset_index()
            # _pivoted.index = pd.Series(["Base vs. Base + own EPU"] * len(_pivoted), name = "Model Combination")

            # pivoted = _pivoted
            
            # pivoted.to_csv(f"./results_pivot_{nDisctrict}_{model}_RMSFE.csv")
            
            # Clark & West

            # compare with base & own SV
            # _pivoted = _pivot(base, alternative, "CW")
            # _pivoted = _pivoted.reset_index()
            # _pivoted.index = pd.Series(["Base vs. Base + own EPU"] * len(_pivoted), name = "Model Combination")

            # pivoted = _pivoted


            # pivoted.to_csv(f"./results_pivot_{nDisctrict}_{model}_CW.csv")

            table = rawTables.loc[(rawTables["nDistrict"] == nDisctrict) & (rawTables['model'] == model)]
            for metric in ["RMSFE", "CW"]:
                base = None
                modes = table['mode'].unique()
                pivoted = pd.DataFrame({})

                for i in range(len(modes)-1):
                    if base is None:
                        base = table.loc[table['mode'] == modes[i]].reset_index(drop=True)
                    alternative = table.loc[table['mode'] == modes[i+1]].reset_index(drop=True)

                    _pivoted = _pivot(base, alternative, metric)
                    _pivoted = _pivoted.reset_index()
                    _pivoted.index = pd.Series([f"{modes[i]} vs. {modes[i+1]}"] * len(_pivoted), name = "Model Combination")

                    pivoted = pd.concat([pivoted, _pivoted], axis = 0)
                    
                pivoted.to_csv(f"./results_pivot_{nDisctrict}_{model}_{metric}.csv")
