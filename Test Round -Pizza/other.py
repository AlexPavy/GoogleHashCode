import random

inf = open('test_round.in', 'r')
outf = open('pavy_florea.out', 'w')

line = inf.readline()
params = line.split(' ')
R = int(params[0])
C = int(params[1])
H = int(params[2])
S = int(params[3])


RawPizza = []
Solution = []


class Pizza:
	def __init__(self, r1, c1, r2, c2, p, ham):
		self.r1 = r1
		self.c1 = c1
		self.r2 = r2
		self.c2 = c2
		self.p = p
		self.ham = ham


# read file
for r in range(R):
	line = inf.readline()
	rawPLine = []
	for c in range(len(line)):
		if line[c] == 'H':
			rawPLine.append(1)
		else:
			rawPLine.append(0)
	RawPizza.append(rawPLine)

def tryRow(pizza):
	if pizza.r2+1 >= R:
		return None
	newPizza = Pizza(pizza.r1, pizza.c1, pizza.r2+1, pizza.c2, pizza.p+pizza.c2 - pizza.c1 + 1, pizza.ham)

	for c in range(newPizza.c1, newPizza.c2+1):
		if RawPizza[newPizza.r2][c] == 2:
			return None
		if RawPizza[newPizza.r2][c] == 1:
			newPizza.ham += 1
	if newPizza.p > S:
		return None
	if newPizza.ham < H:
		return tryRow(newPizza) or tryCol(newPizza)
	else:
		return newPizza

def tryCol(pizza):
	if pizza.c2+1 >= C:
		return None
	newPizza = Pizza(pizza.r1, pizza.c1, pizza.r2, pizza.c2+1, pizza.p+pizza.r2 - pizza.r1 + 1, pizza.ham)

	# print(newPizza.p)
	for r in range(newPizza.r1, newPizza.r2+1):
		if RawPizza[r][newPizza.c2] == 2:
			return None
		if RawPizza[r][newPizza.c2] == 1:
			newPizza.ham += 1
	if newPizza.p > S:
		return None
	if newPizza.ham < H:
		return tryRow(newPizza) or tryCol(newPizza)
	else:
		return newPizza

r4 = 0
c4 = 0
slices = 0

while r4 < R:
	pizza = Pizza(r4, c4, r4, c4, 1, RawPizza[r4][c4] == 1)
	pizza = tryRow(pizza) or tryCol(pizza)

	if pizza:
		c4 = pizza.c2 + 1
	else:
		c4 += 1
		while RawPizza[r4][c4] == 2 and c4 < C:
			c4 += 1


	if c4 >= C:
		c4 = 0
		r4 += 1

	if r4+1 >= R:
		break

	while RawPizza[r4][c4] == 2 and r4 < R:
		c4 += 1

	if pizza:
		slices += 1
		Solution.append(pizza)
		print(pizza.p, pizza.ham)
		for r in range(pizza.r1, pizza.r2+1):
			for c in range(pizza.c1, pizza.c2+1):
				RawPizza[r][c] = 2

def writesol():
	# print solution
	outf.write(str(slices) + '\n')
	for i in range(Solution.__len__()):
		s = Solution[i]
		outf.write(str(s.r1) + ' ' + str(s.c1) + ' ' + str(s.r2) + ' ' + str(s.c2) + '\n')

def score():
	sc = 0
	for i in range(Solution.__len__()):
		s = Solution[i]
		sc += s.p
	print(sc)

writesol()
score()
inf.close()
outf.close()