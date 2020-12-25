import math
import decimal
from decimal import Decimal
from fractions import Fraction
import string
import fileinput
from sympy import *
import re

x = Symbol('x')
y = Symbol('y')

def sign(x):
    return bool(x > 0) - bool(x < 0)

def changeSigns(x):
	z = abs(x)
	return bool(x < 0)*z - bool(x > 0)*z
	
def stringifySol(index, y):
	strung = "n = " + str(index) + ", root: " + str(y)
	return strung

#Complete Horner's Algorithm
def horner(poly, var, f = 0, index = 0):
	
	temp = 0	#first number
	b = []
	
	hornerx = Symbol('(x + ' + str(changeSigns(var)) + ')')
	
	for i in range(0, len(poly)):
		temp = temp * var + poly[i]
		b.append(temp)
	
	print(b)
	
	#get last element
	f = f + b[-1] * (hornerx) **(index)
	del b[-1]
		
	if(len(b) > 0):
		return horner(b, var, f, index + 1)
		
	print('The Taylor Series is: \nf(x) = ' + str(f))
	
	return
	
def lagrangeForm(A, B):
	size = len(A)
	T = []
	
	for i in range(0, size):
		numer = 1
		denom = 1
		for j in range(0, size - 1):
			tempNum = (x - A[(i + j + 1)%size])
			numer = tempNum * numer
			tempDenom = (A[i] - A[(i + j + 1)%size])
			denom = tempDenom * denom
			print("x_" + str(j) + ":  (" + str(tempNum) + ")/ " + str(tempDenom))
		print("L_" + str(i) + " = (" + str((numer)) + ") / " + str(denom))
		T.append(numer/denom)	
	
	eqn = 0
	for i in range (0, size):
		eqn = T[i] * B[i] + eqn
	
	return eqn
	#return simplify(eqn)
	
def dividedDif(A, B, index = 0, p = 0):
	size = len(B)
	
	C = []
	
	for i in range(0, size -1):
		eqn = (B[i + 1] - B[i])/(A[i + 1 + index] - A[(i)])
		C.append(eqn)
	
	print(C)
	
	p = newtonForm(A, B, index, p)
	
	if(size > 1):
		return dividedDif(A, C, index + 1, p)
	
	return simplify(p)
	
def newtonForm(A, B, index, p):
	temp = 1
	for i in range(0, index):
		temp = ((x - A[i]) * temp)
	p = p + B[0]*temp
	print(p)
	return p
	
def scaledPartialPivot(z):
	#get length and scale array
	n = len(z)
	scaleAry = [max([abs(z[i][j]) for j in range(n)]) for i in range(n)] 
  
	#do pivoting
	for i in range(0, n):
		print(z)
		rmax = 0
		for r in range(i, n):
			if rmax < abs(z[r][i]/scaleAry[r]):
				smax = r
				rmax = abs(z[r][i]/scaleAry[r])
				print(smax, rmax)
		#swap with tuple assignment
		(scaleAry[i], scaleAry[smax]) = (scaleAry[smax], scaleAry[i])
		(z[i], z[smax]) = (z[smax], z[i])
		print(z)
		
		for j in range(i+1, n):
			z[j] = [z[j][k] - z[i][k]*z[j][i]/z[i][i] for k in range(n+1)]

	#backward substitution
	print(z)
	x = [0] * n
	for i in range(n-1, -1, -1):
		opr = sum(z[i][j] * x[j] for j in range(i, n))
		print(opr)
		x[i] = (z[i][n] - opr) / z[i][i]
	return x



	
def secantIterate(x_1, x_0, f, iterations, index = 0):
	y = x_1 - ((x_1 - x_0)/(f.subs(x, x_1) - f.subs(x, x_0)))*f.subs(x, x_1)
	if (index < iterations):
		print('Secant: x_', index, '= f(', x_1, ') = ', y)
		return secantIterate(y, x_1, f, iterations, index + 1)
	return stringifySol(index, y)
	
def newtonIterate(z, f, f_prime, iterations, index = 0):
	y = z - f.subs(x, z) / f_prime.subs(x, z)
	if (index < iterations):
		print('Newton: x_', index, '= f(', z, ') = ', y)
		return newtonIterate(y, f, f_prime, iterations, index + 1)
	return stringifySol(index, y)

def bisection(f, a, b, iterations, index = 0):
	c = (a + b)/(2)
	f_c = f.subs(x, c)
	print('Bisection: x_', index, '= f(', c, ') = ', f_c)
	if (index < iterations):
		if(sign(f_c) == sign(f.subs(x, a))):
			return bisection(f, c, b, iterations, index + 1)
		else:
			return bisection(f, a, c, iterations, index + 1, )
	return stringifySol(index, c)
	
def bisectionError(f, a, b, error, index = 0):
	c = (a + b)/(2)
	f_c = f.subs(x, c)
	print('Bisection: x_', index, '= f(', c, ') = ', f_c)
	if (abs(c - a) > error):
		if(sign(f_c) == sign(f.subs(x, a))):
			return bisectionError(f, c, b, error, index + 1)
		else:
			return bisectionError(f, a, c, error, index + 1)
	return stringifySol(index, c)

BS="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def fromDecimal(convTo, number):
	temp = int(number)
	temp2 = number - temp
	b = []
	frac = []
	modulus = 0
	
	print("Number: " + str(number))
	while temp >= (1):
		modulus = BS[temp%convTo]
		b.append(modulus)
		temp = temp//convTo
		print("Dividing by " + str(convTo) + ": " + str(temp) + "; Modulus: " + str(modulus))
	
	c = []
	for i in range(0, len(b)):
		c.append(b[len(b) - i - 1])
	
	#decimal
	j = 0
	while(temp2 != 1 and j < 16):
		print("Multiplying " + str(temp2) + " by " + str(convTo) + ": " + str(temp2 * convTo))
		temp2 = temp2 * convTo
		frac.append(str(int(temp2)))
		if(temp2 > convTo - 1):
			temp2 = temp2 - 1
		j = j + 1
	
	string1 = ""
	string2 = ""
	string1 = string1.join(c)
	string2 = string2.join(frac)
	
	#newnumber = sciNotation(float(string1 + "." + string2))
	#print("Exponential form (ignore 10): " + newnumber)
	
	print(str(number) + " in base " + str(convTo) + " is : " + string1 + "." + string2)
	
	return string1 + "." + string2

#single precision: 127
#double precisoin: 153
def machineExponent(base, power, precision):
	temp = precision + power
	b = []
	modulus = 0
	
	print("Exponent machine number of " + str(power) + " + " + str(precision) + ": " + str(temp))
	while temp >= (1):
		modulus = BS[temp%base]
		b.append(modulus)
		temp = temp//base
		print("Dividing by " + str(base) + ": " + str(temp) + "; Modulus: " + str(modulus))
		
	string1 = ""
	string1 = string1.join(b)
		
	return string1

def sciNotation(x, i = 0):
	string = ""
	if(abs(x) < 1):
		return sciNotation(x * 10, i - 1)
	if(abs(x) >= 10):
		return sciNotation(x * 10**-1, i + 1)
	
	#x = round(x, dec)
	
	string = str(x) + " * 10 **" + str(i)	
	
	return string

def toDecimal(base, x):
	number = 0
	b = []
	intString = str(x)
	length = len(intString)
	index = 0
	string = ""
	digit = 0
	
	#seek decimal
	for i in range(0, length):
		if(intString[i] == "."):
			index = i
	
	print(index)
	
	for i in range(0, length):
		if(intString[i] != "."):
			string =  string + (intString[i] + " * " + str(base) + "**" + str(index - 1) + " + ")
			digit = int(intString[i]) * base**(index - 1)
			number = number + digit
			b.append(digit)
			index = index -1
		#print(number)
		
	
	print(string)
	print(b)
	
	return number
	

def iterate(a, b, f, iterations, index = 0):
	x_n2 = f.subs(x, a)
	x_n2 = x_n2.subs(y, b)
	print(simplify(x_n2))
	if(index < iterations):
		return iterate(b, x_n2, f, iterations, index+1)
	return stringifySol(index, x_n2)
