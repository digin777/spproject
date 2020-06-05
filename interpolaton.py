import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
def interpolation(x,y,novalues):
	xmin=x.min()
	xmax=x.max()
	print(xmax,xmin)
	ratio=(xmax-xmin)/(novalues+1)
	xval=xmin
	xvalues=[]
	for i in range(novalues):
		xval+=ratio
		xvalues.append(xval)
	xvalues.insert(0,xmin)
	xvalues.append(xmax)
	yvalues=np.interp(xvalues,x,y)
	return(xvalues,yvalues)
	

if __name__ == '__main__':
	df=pd.read_csv('out.csv')
	x,y=interpolation(df['we'],df['swe'],77)
	plt.plot(x,y)
	plt.show()