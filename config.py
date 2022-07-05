CONFIG = {

    # Responsive Variables
    "targetFeature" : "Average Urate",

    # features shared across all the regions
    "commonFeatures" : ["logCPIDiff", "NFCI", "TMU", "TFU", "TRU"],

    # region specific features
    "regionVariantFeatures" : ['Average EPU'],

    # target horizon 
    "targetHorizon" : 1,

    # number of area segementation
    "nDistrict" : 9,
    
    # Urate Mode
    # None: Base
    # Own : Own Urate
    # All : All Urate
    # TODO : All+ : All + important area Urate
    "EPU" : None,
    
    # sliding winow 
    "slidingWindow" : 12,

    # validation set ratio
    "test" : 0.2,

}

TARGETS = {
    8 : ['Far West', 'Southwest', 'Rocky Mountain', 'Plains', 'Great Lakes', 'Southeast', 'Mideast', 'New England'],
    9 : ['East North Central', 'East South Central', 'Middle Atlantic', 'Mountain', 'New England', 'Pacific', 'South Atlantic', 'West North Central', 'West South Central']
}

# TODO:  quarterly > monthly
WINDOWS = [4, 8, 16, 20, 28, 40]
HORIZONS = [3, 6, 12]
EPU = [None, "Own", "All"]
