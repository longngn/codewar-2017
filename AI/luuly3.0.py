# pylint: disable=C0103,C0111,C0321,C0301,W0603,W0201,W0621
import sys
from Queue import PriorityQueue, Queue
NROW, NCOL = 20, 30
INF = 9999
MAX_FAILED_ATTACK = 10
numberOfPlayers = int(sys.stdin.readline())
meId = int(sys.stdin.readline()) - 1
class Util(object):
    @staticmethod
    def pickAtLeastOne(seq, pred):
        for ele in seq:
            if pred(ele): return ele
        return seq[0]
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
    def manhattanDist(self, other): return abs(self.x - other.x) + abs(self.y - other.y)
    def adjacentTiles(self):
        res = []
        if self.x > 0: res.append(Tile(self.x - 1, self.y))
        if self.y > 0: res.append(Tile(self.x, self.y - 1))
        if self.x < NROW - 1: res.append(Tile(self.x + 1, self.y))
        if self.y < NCOL - 1: res.append(Tile(self.x, self.y + 1))
        return res
    @staticmethod
    def getDirection(a, b):
        if abs(a.x - b.x) > 1 or abs(a.y - b.y) > 1: return 'INVALID'
        if a == b: return 'STILL'
        if a.x - b.x == 1: return 'UP'
        if a.x - b.x == -1: return 'DOWN'
        if a.y - b.y == 1: return 'LEFT'
        if a.y - b.y == -1: return 'RIGHT'
    def shouldAvoid(self, player):
        if table.get(self) == player.unstableId: return True
        if table.get(player.pos) == player.unstableId and self == player.lastPos and self.isBase(player): return True
        return False
    def distTo(self, player, target): # implement A*, return INF if there is not a way
        s = self
        if isinstance(target, Player): t = target.pos
        else: t = target
        if s == t: return (0, s)
        q = PriorityQueue()
        trace = [[Tile.placeholder for x in range(NCOL)] for y in range(NROW)]
        q.put((s.manhattanDist(t), s, 0))
        trace[s.x][s.y] = s
        while not q.empty():
            qNode = q.get()
            u, du = qNode[1], qNode[2]
            for v in Tile.adjacentTiles(u):
                if v.shouldAvoid(player) or trace[v.x][v.y] != Tile.placeholder: continue
                trace[v.x][v.y] = u
                if v == t:
                    _v = v
                    while trace[_v.x][_v.y] != s:
                        _v = trace[_v.x][_v.y]
                    return (du + 1, _v)
                q.put((v.manhattanDist(t), v, du + 1))
        return (INF, Tile.placeholder)
    def distToSomeTile(self, player, predicate): # => (dist, nextTile, targetTile)
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
                if v.shouldAvoid(player) or trace[v.x][v.y] != Tile.placeholder: continue
                trace[v.x][v.y] = u
                if predicate(v):
                    _v = v
                    while trace[_v.x][_v.y] != s:
                        _v = trace[_v.x][_v.y]
                    return (du + 1, _v, v)
                q.put((v, du + 1))
        return (INF, Tile.placeholder, Tile.placeholder)
    def distToBase(self, player): return self.distToSomeTile(player, lambda u: u.isBase(player))
    def distToKill(self, player, target): return self.distToSomeTile(player, lambda u: table.get(u) == target.unstableId)
    def isBase(self, player): return table.get(self) == player.baseId
    def isBaseCorner(self, player):
        if not self.isBase(player): return False
        adjTiles = self.adjacentTiles()
        adjBaseTiles = [t for t in adjTiles if t.isBase(player)]
        return len(adjBaseTiles) <= 2 and len(adjTiles) > 2
    def isNearBase(self, player):
        if self.isBase(player): return False
        for t in self.adjacentTiles():
            if t.isBase(player): return True
        return False
    def distToBaseCorner(self, player): return self.distToSomeTile(player, lambda u: u.isBaseCorner(player) and u.distTo(me, you)[0] > 7)
    def getPotentialTiles(self, player):
        if self.isBase(player): return 0
        res = 1 if self.isNearBase(player) else 0
        i, j = self.x - 1, self.y
        while i >= 0 and Tile(i, j).isNearBase(player):
            i -= 1
            res += 1
        i, j = self.x + 1, self.y
        while i < NROW and Tile(i, j).isNearBase(player):
            i += 1
            res += 1
        i, j = self.x, self.y - 1
        while j >= 0 and Tile(i, j).isNearBase(player):
            j -= 1
            res += 1
        i, j = self.x, self.y + 1
        while j < NCOL and Tile(i, j).isNearBase(player):
            j += 1
            res += 1
        return res
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
    def distTo(self, target): return self.pos.distTo(self, target)
    def distToBase(self): return self.pos.distToBase(self)
    def distToBaseCorner(self): return self.pos.distToBaseCorner(self)
    def distToKill(self, target): return self.pos.distToKill(self, target)
    def inBase(self): return table.get(self.pos) == self.baseId
    def inBaseCorner(self): return self.pos.isBaseCorner(self)
    def getNumberOfUnstableTiles(self):
        res = 0
        for i in range(NROW):
            for j in range(NCOL):
                if table.get(Tile(i, j)) == self.unstableId: res += 1
        return res
    def viableTiles(self): return [t for t in self.pos.adjacentTiles() if not t.shouldAvoid(self)]
class MyPlayer(Player):
    def moveToAdjTile(self, tile):
        move = Tile.getDirection(self.pos, tile)
        Game.writeMove(move)
    def moveToBase(self):
        nextTile = me.distToBase()[1]
        me.moveToAdjTile(nextTile)
class Enemy(Player):
    pass
class Table(object):
    def __init__(self): self.val = [[0 for x in range(NCOL)] for y in range(NROW)]
    def update(self, a, val): self.val[a.x][a.y] = val
    def get(self, a): return self.val[a.x][a.y]
table = Table()
class Strategy(object):
    def __init__(self):
        self.type = 'expand'
        self.failedAttacks = 0
    def setStrat(self, strat):
        self.type = strat
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
    print me.distToKill(you)
    print you.distToBase()

while True:
    Game.readTable()

    if strategy.type in ['expand', 'flee'] and strategy.failedAttacks < MAX_FAILED_ATTACK and you.getNumberOfUnstableTiles() > 2 and me.distToKill(you)[0] < you.distToBase()[0] + 3 and you.distToKill(me)[0] > me.distToBase()[0] + 3:
        strategy.setStrat('attack')
    if strategy.type == 'attack' and me.distToKill(you)[0] == INF or you.distToKill(me)[0] <= me.distToBase()[0] + 3:
        strategy.setStrat('flee')
        strategy.failedAttacks += 1
    if strategy.type == 'flee' and me.inBase():
        strategy.setStrat('expand')

    if strategy.type == 'expand':
        if me.inBaseCorner():
            tiles = me.viableTiles()
            tiles.sort(key=lambda t: -t.getPotentialTiles(me))
            def shouldGo(tile):
                d = tile.distTo(me, you)[0]
                p = tile.getPotentialTiles(me)
                if p <= 1: return d > 2
                else: return d > 4
            tile = Util.pickAtLeastOne(tiles, shouldGo)
            me.moveToAdjTile(tile)
        elif me.inBase():
            tiles = me.viableTiles()
            tiles.sort(key=lambda t: (t.distToBase(me)[0], t.distToBaseCorner(me)[0]))
            tile = Util.pickAtLeastOne(tiles, lambda t: t.distTo(me, you)[0] > 2)
            me.moveToAdjTile(tile)
        else:
            if me.pos.isNearBase(me):
                next, back = Tile.placeholder, Tile.placeholder
                for t in me.viableTiles():
                    if t.isNearBase(me): next = t
                    elif t.isBase(me): back = t
                if back != Tile.placeholder and next == Tile.placeholder or you.distToKill(me)[0] <= 3 or you.distTo(back)[0] <= 4: me.moveToAdjTile(back)
                else: me.moveToAdjTile(next)
            else: me.moveToBase()
    elif strategy.type == 'attack':
        nextTile = me.distToKill(you)[1]
        me.moveToAdjTile(nextTile)
    elif strategy.type == 'flee':
        me.moveToBase()