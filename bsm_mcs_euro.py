import numpy as np
S0=100
K=105
T=1.0
r=0.05
T=1.0
sigma=0.2
I=100000
z=np.random.standard_normal(I)
ST=S0*np.exp((r-0.5*sigma**2)*T+sigma*np.sqrt(T)*z)
hT=np.maximum(ST-K,0)
C0=np.exp(-r*T)*sum(hT)/I
print("Value of the European Call Option {0:5.3f}".format(C0))