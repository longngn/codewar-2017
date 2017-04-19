# pylint: disable=all
import sys
import Queue
from datetime import datetime
from random import shuffle
NROW, NCOL = 20, 30
INF = 9999
numberOfPlayers = int(sys.stdin.readline())
myPlayerId = int(sys.stdin.readline()) - 1
def readTable():
    for row in range(0, NROW):
        rowString = sys.stdin.readline()
        for col in range(0, NCOL):
            table.update(row, col, int(rowString[col]))
    for playerId in range(numberOfPlayers):
        coord = sys.stdin.readline().split(' ')
        players[playerId].updatePos(int(coord[0]), int(coord[1]))
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self):
        return '%d %d' %(self.x, self.y)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __ne__(self, other):
        return not self.__eq__(other)
    @staticmethod
    def adjacentPoints(a):
        res = []
        if a.x > 0: res.append(Point(a.x - 1, a.y))
        if a.y > 0: res.append(Point(a.x, a.y - 1))
        if a.x < NROW - 1: res.append(Point(a.x + 1, a.y))
        if a.y < NCOL - 1: res.append(Point(a.x, a.y + 1))
        return res
    @staticmethod
    def getDirection(a, b):
        if abs(a.x - b.x) > 1 or abs(a.y - b.y) > 1: return 'INVALID'
        if a == b: return 'STILL'
        if a.x - b.x == 1: return 'UP'
        if a.x - b.x == -1: return 'DOWN'
        if a.y - b.y == 1: return 'LEFT'
        if a.y - b.y == -1: return 'RIGHT'
Point.placeholder = Point(-1, -1)
class Player:
    def __init__(self, id):
        self.id = id
        self.baseId = id * 2 + 1
        self.unstableId = id * 2 + 2
    def updatePos(self, x, y):
        self.pos = Point(x, y)
    def distanceToTileId(self, tileId):
        res = INF
        nearestTile = Point.placeholder
        for x in range(NROW): 
            for y in range(NCOL):
                if table.get(x, y) == tileId:
                    d = table.distanceForPlayer(self.pos, Point(x, y), self.id)[0]
                    if d != INF and (res == INF or d < res): 
                        res = d
                        nearestTile = Point(x, y)
        return (res, nearestTile)
    def distanceToBase(self):
        return self.distanceToTileId(self.baseId)
    def distanceToKill(self, targetId):
        targetUnstableId = targetId * 2 + 2
        return self.distanceToTileId(targetUnstableId)
class MyPlayer(Player):
    def __init__(self, id):
        Player.__init__(self, id)
    def move(self, direction):
        x, y = self.pos.x, self.pos.y
        if direction == 'LEFT': self.updatePos(x, y - 1)
        elif direction == 'RIGHT': self.updatePos(x, y + 1)
        elif direction == 'UP': self.updatePos(x - 1, y)
        elif direction == 'DOWN': self.updatePos(x + 1, y)
class Table:
    def __init__(self):
        self.val = [[0 for x in range(NCOL)] for y in range(NROW)]
    def update(self, x, y, val):
        self.val[x][y] = val
    def get(self, x, y):
        return self.val[x][y]
    def distanceForPlayer(self, s, t, playerId): # implement BFS, return INF if there is not a way
        if s == t: return (0, s)
        q = Queue.Queue()
        trace = [[Point.placeholder for x in range(NCOL)] for y in range(NROW)]
        q.put((s, 0))
        trace[s.x][s.y] = s
        unstableId = playerId * 2 + 2
        while not q.empty():
            qNode = q.get()
            u, du = qNode[0], qNode[1]
            for v in Point.adjacentPoints(u):
                if self.get(v.x, v.y) == unstableId or trace[v.x][v.y] != Point.placeholder: continue
                trace[v.x][v.y] = u
                if v == t:
                    _v = v
                    while trace[_v.x][_v.y] != s:
                        _v = trace[_v.x][_v.y]
                    del q
                    return (du + 1, _v)
                q.put((v, du + 1))
        del q
        return (INF, Point(-1, -1))
class State:
    type = 'def'

table = Table()
players = [Player(i) for i in range(numberOfPlayers)]
players[myPlayerId] = MyPlayer(myPlayerId)
myPlayer = players[myPlayerId]
enemies = []
for i in range(numberOfPlayers):
    if i != myPlayerId: enemies.append(players[i])

def initFirstTurn():
    State.pathIdx = 0
    State.type = 'path'
    if myPlayer.pos.y > 1:
        State.path = ['LEFT', 'LEFT', 'UP', 'RIGHT']
    else:
        State.path = ['RIGHT', 'RIGHT', 'UP', 'LEFT']

def debug():
    print myPlayerId
    print myPlayer.baseId

def writeMove(move):
    sys.stdout.write('%s\n' %move)
firstTurn = True
while True:
    readTable()
    prevTime = datetime.now()
    if firstTurn:
        firstTurn = False
        initFirstTurn()
    if State.type != 'atk':
        for enemy in enemies:
            if myPlayer.distanceToKill(enemy.id)[0] < enemy.distanceToBase()[0]:
                State.type = 'atk'
                State.preyId = enemy.id
    if State.type == 'def':
        move = 'NONE'
        adj = Point.adjacentPoints(myPlayer.pos)
        shuffle(adj)
        for v in adj:
            if table.get(v.x, v.y) == myPlayer.baseId:
                move = Point.getDirection(myPlayer.pos, v)
                break
        writeMove(move)
    elif State.type == 'atk':
        targetTile = myPlayer.distanceToKill(State.preyId)[1]
        next = table.distanceForPlayer(myPlayer.pos, targetTile, myPlayer.id)[1]
        move = Point.getDirection(myPlayer.pos, next)
        writeMove(move)
    elif State.type == 'path':
        if State.pathIdx == len(State.path) - 1: State.type = 'def'
        writeMove(State.path[State.pathIdx])
        State.pathIdx += 1
    print datetime.now() - prevTime
