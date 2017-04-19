# pylint: disable=C0103,C0111,C0321,C0301,W0603,W0201,W0621
import sys
from Queue import PriorityQueue, Queue
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
                table.update(Tile(row, col), int(rowString[col]))
        for playerId in range(numberOfPlayers):
            coord = sys.stdin.readline().split(' ')
            players[playerId].updatePos(int(coord[0]), int(coord[1]))
        Game.turn += 1
    @staticmethod
    def writeMove(move): sys.stdout.write('%s\n' %move)

class Tile(object):
    def __init__(self, x, y): self.x, self.y = x, y
    def __repr__(self): return '%d %d' %(self.x, self.y)
    def __eq__(self, other): return self.x == other.x and self.y == other.y
    def __ne__(self, other): return not self.__eq__(other)
    def distTo(self, other): return abs(self.x - other.x) + abs(self.y - other.y)
    def adjacentTiles(self):
        res = []
        if self.x > 0: res.append(Tile(self.x - 1, self.y))
        if self.y < NCOL - 1: res.append(Tile(self.x, self.y + 1))
        if self.x < NROW - 1: res.append(Tile(self.x + 1, self.y))
        if self.y > 0: res.append(Tile(self.x, self.y - 1))
        return res
    @staticmethod
    def getDirection(a, b):
        if abs(a.x - b.x) > 1 or abs(a.y - b.y) > 1: return 'INVALID'
        if a == b: return 'STILL'
        if a.x - b.x == 1: return 'UP'
        if a.x - b.x == -1: return 'DOWN'
        if a.y - b.y == 1: return 'LEFT'
        if a.y - b.y == -1: return 'RIGHT'
    def distanceToTile(self, player, t): # implement A*, return INF if there is not a way
        s = self
        if s == t: return (0, s)
        q = PriorityQueue()
        trace = [[Tile.placeholder for x in range(NCOL)] for y in range(NROW)]
        q.put((s.distTo(t), s, 0))
        trace[s.x][s.y] = s
        while not q.empty():
            qNode = q.get()
            u, du = qNode[1], qNode[2]
            for v in Tile.adjacentTiles(u):
                if table.get(v) == player.unstableId or trace[v.x][v.y] != Tile.placeholder: continue
                trace[v.x][v.y] = u
                if v == t:
                    _v = v
                    while trace[_v.x][_v.y] != s:
                        _v = trace[_v.x][_v.y]
                    return (du + 1, _v)
                q.put((v.distTo(t), v, du + 1))
        return (INF, Tile.placeholder)
    def distanceToSomeTile(self, player, predicate): # => (dist, nextTile, targetTile)
        s = self
        if predicate(s): return (0, s, s)
        q = Queue()
        trace = [[Tile.placeholder for y in range(NCOL)] for x in range(NROW)]
        q.put((s, 0))
        trace[s.x][s.y] = s
        while not q.empty():
            qNode = q.get()
            u, du = qNode[0], qNode[1]
            for v in u.adjacentTiles():
                if table.get(v) == player.unstableId or trace[v.x][v.y] != Tile.placeholder: continue
                trace[v.x][v.y] = u
                if predicate(v):
                    _v = v
                    while trace[_v.x][_v.y] != s:
                        _v = trace[_v.x][_v.y]
                    return (du + 1, _v, v)
                q.put((v, du + 1))
        return (INF, Tile.placeholder, Tile.placeholder)
    def distanceToBase(self, player): return self.distanceToSomeTile(player, lambda u: table.get(u) == player.baseId)
    def distanceToUnoccupied(self, player): return self.distanceToSomeTile(player, lambda u: table.get(u) != player.baseId)
    def distanceToKill(self, player, target): return self.distanceToSomeTile(player, lambda u: table.get(u) == target.unstableId)
Tile.placeholder = Tile(-1, -1)

class Player(object):
    def __init__(self, id):
        self.id = id
        self.baseId = id * 2 + 1
        self.unstableId = id * 2 + 2
        self.pos = Tile.placeholder
    def updatePos(self, x, y):
        self.lastPos = self.pos
        self.pos = Tile(x, y)
    def distanceToTile(self, tile): return self.pos.distanceToTile(self, tile)
    def distanceToBase(self): return self.pos.distanceToBase(self)
    def distanceToUnoccupied(self): return self.pos.distanceToUnoccupied(self)
    def distanceToKill(self, target): return self.pos.distanceToKill(self, target)
    def inBase(self): return table.get(self.pos) == self.baseId
    def numberOfUnstableTiles(self):
        res = 0
        for i in range(NROW):
            for j in range(NCOL):
                if table.get(Tile(i, j)) == self.unstableId: res += 1
        return res
class MyPlayer(Player):
    def moveToAdjTile(self, tile):
        move = Tile.getDirection(self.pos, tile)
        Game.writeMove(move)
    def moveToAdjTileReverse(self, tile):
        move = Tile.getDirection(self.pos, tile)
        x, y = self.pos.x, self.pos.y
        if move == 'LEFT': move = 'RIGHT' if y < NCOL-1 else 'UP' if x > 0 else 'DOWN'
        elif move == 'RIGHT': move = 'LEFT' if y > 0 else 'UP' if x > 0 else 'DOWN'
        elif move == 'UP': move = 'DOWN' if x < NROW-1 else 'LEFT' if y > 0 else 'RIGHT'
        elif move == 'DOWN': move = 'UP' if x > 0 else 'LEFT' if y > 0 else 'RIGHT'
        Game.writeMove(move)
class Enemy(Player):
    def __init__(self, id):
        Player.__init__(self, id)
        self.behavior = 'active'
class Table(object):
    def __init__(self): self.val = [[0 for x in range(NCOL)] for y in range(NROW)]
    def update(self, a, val): self.val[a.x][a.y] = val
    def get(self, a): return self.val[a.x][a.y]
    def isNearBase(self, tile, player):
        for v in tile.adjacentTiles():
            if self.get(v) == player.baseId: return True
        return False
table = Table()
class Strategy(object):
    def __init__(self):
        self.type = 'approach'
        self.patrolIndex = 0
        self.patrolPattern = ['LEFT', 'UP', 'RIGHT', 'DOWN']
        self.minimumSafeDistance = 6
    def setStrat(self, strat):
        self.type = strat
        if strat == 'patrol':
            if me.pos.x > 0 and me.pos.y > 0: self.patrolPattern = ['LEFT', 'UP', 'RIGHT', 'DOWN']
            else: self.patrolPattern = ['RIGHT', 'DOWN', 'LEFT', 'UP']
    def patrolNext(self):
        move = self.patrolPattern[self.patrolIndex]
        self.patrolIndex = (self.patrolIndex + 1) % len(self.patrolPattern)
        return move
strategy = Strategy()

players = []
for i in range(numberOfPlayers):
    if i == meId: players.append(MyPlayer(i))
    else: players.append(Enemy(i))
me = players[meId]
for i in range(numberOfPlayers):
    if i != meId:
        you = players[i]
        break

def debug():
    print me.distanceToKill(you)
    print you.distanceToBase()

while True:
    Game.readTable()

    if me.inBase():
        (dist, nextTile, targetTile) = me.distanceToUnoccupied()
        me.moveToAdjTile(nextTile)
    elif me.numberOfUnstableTiles() == 1:
        nextTiles = [v for v in me.pos.adjacentTiles() if v != me.lastPos]
        nextTiles.sort(key=lambda u: u.distanceToBase(me))
        me.moveToAdjTile(nextTiles[0])
    else:
        (dist, nextTile, targetTile) = me.distanceToBase()
        me.moveToAdjTile(nextTile)
        