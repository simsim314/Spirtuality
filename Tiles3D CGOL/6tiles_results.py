import golly as g 
import numpy as np
import ast

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

	add_rule(mar_rule, [0, 0, 0, 0], [0, 0, 0, 0])
	add_rule(mar_rule, [1, 1, 1, 1], [bits[1], bits[1], bits[1], bits[1]])
	add_rule(mar_rule, [1, 0, 1, 0], [bits[2], bits[3], bits[2], bits[3]])
	add_rule(mar_rule, [1, 0, 0, 0], [bits[4], bits[5], bits[6], bits[7]])
	add_rule(mar_rule, [1, 1, 0, 0], [bits[8], bits[9], bits[10], bits[11]])
	add_rule(mar_rule, [1, 1, 1, 0], [bits[0], bits[12], bits[13], bits[14]])
	
	return mar_rule 

def rand_fill(x, y, N):
	D = int(N / 2)
	S = int(N/4)
	g.select([x + S, y + S,D,D])
	g.randfill(50)

def all_rules():
	rules = [] 
	bits = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	
	for i in range(2**15):
		rules.append(fill_rule(bits))
		next(bits)
	
	return rules 

a_rules = all_rules()

N = 200	

rules = [] 

with open(r'C:\Users\SimSim314\Documents\GitHub\Roblox\rules.txt','r') as f:
	lines = f.readlines()

for line in lines:
	if len(line) > 5:
		rules.append(ast.literal_eval(line))

for i in range(2**15):
	for r in range(len(rules)):
		x = (N + 10) * r
		
		if i == 0:
			rand_fill(x,0, N)
			
		iter(x + 0, 0, N, rules[r])
		iter(x + 1, 1, N, rules[r])
		
		g.update()