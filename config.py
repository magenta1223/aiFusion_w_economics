CONFIG = {

    # target variables 
    "target" : "d",
    # target horizon 
    "targetHorizon" : 1,

    # number of segmentation
    "nDistrict" : 9,
    
    # Stochastic volatility mode
    # None: Base
    # Own : Own SV
    # All : All SV
    # All+ : All + important area SV
    "StochVol" : None,
    
    # sliding winow 
    "slidingWindow" : 12,

    # test set ratio
    "test" : 0.2

}

TARGETS = {
    8: ['Far West', 'Southwest', 'Rocky Mountain', 'Plains', 'Great Lakes', 'Southeast', 'Mideast', 'New England'],
    9 : ['East North Central', 'East South Central', 'Middle Atlantic', 'Mountain', 'New England', 'Pacific', 'South Atlantic', 'West North Central', 'West South Central']
}

WINDOWS = [4, 8, 16, 20, 28, 40]
HORIZONS = [1, 2, 4]
STOCHASTICVOLATILITIES = [None, "Own", "All"]
