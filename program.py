from lib.spectrum import johnswapspectrum
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
spetrum=johnswapspectrum()
alpha=float(input("input alpha: "))
spetrum.set_alpha(alpha)
hs=float(input("input sig.wave height: "))
spetrum.set_waveheight(hs)
tp=float(input("spectral peak period: "))
spetrum.set_sep_peakperiod(tp)
gamma=float(input("input peakness parameter: "))
spetrum.set_peakness_parameter(gamma)
sigma_a=float(input("input sigma_a: "))
sigma_b=float(input("input sigma_b: "))
spetrum.set_sigma_a_and_sigma_b(sigma_a,sigma_b)
spetrum.set_omega_z()
df=pd.DataFrame(columns=['T','w','sig','sw'])
no_w=int(input("no of w : "))
for i in range(no_w):
	#w=float(input("input w : "))
	for w in np.arange(0.250,2.225,0.025):
		df=df.append({'T':spetrum.c_T(w),'w':w,'sig':spetrum.c_sigma(w),'sw':spetrum.c_somega(w,spetrum.c_sigma(w))},ignore_index=True)
print(df.head())
inp=input('do you want compute spectum')
if inp=="y":
	angle=float(input("angle :"))
	velocity=float(input("velocity :"))
	df['we']=df.apply(lambda x:spetrum.e_omega(x['w'],velocity,angle),axis=1)
	print([i for i in df["we"]],df["we"].name)
	df['swe']=df.apply(lambda x:spetrum.c_somega_e(x['sw'],x['we'],velocity,angle),axis=1)
	print(df)
	plt.plot(df['we'],df['swe'])
	plt.show()
	df.to_csv('out.csv',index=False)
