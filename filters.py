import matplotlib.pyplot as plt 
import numpy as np 
import scipy as sp 
'''
This is a block comment
'''
# Variables
e = 0.5088
nb = 4		# order of butterworth
n = 3
R1 = 50
R2 = 75
wp = 900e+06
ck = [1,1,1]
cap_array_50 = [1,1,1]
cap_array_75 = [1,1,1]
l_array_50 = [1,1,1]
l_array_75 = [1,1,1]
bk_old = np.array([1,.6464, 1.561,1.561,.6464])
bk = [1,1,1,1,1]
for i in range(1,5):
	bk[i] = 2*(e**(1/nb))*np.sin(((2*i-1)*np.pi)/(2*nb))
print "\nBks are: " + str(bk)

beta = np.sinh(np.tanh(1/np.sqrt(1+e**2))/n)
for i in range(1,len(bk)-1):
	print i
	if (i == 1):
		ck[i-1] = (bk[i]*bk[i-1])/(1*(beta**2+np.sin((i-1)*np.pi/n)**2))
	else: 
		ck[i-1] = (bk[i]*bk[i-1])/(ck[i-1]*(beta**2+np.sin((i-1)*np.pi/n)**2))

for i in range(0,3):
	print "i is: " + str(i)
	cap_array_50[i] = 1/(wp*R1)*ck[i]
	cap_array_75[i] = 1/(wp*R2)*ck[i]
	l_array_50[i] = R1/wp * ck[i]
	l_array_75[i] = R2/wp * ck[i]
print beta
print ck
print "Cap Array At 50" + u"\u2126" + " is " + str(cap_array_50)+"\n"
print "Inductor Array At 50" + u"\u2126" + " is" + str(l_array_50) + "\n"
print "Cap Array at 75" + u"\u2126" + " is " + str(cap_array_75) + "\n"
print "Inductor Array at 75" + u"\u2126" + " is " + str(l_array_75) + "\n"