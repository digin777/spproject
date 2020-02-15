import math
import pandas as pd
class johnswapspectrum:

	def __init__(self,alpha=None,hs=None,tp=None,gamma=None,*args):
		self.alpha=alpha
		self.hs=hs
		self.tp=tp
		self.gamma=gamma
		if args is not ():
			self.sigma_a,self.sigma_b=args
			
	def set_alpha(self,alpha):
		self.alpha=alpha
		
	def set_waveheight(self,hs):
		self.hs=hs
		
	def set_sep_peakperiod(self,tp):
		self.tp=tp
		
	def set_peakness_parameter(self,gamma):
		self.gamma=gamma
		
	def set_sigma_a_and_sigma_b(self,*args):
		self.sigma_a,self.sigma_b=args
		
	def set_omega_z(self):
		self.omega_z=self.c_omega_z(self.tp)
		
	def c_sigma(self,omega):
		assert(self.sigma_a!=None and self.sigma_b!=None),"sigma_a and sigma_b must be provided"
		if omega<=self.omega_z:
			return self.sigma_a
		else:
			return self.sigma_b
			
	def c_omega_z(self,tp=None):
		if tp==None:
			tp=self.tp
		return((2*math.pi)/tp)
		
	def c_T(self,omega):
		return((2*math.pi)/omega)
		
	def c_somega(self,omega,sigma,g=9.81):
		part_a=((self.alpha*(g**2)*(omega**-5)))
		part_b=math.exp(-1.25*((omega/self.omega_z)**-4))
		part_c=self.gamma**(math.exp((-(omega-self.omega_z)**2)/(2*(sigma**2)*(self.omega_z**2))))
		return part_a*part_b*part_c
			
	def e_omega(self,omega,velocity=5,angle=1,g=9.81):
		omega_e=omega*(1-(((omega*velocity)/g)*math.cos(angle)))
		return omega_e
		
	def c_somega_e(self,somega,omega_e,velocity,angle,g=9.81):
		part_a=((4*omega_e*velocity)/g)
		part_b=math.sqrt(1-part_a*math.cos(angle))
		part_c=somega*(1/part_b)
		return part_c
	
if __name__=="__main__":
	x=johnswapspectrum()
	x.set_sep_peakperiod(15.50)
	print(x.c_omega_z())