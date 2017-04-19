# pylint: disable=C0103,C0111,C0321,C0301,W0603,W0201,W0621
import sys
from Queue import PriorityQueue, Queue
from datetime import datetime
NROW, NCOL = 20, 30
INF = 9999
numberOfPlayers = int(sys.stdin.readline())
meId = int(sys.stdin.readline()) - 1
class Game(object):
    turn = 0
    @staticmethod
    def readTable():
        for row in range(0, NROW):
            rowString = sys.stdin.readline()
            for col in range(0, NCOL):
                table.update(Point(row, col), int(rowString[col]))
        for playerId in range(numberOfPlayers):
            coord = sys.stdin.readline().split(' ')
            players[playerId].updatePos(int(coord[0]), int(coord[1]))
        Game.turn += 1
    @staticmethod
    def writeMove(move):
        sys.stdout.write('%s\n' %move)
class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self):
        return '%d %d' %(self.x, self.y)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __ne__(self, other):
        return not self.__eq__(other)
    def distTo(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    def adjacentPoints(self):
        res = []
        if self.x > 0: res.append(Point(self.x - 1, self.y))
        if self.y < NCOL - 1: res.append(Point(self.x, self.y + 1))
        if self.x < NROW - 1: res.append(Point(self.x + 1, self.y))
        if self.y > 0: res.append(Point(self.x, self.y - 1))
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
class Player(object):
    def __init__(self, id):
        self.id = id
        self.baseId = id * 2 + 1
        self.unstableId = id * 2 + 2
    def updatePos(self, x, y):
        self.pos = Point(x, y)
    def distanceToTileId(self, tileId): # => (dist, nextTile, targetTile)
        s = self.pos
        if table.get(s) == tileId: return (0, s, s)
        q = Queue()
        trace = [[Point.placeholder for x in range(NCOL)] for y in range(NROW)]
        q.put((s, 0))
        trace[s.x][s.y] = s
        while not q.empty():
            qNode = q.get()
            u, du = qNode[0], qNode[1]
            for v in u.adjacentPoints():
                if table.get(v) == self.unstableId or trace[v.x][v.y] != Point.placeholder: continue
                trace[v.x][v.y] = u
                if table.get(v) == tileId:
                    _v = v
                    while trace[_v.x][_v.y] != s:
                        _v = trace[_v.x][_v.y]
                    return (du + 1, _v, v)
                q.put((v, du + 1))
        return (INF, Point.placeholder, Point.placeholder)
    def distanceToBase(self):
        return self.distanceToTileId(self.baseId)
    def distanceToKill(self, targetId):
        targetUnstableId = targetId * 2 + 2
        return self.distanceToTileId(targetUnstableId)
class MyPlayer(Player):
    pass
    # def move(self, direction):
    #     x, y = self.pos.x, self.pos.y
    #     if direction == 'UP': self.updatePos(x - 1, y)
    #     elif direction == 'RIGHT': self.updatePos(x, y + 1)
    #     elif direction == 'DOWN': self.updatePos(x + 1, y)
    #     elif direction == 'LEFT': self.updatePos(x, y - 1)
class Enemy(Player):
    def __init__(self, id):
        Player.__init__(self, id)
        self.behavior = 'active'
class Table(object):
    def __init__(self):
        self.val = [[0 for x in range(NCOL)] for y in range(NROW)]
    def update(self, a, val):
        self.val[a.x][a.y] = val
    def get(self, a):
        return self.val[a.x][a.y]
    def distanceForPlayer(self, s, t, playerId): # implement A*, return INF if there is not a way
        if s == t: return (0, s)
        q = PriorityQueue()
        trace = [[Point.placeholder for x in range(NCOL)] for y in range(NROW)]
        q.put((s.distTo(t), s, 0))
        trace[s.x][s.y] = s
        unstableId = playerId * 2 + 2
        while not q.empty():
            qNode = q.get()
            u, du = qNode[1], qNode[2]
            for v in u.adjacentPoints():
                if self.get(v) == unstableId or trace[v.x][v.y] != Point.placeholder: continue
                trace[v.x][v.y] = u
                if v == t:
                    _v = v
                    while trace[_v.x][_v.y] != s:
                        _v = trace[_v.x][_v.y]
                    return (du + 1, _v)
                q.put((v.distTo(t), v, du + 1))
        return (INF, Point.placeholder)
    def isBaseEdge(self, u, baseId):
        for v in u.adjacentPoints():
            if self.get(v) == baseId: return True
        return False
class Strategy(object):
    def __init__(self):
        self.type = 'patrol'
        self.nextType = 'patrol'
        self.patrolIndex = 0
        self.patrolPattern = ['LEFT', 'DOWN', 'RIGHT', 'UP']
    def setStrat(self, strat, nextStrat):
        self.type = strat
        self.nextType = nextStrat
    def endStrat(self):
        self.type = self.nextType
    def patrolNext(self):
        move = self.patrolPattern[self.patrolIndex]
        self.patrolIndex = (self.patrolIndex + 1) % len(self.patrolPattern)
        return move
strategy = Strategy()

table = Table()
players = []
for i in range(numberOfPlayers):
    if i == meId: players.append(MyPlayer(i))
    else: players.append(Enemy(i))
me = players[meId]
for i in range(numberOfPlayers):
    if i != meId:
        you = players[i]
        break

def initFirstTurn():
    strategy.pathIdx = 0
    strategy.setStrat('path', 'patrol')
    if me.pos.y > 2:
        strategy.path = ['LEFT', 'LEFT', 'DOWN', 'LEFT', 'UP', 'UP', 'RIGHT', 'RIGHT']
    else:
        strategy.path = ['RIGHT', 'RIGHT', 'DOWN', 'RIGHT', 'UP', 'UP', 'LEFT', 'LEFT']

def debug():
    pass

while True:
    Game.readTable()
    if strategy.type != 'attack' and strategy.type != 'flee':
        if me.distanceToKill(you.id)[0] < you.distanceToBase()[0]:
            strategy.setStrat('attack', 'flee')

    if strategy.type == 'patrol':
        Game.writeMove(strategy.patrolNext())
    elif strategy.type == 'attack':
        (dist, nextTile, targetTile) = me.distanceToKill(you.id)
        if dist == INF:
            strategy.endStrat()
        else:
            move = Point.getDirection(me.pos, nextTile)
            Game.writeMove(move)
        