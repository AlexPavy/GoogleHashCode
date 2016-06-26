__author__ = 'Alex'

import random

inf = open('dc.in', 'r')
outf = open('pavy_florea.out', 'w')

line = inf.readline()
params = line.split(' ')
R = int(params[0])
S = int(params[1])
U = int(params[2])
P = int(params[3])
M = int(params[4])

SlotsMap = [[0 for s in range(S)] for r in range(R)]
SlotsMap_c = [[0 for s1 in range(S)] for r1 in range(R)]

Servers = []


class SolServer:
	def __init__(self, r, s, _p, c):
		self.r = r
		self.s = s
		self.p = _p
		self.c = c

BestServersSol = [SolServer('u', 0, 0, 0) for m1 in range(M)]  # positions
ServersSol = [SolServer('u', 0, 0, 0) for m1 in range(M)]  # positionssq



for u in range(U):
	line = inf.readline()
	pos = line.split(' ')
	SlotsMap[int(pos[0])][int(pos[1])] = -1
	SlotsMap_c[int(pos[0])][int(pos[1])] = -1

for m in range(M):
	line = inf.readline()
	serv = line.split(' ')
	servArray = [int(serv[0]), int(serv[1])]
	Servers.append(servArray)

Servers_enum = enumerate(Servers)
SortedServers = sorted(Servers_enum, key=lambda server: float(server[1][1]) / float(server[1][0]), reverse=True)


def poolscore(servers, p4):
	capacite = 0
	maxscore = 0
	nb_serv = 0
	for r3 in range(R):
		rowscore = 0
		for m3 in range(M):
			if servers[m3].r == r3:
				if servers[m3].p == p4:
					if servers[m3].c > 0:
						nb_serv += 1
					rowscore += servers[m3].c

		maxscore = max(maxscore, rowscore)
		capacite += rowscore

	if nb_serv == 0:
		return capacite

	if nb_serv == 1:
		return capacite

	return capacite + 1000 - maxscore


def worstPool(servers):
	poolsWithScore = [poolscore(servers, p) for p in range(P)]
	poolsWithScore_enum = enumerate(poolsWithScore)
	sortedpools = sorted(poolsWithScore_enum, key=lambda pool_p: pool_p[1])
	return sortedpools[0]


def fitness(servers):
	return worstPool(servers)[1]


def writesol():
	# print solution
	for m10 in range(M):
		if BestServersSol[m10].r == 'x':
			outf.write('x\n')
		else:
			outf.write(str(ServersSol[m10].r) + ' ' + str(ServersSol[m10].s) + ' ' + str(ServersSol[m10].p) + '\n')


def copySol(orig, dest):
	for m11 in range(M):
		dest[m11].r = orig[m11].r
		dest[m11].s = orig[m11].s
		dest[m11].p = orig[m11].p
		dest[m11].c = orig[m11].c
	return dest


def assign(m):

	# assign to a row
	# assign to best pool
	assigned = False
	row_c = 0
	slot_c = -1

	while not assigned:
		slot_c += 1
		if slot_c == S:
			slot_c = -1
			row_c += 1
			continue

		if row_c == R:
			break

		isPossible = True

		for p in range(serv[0]):
			if not isPossible:
				break

			if (p + slot_c) >= S:
				isPossible = False
				break

			if SlotsMap_c[row_c][p + slot_c] == -1:
				isPossible = False
				break

			if SlotsMap_c[row_c][p + slot_c] == 1:
				isPossible = False
				break

		if isPossible:
			# assign to best pool choice
			# maybe try a random pool

			bestPoolpos = worstPool(ServersSol)[0]
			print("bestPoolpos: " + str(bestPoolpos) + " score: " + str(poolscore(ServersSol, bestPoolpos)))

			# ServersSol write
			newServer = SolServer(row_c, slot_c, bestPoolpos, serv[1])
			ServersSol[servTup[0]] = newServer
			# BestServersSol write
			newServer2 = SolServer(row_c, slot_c, bestPoolpos, serv[1])
			BestServersSol[servTup[0]] = newServer2

			# fill map_c
			for p in range(serv[0]):
				SlotsMap_c[row_c][p + slot_c] = 1

			assigned = True

	if not assigned:
		ServersSol[servTup[0]] = SolServer('x', 0, 0, 0)

itera = 0

# 1 Heuristic
for m in range(M):
	servTup = SortedServers[m]
	serv = servTup[1]
	assign(m)

copySol(ServersSol, BestServersSol)

# 2 refine
while itera < 40:
	itera += 1
	print("Itera", itera)

	if itera % 10 == 0:
		copySol(BestServersSol, ServersSol)

	print("Going to refine a bit...")
	for r5 in range(R):
		for s5 in range(S):
			continuousCursor_b = 0
			continuousCursor_e = 0
			if SlotsMap_c[r5][s5] == -1:
				continuousCursor_b = s5
				continuousCursor_e = continuousCursor_b + 1

			elif SlotsMap_c[r5][s5] == 0:
				# find a continuous place. Have a random chance to replace it with random servers Taken From a random place
				while continuousCursor_e < S or SlotsMap_c[r5][continuousCursor_e] != -1:
					continuousCursor_e += 1

				for m5 in range(M):
					if ServersSol[m5].r == r5 and continuousCursor_b <= ServersSol[m5].s <= continuousCursor_e:
						if random.randrange(1, 10+1) >= 3:
							ServersSol[m5] = SolServer('u', 0, 0, 0)  # unassign

	m = 0
	while ServersSol[m].r != 'u' and ServersSol[m].r != 'x':
		m = random.randrange(0, M)
	assign(m)

	if fitness(ServersSol) > fitness(BestServersSol):
		copySol(ServersSol, BestServersSol)


writesol()
inf.close()
outf.close()