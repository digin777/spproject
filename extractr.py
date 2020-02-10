import pandas as pd
from matplotlib import pyplot as plt
import script
df=pd.read_csv("data/pddata.csv")
'''plt.plot(df['w'], df['Sz(w)'])
plt.show()
plt.plot(df['w'],df['f(g)'])
plt.show()'''
df['we']=df['w'].apply(script.e_omega)
df['swe']=df.apply(lambda x:script.c_somega_e(x['Sz(w)'],x['we'],1,1), axis=1)
plt.plot(df['we'],df['swe'])
plt.show()
print(df.head())