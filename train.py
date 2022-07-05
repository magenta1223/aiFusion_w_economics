from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from sklearn.metrics import mean_squared_error
import os
import numpy as np
from config import *
from itertools import product
from copy import deepcopy


def loadData(nDistrict):
    assert nDistrict in [8, 9], "Invalid number of district."
    
    return pd.read_csv(f"./data/mergedData{nDistrict}.csv")

def toDataFrame(dictionary):
    return pd.DataFrame({ k : [v]   for k, v in dictionary.items()})

def train(config):
    """
    Train Random Forest Regressor by given configuration.
    """
    data = loadData(config['nDistrict'])

    # Response variable
    # Explanatory Variable
    # - Stochastic Volatility

    # - CPI
    # - Base Rate
    # - NFCI

    # CF: common features shared with other areas. ["logCPIDiff", "NFCI", "TMU", "TFU", "TRU"]
    # targetFeature : GROWTH RATE / Average Urate
    EV = config['commonFeatures'] + [ f"{config['targetFeature']}_{config['targetArea']}_shifted_{i}" for i in range(config['slidingWindow'])]


    # stochatic volatility mode
    # deprecated. replaced with avg epu
    if config['EPU'] is not None:
        if config['EPU'] == "Own":
            EV += [f"Average EPU_{config['targetArea']}"]
        elif config['EPU'] == "All":
            EV += [col for col in data.columns if "Average EPU" in col]
        else:
            pass

    # - lag(1) of Growth Rate (sliding window)
    # GROWTH RATE > URate  
    for i in range(config['slidingWindow']):
        data[f"{config['targetFeature']}_{config['targetArea']}_shifted_{i}"] = data[f"{config['targetFeature']}_{config['targetArea']}"].shift(i)


    # target horizon
    # URate
    data['target'] = data[f"{config['targetFeature']}_{config['targetArea']}"].shift(- config['targetHorizon'])
    data = data.dropna()
    
    # set split. default ratio = 0.2
    valSet = int(data.shape[0] * config["test"])
    trainSet = data.iloc[:-valSet, :].reset_index(drop=True)
    valSet = data.tail(valSet).reset_index(drop=True)

    # RF regressor
    # TODO : hyper parameter tuning
    regressor = RandomForestRegressor( n_estimators= 300, verbose = 1, n_jobs= 10 )

    ## train
    regressor.fit( X= trainSet[EV], y = trainSet['target'], )

    ## predcition
    pred = regressor.predict(valSet[EV])

    ## error metric
    ## TODO : apply Clark-West test
    config['valError_RMSE'] = np.sqrt(mean_squared_error(pred, valSet['target']))
    
    # save results
    
    ## initialize
    if not os.path.exists("./results.csv"):
        toDataFrame(config).to_csv("./results.csv", index = False)
    
    ## load & save
    else:
        result = pd.read_csv("./results.csv")
        pd.concat([result, toDataFrame(config)], axis = 0).to_csv("./results.csv", index = False)


def search():
    """
    Grid search (not RF's parameter tuning)
    """
    for nDistrict in [8, 9]:
       targets = TARGETS[nDistrict]
       CONFIG["nDistrict"] = nDistrict
       for combination in product(EPU, HORIZONS, targets, WINDOWS):
           config = deepcopy(CONFIG)
           config['EPU'] = combination[0]
           config['targetHorizon'] = combination[1]
           config['targetArea'] = combination[2]
           config['slidingWindow'] = combination[3]
           train(config)