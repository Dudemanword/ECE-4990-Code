# filter component value generator
# ECE 4990 by Kevin Hogg

#import mathmatical functions
import decimal;
import numpy as np;
import scipy as sp;

class Filter:
	"""Filter class for calculating component values"""

	def __init__(self, type="lowpass", design="trans", zin=50, f1=None, bw=0, pat=1.0, fs=None, sat=30.0, firsty="L"):
		types = ('lowpass', 'highpass', 'bandpass', 'bandstop')
		designs = ('trans', 'butter', 'cheby')
		self.type = type.lower()
		if all(x!=self.type.lower() for x in types):
			raise ValueError('Filter type not recognized...')
		self.design = design.lower()
		if all(x!=self.design.lower() for x in designs):
			raise ValueError('Filter design type not recognized...')
		self.zin = zin
		if (f1 != None):
			self.w1 = f1*2*np.pi
		else: raise ValueError('No frequency provided!')

		self.bw = bw*2*np.pi

		if (fs != None):
			self.ws = fs*2*np.pi

		self.firsty = firsty.lower()
		self.components = []

		# epsilon and attenuation calcs
		self.epsilon = np.sqrt(10**(pat/10)-1)
		self.sat = 10**(sat/10)
		self.pat = 10**(pat/10)

		if (self.design == "trans"):
			self.genTrans()
			if (self.type == "highpass"): self.convHighPass();
			elif (self.type == "bandpass"): self.convBandPass()
			elif (self.type == "bandstop"): self.convBandStop()
		
		elif (self.design == "butter"):
			self.genButter()
			if (self.type == "highpass"): self.convHighPass();
			elif (self.type == "bandpass"): self.convBandPass()
			elif (self.type == "bandstop"): self.convBandStop()

		elif (self.design == "cheby"):
			self.genCheby()
			if (self.type == "highpass"): self.convHighPass();
			elif (self.type == "bandpass"): self.convBandPass()
			elif (self.type == "bandstop"): self.convBandStop()

		'''
			# cleaner implementation...?
			@classmethod
				def trans(self, type, zin=50):
		'''

	def genTrans(self):
		# calculations for transmission line design
		cap = (2/(self.w1))*1/self.zin;
		ind = (2/(self.w1))*self.zin;
		l1 = Component("L1", "inductor", ind)
		c1 = Component("C2", "capacitor", cap)
		self.components = [l1, c1]

	def genButter(self):
		# find order first
		n = np.ceil((np.log(np.sqrt(self.sat)/self.epsilon))/(np.log(self.ws/self.w1)));

		#find coefficients
		bk = np.ones(len(str(n))+2);

		for i in range(1,len(str(n))+2):
			bk[i] = 2*(self.epsilon**(1/n))*np.sin(((2*i-1)*np.pi)/(2*n));

		if (self.firsty == "l"):
			for i in range(1, len(str(n))+2):
				if (i%2 == 1):
					tmp = "L" + str(i)
					self.components.append(Component(tmp, "inductor", self.zin*bk[i]/self.w1));
				elif (i%2 == 0):
					tmp = "C" + str(i)
					self.components.append(Component(tmp, "capacitor", bk[i]/(self.w1*self.zin)));
		elif (self.firsty == "c"):
			for i in range(1, len(str(n))+2):
				if (i%2 == 1):
					tmp = "C" + str(i)
					self.components.append(Component(tmp, "capacitor", bk[i]/(self.w1*self.zin)));
				elif (i%2 == 0):
					tmp = "L" + str(i)
					self.components.append(Component(tmp, "inductor", self.zin*bk[i]/self.w1));


	def genCheby(self):
		# find order first
		n = np.ceil((np.arccosh(np.sqrt(self.sat-1)/self.epsilon))/(np.arccosh(self.ws/self.w1)));

		#find coefficients
		beta = np.sinh(np.arctanh(1/np.sqrt(1+self.epsilon**2))/n)

		cbk = [1];
		for i in range(1,len(str(n))+1):
			cbk.append(2*np.sin(((2*i-1)*np.pi)/(2*n)));

		ck = np.ones(len(str(n))+1);

		for i in range(1,len(cbk)):
			if (i == 1):
				ck[i] = cbk[i]/beta;
			else: 
				ck[i] = (cbk[i]*cbk[i-1])/(ck[i-1]*(beta**2+np.sin((i-1)*np.pi/n)**2));

		if (self.firsty == "l"):
			for i in range(1, len(str(n))+1):
				if (i%2 == 1):
					tmp = "L" + str(i)
					self.components.append(Component(tmp, "inductor", self.zin*ck[i]/self.w1));
				elif (i%2 == 0):
					tmp = "C" + str(i)
					self.components.append(Component(tmp, "capacitor", ck[i]/(self.w1*self.zin)));
		elif (self.firsty == "c"):
			for i in range(1, len(str(n))+1):
				if (i%2 == 1):
					tmp = "C" + str(i)
					self.components.append(Component(tmp, "capacitor", ck[i]/(self.w1*self.zin)));
				elif (i%2 == 0):
					tmp = "L" + str(i)
					self.components.append(Component(tmp, "inductor", self.zin*ck[i]/self.w1));


	def convHighPass(self):
		for i in range(0, len(self.components)):
			if(self.components[i].type == "inductor"):
				self.components[i].setType("capacitor")
				self.components[i].setName(self.components[i].name.replace('L', 'C'))
				self.components[i].setValue(1/(self.w1**2*self.components[i].value))
			elif(self.components[i].type == "capacitor"):
				self.components[i].setType("inductor")
				self.components[i].setName(self.components[i].name.replace('C', 'L'))
				self.components[i].setValue(1/(self.w1**2*self.components[i].value))
					
	def convBandPass(self):
		tmpcomponents = []
		for i in range(0, len(self.components)):
			if(self.components[i].type == "inductor"):
				tmpcomponents.append(Component(self.components[i].name, "inductor", (self.w1*self.components[i].value)/self.bw))
				tmpcomponents.append(Component(self.components[i].name.replace('L', 'C'), "capacitor", self.bw/((self.w1**3)*self.components[i].value)))
			elif(self.components[i].type == "capacitor"):
				tmpcomponents.append(Component(self.components[i].name.replace('C', 'L'), "inductor", self.bw/((self.w1**3)*self.components[i].value)))
				tmpcomponents.append(Component(self.components[i].name, "capacitor", (self.components[i].value*self.w1/self.bw)))
		self.components = tmpcomponents
	
	def convBandStop(self):
		tmpcomponents = []
		for i in range(0, len(self.components)):
			if(self.components[i].type == "inductor"):
				tmpcomponents.append(Component(self.components[i].name, "inductor", (self.bw*self.components[i].value)/self.w1))
				tmpcomponents.append(Component(self.components[i].name.replace('L', 'C'), "capacitor", 1/(self.bw*self.components[i].value*self.w1)))
			elif(self.components[i].type == "capacitor"):
				tmpcomponents.append(Component(self.components[i].name.replace('C', 'L'), "inductor", 1/(self.bw*self.components[i].value*self.w1)))
				tmpcomponents.append(Component(self.components[i].name, "capacitor", (self.bw*self.components[i].value)/self.w1))
		self.components = tmpcomponents

	def getComponents(self):
		return self.components


class Component:
	"""Test of component class"""
	def __init__(self, name, type="empty", value=-1):
		self.name = name
		self.type = type.lower()
		types = ("line", "capacitor", "inductor", "empty")
		if all(x!=self.type for x in types):
			raise ValueError('Filter type not recognized...')
		self.value = value
		if (self.type == "capacitor"): self.units = "F"
		elif (self.type == "inductor"): self.units = "H"

	def setName(self, name):
		self.name = name

	def getName(self):
		return self.name

	def setType(self, type):
		self.type = type

	def setValue(self, value):
		self.value = value

	def getValue(self):
		return self.value

# stuffs below for testing purposes
fil = Filter('bandstop', 'cheby', 50, f1=900e6, bw=100e6, fs=2.7e9, firsty='L')

print "\nComponent values for a " + str(fil.design) + " " + str(fil.type) + " filter @ " + str(fil.zin) + "ohms"
print "----------------------------------------------------------"
components = fil.getComponents()
for i in range(0, len(components)):
	print components[i].name + ": " + decimal.Decimal(str(components[i].value)).to_eng_string()