import numpy as np
import decimal

Caps = np.array(input("Insert List of Capacitances: "))
wr = np.array(input("Insert List of Resonant Frequencies: "))
for i in range(0,len(wr)):
	print "Parastic Inductances of " +str(Caps[i]) +" F " + " is " + decimal.Decimal(str(((1/(2*np.pi*wr[i]))**2)/Caps[i])).to_eng_string() +" H"