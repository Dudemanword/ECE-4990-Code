# low pass filter calculator
# ECE 4990 by Kevin Hogg

#import mathmatical functions
import decimal;
import numpy as np;
import scipy as sp;

#input variables
zin = 50.0;
fh = 1000e6;
pat = 1.0;		#passband attenuation in dB
fs = 3e9;
sat = 30.0;		#stopband attenuation  in dB
#firsty = str(raw_input("L or C first? "));		#L or C
firsty = "L";

#calculated variables
wh = 2*np.pi*fh;
ws = 2*np.pi*fs;

# transmission line section
#-------------------------------------------------------------
# function below

def low_pass(z, w):
	cap = (2/(w))*1/z;
	ind = (2/(w))*z;
	out = [cap, ind];
	return out;

output = low_pass(zin, wh);

print "\nFor transmission line based filter @ " + str(zin) + u"\u2126" + ":";
print "Capacitor Value: " + decimal.Decimal(str(output[0])).to_eng_string();
print "Inductor Value: " + decimal.Decimal(str(output[1])).to_eng_string();

# butterworth section
#-------------------------------------------------------------
# find order first

e = np.sqrt(10**(pat/10)-1);
As = 10**(sat/10);
n = np.ceil((np.log(np.sqrt(As)/e))/(np.log(ws/wh)));

#find coefficients
bk = np.ones(len(str(n))+2);

for i in range(1,len(str(n))+2):
	bk[i] = 2*(e**(1/n))*np.sin(((2*i-1)*np.pi)/(2*n));
print "\nBks are: " + str(bk)

compies = [];		#component array
if (firsty == "L" or firsty == "l"):
	for (i) in range(0,len(str(n))+1):
		if (i%2 == 0): compies.append(zin*bk[i+1]/wh);
		elif (i%2 == 1): compies.append(bk[i+1]/(wh*zin));

elif (firsty == "C" or firsty == "c"):
	for (i) in range(0,len(str(n))+1):
		if (i%2 == 0): compies.append(bk[i+1]/(wh*zin));
		elif (i%2 == 1): compies.append(zin*bk[i+1]/wh);

print "\nFor Butterworth filter @ " + str(zin) + u"\u2126" + ":";
print "Components (" + str(firsty) + " first)";
for k in range(0,len(compies)):
	print "Component " + str(k+1) + " : " + decimal.Decimal(str(compies[k])).to_eng_string();

# chebyshev section
#-------------------------------------------------------------
# find order first
nc = np.ceil((np.arccosh(np.sqrt(As-1)/e))/(np.arccosh(ws/wh)));

#find coefficients

beta = np.sinh(np.arctanh(1/np.sqrt(1+e**2))/nc)

cbk = [1];
for i in range(1,len(str(nc))+1):
	cbk.append(2*np.sin(((2*i-1)*np.pi)/(2*nc)));
print "\nCBks are: " + str(cbk)

ck = np.ones(len(str(nc))+1);
print "\nCKs are:" + str(ck);
for i in range(1,len(cbk)):
	if (i == 1):
		ck[i] = cbk[i]/beta;
	else: 
		ck[i] = (cbk[i]*cbk[i-1])/(ck[i-1]*(beta**2+np.sin((i-1)*np.pi/nc)**2));

compies_cheby = [];		#component array
if (firsty == "L" or firsty == "l"):
	for (i) in range(1,len(str(nc))+1):
		if (i%2 == 1): compies_cheby.append(zin*ck[i]/wh);
		elif (i%2 == 0): compies_cheby.append(ck[i]/(wh*zin));

elif (firsty == "C" or firsty == "c"):
	for (i) in range(1,len(str(nc))+1):
		if (i%2 == 1): compies_cheby.append(ck[i]/(wh*zin));
		elif (i%2 == 0): compies_cheby.append(zin*ck[i]/wh);

print "\nFor Chebyshev filter @ " + str(zin) + u"\u2126" + ":";
print "Components (" + str(firsty) + " first)";
for k in range(0,len(compies_cheby)):
	print "Component " + str(k+1) + " : " + decimal.Decimal(str(compies_cheby[k])).to_eng_string();