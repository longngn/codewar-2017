# pylint: disable=C0103,C0111,C0321,C0301,W0603,W0201,W0621
import sys
from Queue import PriorityQueue, Queue
from copy import deepcopy
NROW, NCOL = 20, 30
INF = 9999
MAX_TURN = 1000
numberOfPlayers = int(sys.stdin.readline())
meId = int(sys.stdin.readline()) - 1
class Util(object):
    @staticmethod
    def pickAtLeastOne(sequence, predicate):
        for element in sequence:
            if predicate(element): return element
        return sequence[0]
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
class Table(object):
    def __init__(self): self.val = [[0 for x in range(NCOL)] for y in range(NROW)]
    def __repr__(self):
        res = ''
        for x in range(NROW):
            for y in range(NCOL):
                res += str(self.get(Tile(x, y)))
            res += '\n'
        return res
    def update(self, a, val): self.val[a.x][a.y] = val
    def get(self, a): return self.val[a.x][a.y]
    def withPathToBaseOf(self, player, pos):
        resTable = deepcopy(self)
        pathToBase = pos.distToBaseOf(player)[1]
        pathToBase.append(pos)
        for tile in pathToBase:
            resTable.update(tile, player.unstableId)
        return resTable
table = Table()
class Tile(object):
    def __init__(self, x, y): self.x, self.y = x, y
    def __repr__(self): return '%d %d' %(self.x, self.y)
    def __eq__(self, other): return self.x == other.x and self.y == other.y
    def __ne__(self, other): return not self.__eq__(other)
    def manDistTo(self, other): return abs(self.x - other.x) + abs(self.y - other.y)
    def adjacentTiles(self):
        res = []
        if self.x > 0: res.append(Tile(self.x - 1, self.y))
        if self.y > 0: res.append(Tile(self.x, self.y - 1))
        if self.x < NROW - 1: res.append(Tile(self.x + 1, self.y))
        if self.y < NCOL - 1: res.append(Tile(self.x, self.y + 1))
        return res
    @staticmethod
    def getDirection(a, b):
        if a.x - b.x == 1: return 'UP'
        if a.x - b.x == -1: return 'DOWN'
        if a.y - b.y == 1: return 'LEFT'
        if a.y - b.y == -1: return 'RIGHT'
        return 'LEFT'
    def shouldAvoid(self, player, table=table):
        if table.get(self) == player.unstableId: return True
        if table.get(player.pos) == player.unstableId and self == player.lastPos: return True
        return False
    def isEncircled(self, player, table):
        s = self
        q = Queue()
        q.put((s, 0))
        trace = [[Tile.placeholder for x in range(NCOL)] for y in range(NROW)]
        trace[s.x][s.y] = s
        while not q.empty():
            (u, du) = q.get()
            for v in u.adjacentTiles():
                # THE CODE BELOW IS IMPROVISED, REFACTOR LATER!!!!!
                if table.get(v) in [player.baseId, player.unstableId, you.unstableId] or trace[v.x][v.y] != Tile.placeholder: continue
                if v.isTableEdge(): return False
                trace[v.x][v.y] = u
                q.put((v, du + 1))
        return True
    def distToSomeTile(self, player, predicate, table=table): # => (dist, path)
        s = self
        path = []
        if predicate(s): return (0, path)
        q = Queue()
        trace = [[Tile.placeholder for y in range(NCOL)] for x in range(NROW)]
        q.put((s, 0))
        trace[s.x][s.y] = s
        while not q.empty():
            (u, du) = q.get()
            for v in u.adjacentTiles():
                if v.shouldAvoid(player, table) or trace[v.x][v.y] != Tile.placeholder: continue
                trace[v.x][v.y] = u
                if predicate(v):
                    _v = v
                    while trace[_v.x][_v.y] != s:
                        path.append(_v)
                        _v = trace[_v.x][_v.y]
                    path.append(_v)
                    path.reverse()
                    return (du + 1, path)
                q.put((v, du + 1))
        return (INF, path)
    def distToBaseOf(self, player): return self.distToSomeTile(player, lambda u: u.inBaseOf(player))
    def distToKill(self, player, target, table=table): return self.distToSomeTile(player, lambda u: table.get(u) == target.unstableId)
    def inBaseOf(self, player): return table.get(self) == player.baseId
    def isTableEdge(self): return self.x == 0 or self.x == NROW-1 or self.y == 0 or self.y == NCOL-1
    def distToUnoccupied(self, player): return self.distToSomeTile(player, lambda u: not u.inBaseOf(player))
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
    def distToBase(self): return self.pos.distToBaseOf(self)
    def distToKill(self, target, table=table): return self.pos.distToKill(self, target, table)
    def distToUnoccupied(self): return self.pos.distToUnoccupied(self)
    def inBase(self): return table.get(self.pos) == self.baseId
    def viableTiles(self): return [t for t in self.pos.adjacentTiles() if not t.shouldAvoid(self)]
class MyPlayer(Player):
    def moveToAdjTile(self, tile):
        move = Tile.getDirection(self.pos, tile)
        Game.writeMove(move)
class Enemy(Player):
    pass

players = []
for i in range(numberOfPlayers):
    if i == meId: players.append(MyPlayer(i))
    else: players.append(Enemy(i))
me = players[meId]
for i in range(numberOfPlayers):
    if i != meId:
        you = players[i]
        break
observer = Player(-10)
observer.lastPos = Tile(-2, -2)

while True:
    Game.readTable()

    def riskLevel(t):
        hypoTable = table.withPathToBaseOf(me, t)
        (backDist, backPath) = t.distToBaseOf(me)
        killDist = you.pos.distToKill(observer, me, table=hypoTable)[0]
        if len(backPath) > 0: killDist = min(killDist, you.pos.manDistTo(backPath[-1]) - 1)
        return 0 if killDist > backDist + 1 else 1
    if me.inBase():
        tiles = me.viableTiles()
        tiles.sort(key=lambda t: t.distToUnoccupied(me)[0])
        def safeNextTile(t):
            if t.inBaseOf(me): return t.manDistTo(you.pos) > 2
            me.lastPos = me.pos
            return riskLevel(t) == 0
        tile = Util.pickAtLeastOne(tiles, safeNextTile)
        me.moveToAdjTile(tile)
    else:
        tiles = me.viableTiles()
        def punctualLevel(t):
            d = t.distToBaseOf(me)[0]
            return 0 if d < MAX_TURN - Game.turn else 1
        hypoTable = table.withPathToBaseOf(me, me.pos)
        def outsideLevel(t):
            if hypoTable.get(t) == me.unstableId: return 1
            if t.isEncircled(me, hypoTable): return 2
            return 0
        tiles.sort(key=lambda t: (riskLevel(t), punctualLevel(t), outsideLevel(t), -t.distToBaseOf(me)[0], -t.manDistTo(you.pos)))
        if riskLevel(tiles[0]) == 1: tiles.sort(key=lambda t: t.distToBaseOf(me)[0])
        me.moveToAdjTile(tiles[0])
        