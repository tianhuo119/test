import math
import numpy as np
from time import time
np.random.seed(20000)
t0=time()
t0=time()
S0=100
K=105
T=1.0
r=0.05
sigma=0.2
M=50
dt=T/M
I=250000
S=np.zeros((M+1,I))
S[0]=S0
for t in range(1,M+1):
    z=np.random.standard_normal(I)
    S[t]=S[t-1]*np.exp((r-0.5*sigma**2)*dt+sigma*math.sqrt(dt)*z)
C0=math.exp(-r*T)*np.sum(np.maximum(S[-1]-K,0))/I
tnp1=time()-t0
print("European Option Value {0:7.3f}".format(C0))
print("Duration in Seconds {0:7.3f}".format(tnp1))