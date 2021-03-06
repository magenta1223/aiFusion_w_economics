from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor

CONFIG = {

    # Responsive Variables
    "targetFeature" : "Average Urate",
    
    # ------------------ V1 --------------------- #  
    # features shared across all the regions
    # deprecated 
    # "commonFeatures" : ["logCPIDiff", "NFCI", "TMU", "TFU", "TRU"],
    # region specific features
    # "regionVariantFeatures" : ['Average EPU'],


    # ---------------- V2 ----------------------- # 

    "regionVariantFeatures" : ["Aggregate Civil Labor Force Growth", "Average Initial Claim", "Average EPU"],

    "features" : {
        "national" : [],
        "regional" : []
    },

    # target horizon 
    "targetHorizon" : 1,

    # number of area segementation
    "nDistrict" : 9,
    
    # Urate Mode
    # None: Base
    # Own : Own Urate
    # All : All Urate
    # TODO : All+ : All + important area Urate
    # "EPU" : None,

    "model" : "RandomForest",
    
    # sliding winow 
    "slidingWindow" : 12,

    # validation set ratio
    "test" : 0.2,

    "threshold" : 0.95,
    
    # type 2 error
    "alpha" : 0.05
}

FEATURE_DICT = {
    "base" : {
        "national" : [ ],
        "regional" : ["Aggregate Civil Labor Force Growth", "Average Initial Claim"]
    },
    "alternative" : {
        "national" : [ ],
        "regional" : ["Aggregate Civil Labor Force Growth", "Average Initial Claim", "Average EPU"]
    },
    # example
    # "newExperiment" : {
    #     "national" : [ NATIONAL VARIABLES ],
    #     "regional" : [ REGIONAL VARIABLES ]
    # },

}


MODELS_DICT = {
    "RandomForest" : RandomForestRegressor,
    "AdaBoost" : AdaBoostRegressor,
    "GradientBoost" : GradientBoostingRegressor
}

#MODELS = ["RandomForest", "AdaBoost", "GradientBoost"]
MODELS = ["RandomForest"]


TARGETS = {
    8 : ['Far West', 'Southwest', 'Rocky Mountain', 'Plains', 'Great Lakes', 'Southeast', 'Mideast', 'New England'],
    9 : ['East North Central', 'East South Central', 'Middle Atlantic', 'Mountain', 'New England', 'Pacific', 'South Atlantic', 'West North Central', 'West South Central']
}

# TODO:  quarterly > monthly
WINDOWS = [4, 8, 16, 20, 28, 40]
HORIZONS = [3, 6, 12]
# EPU = [None, "Own", "All"] # deprecated
 


PARAMS = {
    "RandomForest" : {
        "n_estimators" : 10,
        "criterion" : "squared_error",
        "n_jobs" : 1,
        "verbose" : 1
    },

    "AdaBoost" : {
        "base_estimator" : DecisionTreeRegressor(criterion= "squared_error", max_depth= 5),
        "n_estimators" : 10,
        "loss" : "square"
    },

    "GradientBoost" : {
        "n_estimators" : 10, 
        "criterion" : "squared_error"
    }
} 

