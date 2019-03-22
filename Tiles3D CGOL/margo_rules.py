import golly as g 
import numpy as np

def rotate(l, k):
	l1 = []
	
	for i in range(len(l)):
		l1.append(l[(k + i) % len(l)])
		
	return l1


def add_rule(mar_rule, l_in, l_out):
	for i in range(4):
		l = rotate(l_in, i)
		u = rotate(l_out, i)
		strl = ""
		for j in l:
			strl += str(j)
			
		mar_rule[strl] = u

def key_xy(x, y):
	res = ""
	res += str(g.getcell(x, y))
	res += str(g.getcell(x + 1, y))
	res += str(g.getcell(x + 1, y + 1))
	res += str(g.getcell(x, y + 1))
	return res

def fill_xy(x, y, l):
	g.setcell(x, y, l[0])
	g.setcell(x + 1, y, l[1])
	g.setcell(x + 1, y + 1, l[2])
	g.setcell(x, y + 1, l[3])
	
def iter(dx, dy, N, rule):

	for i in range(dx, N + dx, 2):
		for j in range(dy, N + dy, 2):
			l = rule[key_xy(i, j)]
			fill_xy(i, j, l)



def next(bits):
	i = 0 
	
	while bits[i] == 1 and i < len(bits):
		bits[i] = 0 
		i += 1
	
	bits[i] = 1
	
def fill_rule(bits):
	mar_rule = {}

	add_rule(mar_rule, [1, 0, 1, 0], [bits[0], bits[1], bits[2], bits[3]])
	add_rule(mar_rule, [1, 0, 0, 0], [bits[4], bits[5], bits[6], bits[7]])

	add_rule(mar_rule, [1, 1, 0, 0], [bits[8], bits[8], bits[8], bits[8]])
	add_rule(mar_rule, [1, 1, 1, 0], [bits[8], bits[8], bits[8], bits[8]])
	add_rule(mar_rule, [1, 1, 1, 1], [bits[8], bits[8], bits[8], bits[8]])

	add_rule(mar_rule, [0, 0, 0, 0], [0, 0, 0, 0])
	
	return mar_rule 

def rand_fill(x, y, N):
	D = int(N / 2)
	S = int(N/4)
	g.select([x + S, y + S,D,D])
	g.randfill(50)

def all_rules():
	rules = [] 
	bits = [0,0,0,0,0,0,0,0,0,0]
	
	for i in range(512):
		rules.append(fill_rule(bits))
		next(bits)
	
	return rules 

rules = all_rules()

N = 20

for i in range(512):
	x = (N + 10) * (i % 30) 
	y = (N + 10) * int(i / 30) 
	
	rand_fill(x, y,N)

failed = [] 

for j in range(10000):
	for i in range(512):
		x = (N + 10) * (i % 32) 
		y = (N + 10) * int(i / 32) 
		
		if (x, y) in failed:
			continue 
		
		#if y >= N * 5:
		#	continue 
			
			
		#if len(g.getcells([x, y, N, N])) / 2 < 1400 or j < 2:
			
		iter(x, y, N, rules[i])
		iter(x + 1, y + 1, N, rules[i])
			
		#g.show(str((i, j, rules[i])))
		g.show(str((i, j)))
		g.update()
		#else:
		#	failed.append((x, y))


