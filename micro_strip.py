# micro strip low pass filter calculation
# ECE 4990 by Kevin Hogg

#import mathmatical functions
import decimal;
import numpy as np;
import scipy as sp;
#input variables
zin = 50.0;
fh = 1500e6;
c = 3e10;
er = 4.5;
zin_l = 150;
zin_c = 15;

#calculated variables
wh = 2*np.pi*fh;

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

# calculate length for microstrip
#-------------------------------------------------------------
# for inductor
len_ind = (output[1]*c)/(zin_l*np.sqrt(er));

# for capacitor
len_cap = (output[0]*zin_c*c)/(np.sqrt(er));

print "\nMicrostrip Lengths (in cm)";
print "Capacitor length: " + decimal.Decimal(str(len_cap)).to_eng_string();
print "Inductor length: " + decimal.Decimal(str(len_ind)).to_eng_string();