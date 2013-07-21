from numpy import *
vb = 2.0
R2 = 300.0
Vcc = 10.0
vt = 25e-03
ib = 380e-06
R = 100.0
C = 1.768e-12
m = 3.104
r1 = 1e3
r2 = 10e3
rp = 50.0
omega_0 = 2*pi*1e9

#defining j so I can use it with variables
j = complex(0, 1)

#Functions that do things...
def find_L(R, C, m):
	L = (R**2 * C)/m
	return L

def find_rp(rin, q):
	rp = rin*(1+q**2)
	return rp

def r_pi(vt, ib):
	rpi = vt/ib
	return rpi

def find_rs(r1,r2,rpi):
	rin = r1*r2/(r1+r2) 
	rin_real = rin*rpi/(rin + rpi)+10
	print rin_real
	return rin_real

def calc_q(rp,rs):
	if (rp > rs):
		q = sqrt(rp/rs - 1)
	else:
		print 'config 2'
		q = sqrt(rs/rp - 1)
	return q

def find_ls(rs, q, omega_0):
	ls = rs*q/omega_0
	return ls

def find_c(omega_0, ls):
	c = ((1/omega_0)**2)/ls
	return c

def find_zs(ro, R, omega, L, C):
	s = j*omega
	z_1 = parallel(ro, (L*s+R))
	zs = parallel(z_1, 1/(C*s))
	#zs = (R*(s*(L/R) + 1))/(s**2*L*C + s*R*C + 1)
	#zs = (R/(s*C))/(R + (1/(s*C)))
	return zs

def parallel(a, b):
	ans = a*b/(a+b)
	return ans

#Do calculations and stuff
r_first = parallel(100, (1/(j*omega_0*C)))
ro = parallel(r_first, 1.535e3)
zs = find_zs(ro,100, omega_0, 5.134e-9, 1.592e-12)
#rpi = r_pi(vt,ib)
#rp = find_rs(r1,r2,rpi)
rp = abs(ro)
rs = 50
q = calc_q(rp, rs)
ls = find_ls(rs,q,omega_0)
c = find_c(omega_0, ls)

print 'rs is ' + str(rs), 'q is ' + str(q), 'rp is ' + str(rp), 'ls is ' + str(ls), 'c is ' + str(c), 'zs is ' + str(abs(zs))
#print 'rs is ' + str(rs), 'q is ' + str(q), 'rp is ' + str(rp), 'ls is ' + str(ls), 'c is ' + str(c),'rpi is ' + str(rpi)
#'rpi is ' + str(rpi), 
