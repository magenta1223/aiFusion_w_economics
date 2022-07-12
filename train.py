from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from sklearn.metrics import mean_squared_error
import os
import numpy as np
from config import *
from itertools import product
from copy import deepcopy
from metric import clarkwest


def loadData(nDistrict):
    assert nDistrict in [8, 9], "Invalid number of district."
    return pd.read_csv(f"./data/mergedData{nDistrict}.csv")

def toDataFrame(dictionary):
    return pd.DataFrame({ k : [v]   for k, v in dictionary.items()})

def cutoff_features(X_train, regressor, threshold):
    vars = X_train.columns
    FI = regressor.feature_importances_
    FI = [ (vars[i], FI[i])    for i in range(len(vars))]
    FI = sorted(FI, key = lambda x: x[1], reverse = True)

    cummulative = 0
    features = []
    for f, i in FI:
        cummulative += i
        features.append(f)

        if cummulative >= threshold:
            break
    return features



def getDataset(config, dropFeatures = None):
    data = loadData(config['nDistrict'])

    # commonFeatures: features shared across all the regions. ["logCPIDiff", "NFCI", "TMU", "TFU", "TRU"]
    # targetFeature : GROWTH RATE / Average Urate
    #EV = config['commonFeatures'] + [ f"{config['targetFeature']}_{config['targetArea']}_shifted_{i}" for i in range(1, config['slidingWindow'] + 1)]
    EV = [ f"{config['targetFeature']}_{config['targetArea']}_shifted_{i}" for i in range(1, config['slidingWindow'] + 1)]
    # avg epu
    # if config['EPU'] is not None:
    #     if config['EPU'] == "Own":
    #         EV += [f"Average EPU_{config['targetArea']}"]
    #     elif config['EPU'] == "All":
    #         EV += [col for col in data.columns if "Average EPU" in col]
    #     else:
    #         pass

    national_Variables = config['features']['national']
    regional_Variables = config['features']['regional']

    if national_Variables:
        EV += national_Variables
    
    if regional_Variables:
        # for var in regional_Variables:
        #     for area in TARGETS[config['nDistrict']]:
        #         EV.append( f"{var}_{area}" )
        EV += [ f"{var}_{area}"  for var in regional_Variables for area in TARGETS[config['nDistrict']]]
    

    for i in range(1, config['slidingWindow'] + 1):
        data[f"{config['targetFeature']}_{config['targetArea']}_shifted_{i}"] = data[f"{config['targetFeature']}_{config['targetArea']}"].shift(i)

    # target horizon
    data['target'] = data[f"{config['targetFeature']}_{config['targetArea']}"].shift(- config['targetHorizon'])
    data = data.dropna()

    if dropFeatures is not None:
        data = data.drop(dropFeatures, axis = 1)
    
    # set split. default ratio = 0.2
    valSet = int(data.shape[0] * config["test"])
    trainSet = data.iloc[:-valSet, :].reset_index(drop=True)
    valSet = data.tail(valSet).reset_index(drop=True)

    return trainSet[EV], trainSet['target'], valSet[EV], valSet['target']

def train(config):
    """
    Train Random Forest Regressor by given configuration.
    """
    X_train, y_train, X_val, y_val = getDataset(config)

    # RF regressor
    # TODO 
    
    # Recursive variable importance > RFCV
    # RF / ada / gradient boosting을 비교
    regressor = MODELS_DICT[config['model']](**PARAMS[config['model']])

    ## train
    regressor.fit( X= X_train, y = y_train, )

    ## predcition
    pred = regressor.predict(X_val)


    ## error metric
    ## TODO : apply Clark-West test
    config['valError_RMSE'] = np.sqrt(mean_squared_error(pred, y_val))
    config['predictions'] = pred
    config['targets'] = y_val.values.tolist()
    del config['features']
    # save results
    
    ## initialize
    if not os.path.exists(f"./results.csv"):
        toDataFrame(config).to_csv("./results.csv", index = False)
    
    else:
        ## load & save
        result = pd.read_csv("./results.csv")
        pd.concat([result, toDataFrame(config)], axis = 0).to_csv("./results.csv", index = False)


    if config['model'] == "RandomForest":
        # variable filtering by feature importance
        feature_cufoff = cutoff_features(X_train, regressor, config['threshold'])

        regressor = MODELS_DICT[config['model']](**PARAMS[config['model']])
        config['model'] = f"RF_cutoff_{config['threshold']}"

        ## train
        regressor.fit( X= X_train[feature_cufoff], y = y_train, )
        pred = regressor.predict(X_val[feature_cufoff])

        ## error metric
        config['valError_RMSE'] = np.sqrt(mean_squared_error(pred, y_val))
        config['predictions'] = pred
        config['targets'] = y_val.values.tolist()
        # save results
        
        ## initialize
        if not os.path.exists(f"./results.csv"):
            toDataFrame(config).to_csv("./results.csv", index = False)
        
        ## load & save
        else:
            result = pd.read_csv("./results.csv")
            pd.concat([result, toDataFrame(config)], axis = 0).to_csv("./results.csv", index = False)


def search():
    """
    Grid search (no RF's parameter tuning)
    """
    # for nDistrict in [8, 9]:
    #    targets = TARGETS[nDistrict]
    #    CONFIG["nDistrict"] = nDistrict
    #    for combination in product(EPU, HORIZONS, targets, WINDOWS, MODELS):
    #        config = deepcopy(CONFIG)
    #        config['EPU'] = combination[0]
    #        config['targetHorizon'] = combination[1]
    #        config['targetArea'] = combination[2]
    #        config['slidingWindow'] = combination[3]
    #        config['model'] = combination[4]
    #        train(config)

    for nDistrict in [8, 9]:
       targets = TARGETS[nDistrict]
       CONFIG["nDistrict"] = nDistrict
       for combination in product(FEATURE_DICT.keys(), HORIZONS, targets, WINDOWS, MODELS):
           config = deepcopy(CONFIG)
           config['mode'] = combination[0]
           config['features'] = FEATURE_DICT[combination[0]]
           config['targetHorizon'] = combination[1]
           config['targetArea'] = combination[2]
           config['slidingWindow'] = combination[3]
           config['model'] = combination[4]
           train(config)
