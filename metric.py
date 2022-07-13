from scipy.stats import norm
import numpy as np

def clarkwest(null_M_pred, alt_M_pred, target):
    """
    Clark and West prediction for rolling window.
    기존 구현  :
    clarkwest_calculation(
        target        = extract_target(null, dataset[-seq_len(R),,drop = FALSE]),
        null.forecast = recursive_forecasts(null, dataset, R, window),
        alt.forecast  = recursive_forecasts(alt, dataset, R, window),
        vcv)

    clarkwest_calculation <- function(target, null.forecast, 
                                    alt.forecast, vcv) {
        P <- length(target)
        oos.sequence <- {(target - null.forecast)^2 - 
                        (target - alt.forecast)^2 + 
                        (null.forecast - alt.forecast)^2}
        mu <- mean(oos.sequence)
        avar <- vcv(oos.sequence) # vcv : variance-covariance matrix 같기는 한데, matrix가 pnorm의 인자로 들어갈 수 없다. 그냥 분산으로 가정. 
        return(list(mu = mu, avar = avar, 
                    pvalue = pnorm(sqrt(P) * mu, 0, sqrt(avar), FALSE)))
        }
    
    recursive_forecast : window type에 따른 예측. 현재는 rolling (sliding) window만을 사용하기 때문에 불필요함
    oos.seqeunce : null model의 MSE - alternative model의 MSE + null 과 alternative 간의 MSE
    즉, 앞의 두 항은 두 모델의 우열 비교. 마지막 항은 두 모델의 차이 비교
    
    그리고 mean과 vcv함수를 통해 이 시퀀스의 평균과 조정분산을 구한다.
    이 값들은 모델의 우열 혹은 차이가 있는지 없는지를 검정한다.
    """

    def squaredError(seq0, seq1):
        return (seq0 - seq1) ** 2

    oos = squaredError(target, null_M_pred) - squaredError(target, alt_M_pred) + squaredError(null_M_pred, alt_M_pred)
    
    mu = oos.mean()
    var = oos.var()
    p = len(target)

    return [mu, var, 1- norm.cdf(mu * np.sqrt(p), 0, np.sqrt(var))]

