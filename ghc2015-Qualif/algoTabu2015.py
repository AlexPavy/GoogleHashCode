__author__ = 'Alex'

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
PoolsSol = [0 for p2 in range(P)]


class SolServer:
	def __init__(self, r, s, _p, c):
		self.r = r
		self.s = s
		self.p = _p
		self.c = c
		self.used = False

ServersSol = [SolServer(0, 0, 0, 0) for m1 in range(M)]  # positions

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


def poolscore(p4):
	capacite = 0
	maxscore = 0
	nb_serv = 0
	for r3 in range(R):
		rowscore = 0
		for m3 in range(M):
			if ServersSol[m3].r == r3:
				if ServersSol[m3].p == p4:
					if ServersSol[m3].c > 0:
						nb_serv += 1
					rowscore += ServersSol[m3].c

		maxscore = max(maxscore, rowscore)
		capacite += rowscore

	if nb_serv == 0:
		return capacite

	if nb_serv == 1:
		return capacite

	return capacite + 1000 - maxscore

score = 0
while score < 400:
	candidateList = []
	# add non-tabu neighbors
	# add server neighbor
	assigned = False


pool = 0
for m in range(M):

	servTup = SortedServers[m]
	serv = servTup[1]

	# assign to a row
	# assign to next pool
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
			# PoolsSol_enum = enumerate(PoolsSol)

			poolsWithScore = [poolscore(p) for p in range(P)]
			poolsWithScore_enum = enumerate(poolsWithScore)
			sortedpools = sorted(poolsWithScore_enum, key=lambda pool_p: pool_p[1])
			bestPoolpos = sortedpools[0][0]
			print("bestPoolpos: " + str(bestPoolpos) + " score: " + str(poolscore(bestPoolpos)))
			PoolsSol[bestPoolpos] += serv[1]  # add capacity of server

			# ServersSol write
			newServer = SolServer(row_c, slot_c, bestPoolpos, serv[1])
			newServer.used = True
			ServersSol[servTup[0]] = newServer

			# fill map_c
			for p in range(serv[0]):
				SlotsMap_c[row_c][p + slot_c] = 1

			assigned = True

	if not assigned:
		ServersSol[servTup[0]] = SolServer('x', 0, 0, 0)

	pool += 1  # maybe take the less gifted pool
	if pool == P:
		pool = 0

print("Going to refine a bit...")
for r5 in range(R):
	for s5 in range(S):
		if SlotsMap_c[r5][s5] == 0:
			for m5 in range(M):
				if ServersSol[m5].r == r5:
					if ServersSol[m5].s <= r5:

# print solution
for m in range(M):
	if ServersSol[m].r == 'x':
		outf.write('x\n')
	else:
		outf.write(str(ServersSol[m].r) + ' ' + str(ServersSol[m].s) + ' ' + str(ServersSol[m].p) + '\n')


inf.close()
outf.close()