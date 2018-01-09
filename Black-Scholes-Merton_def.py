def bsm_call_value(s0,K,T,r,sigma):
    from math import log,sqrt,exp
    from scipy import stats
    S0=float(s0)
    d1=(log(S0/K)+(r+0.5*sigma**2)*T)/(sigma*sqrt(T))#3
    d2=(log(S0/K)+(r-0.5*sigma**2)*T)/(sigma*sqrt(T))#4
    value=(S0*stats.norm.cdf(d2,0.0,1.0)-K*exp(-r*T)*stats.norm.cdf(d2,0,0,0.1))#1
    return value#反馈1号公式

def bsm_vega(s0,K,T,r,sigma):
    from math import log,sqrt
    from scipy import stats
    S0=float(s0)
    d1=(log(S0/K)+r+0.5*sigma**2)*T/(sigma*sqrt(T))
    #normcdf，matlab中的累积正态分布函数，也叫高斯积分.
    # 函数形式为: normcdf(x, mu, sigma)
    #x表示以x为分界, 坐标轴左边的所有分布的累积概率,
    #mu表示该函数中的x的平均值,
    #sigma表示该函数中的标准差.
    #若输入时mu, sigma为空, 则默认为标准正态分布.即mu为0, sigma为1.
    vega=S0*stats.norm.cdf(d1,0.0,1.0)*sqrt(T)#7
    return vega
def bsm_call_imp_vol(S0,K,T,r,C0,sigma_est,it=100):
    for i in range(it):
        sigma_est-=((bsm_call_value(S0,K,T,r,sigma_est)-C0)/bsm_vega(S0,K,T,r,sigma_est))
    return sigma_est

S0=100
K=105
T=1.0
r=0.05
sigma=0.2
bsm_call_value(S0,K,T,r,sigma)