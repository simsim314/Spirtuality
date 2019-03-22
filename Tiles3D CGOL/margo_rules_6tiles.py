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

rules = all_rules()

N = 200	
	
failed = [] 
result = [] 

def validate_pop():
	pop = int(g.getpop())
	
	if pop == 0:
		return False 
		
	iter(0, 0, N, rules[i])
	iter(1, 1, N, rules[i])
	
	pop1 = int(g.getpop())
	
	if pop1 == 0:
		return False
	
	iter(0, 0, N, rules[i])
	iter(1, 1, N, rules[i])
	
	pop2 = int(g.getpop())
	
	if pop2 == 0:
		return False
	
	d1 = pop1 - pop
	d2 = pop2 - pop
	
	g.update()
	
	if d1 != 0:		
		if abs(d2 / d1) > 1.2:
			return False
	
	return True
	
for i in range(2**15):
		
	g.new(str(i))
	
	rand_fill(0,0, N)
	iter(0, 0, N, rules[i])
	iter(1, 1, N, rules[i])
	
	prev_box = str(g.getrect())
	p_num_out = 0 
	boxs = {} 
	cells = g.getcells(g.getrect())
	

	for j in range(250):
		if validate_pop() == False:
			break
		
		if str(cells) == str(g.getcells(g.getrect())):
			break 
		else :
			cells = g.getcells(g.getrect())
			
		numc = len(g.getcells([30, 30, 140, 140])) / 2
		pop = int(g.getpop())
		num_out = pop - numc
		
		if pop == 0:
			break 
	
		if num_out > 40:
			break
		
		if prev_box != str(g.getrect()):
			if abs(p_num_out - num_out) < 10 and abs(p_num_out - num_out) > 0:
				with open(r'C:\Users\SimSim314\Documents\GitHub\Roblox\rules.txt', "a") as myfile:
					myfile.write(str(rules[i]))
					myfile.write("\n\n")
				
				result.append(rules[i])
				break
				
		if prev_box in boxs:
			boxs[prev_box] += 1
		else:
			boxs[prev_box] = 1
		
		if boxs[prev_box] == 20:
			break
			
		prev_box = str(g.getrect())
		p_num_out = num_out
		
		g.show(str((i, j, len(result))))
		g.fit()
		g.update()


