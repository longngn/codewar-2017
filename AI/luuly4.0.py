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
        if abs(a.x - b.x) > 1 or abs(a.y - b.y) > 1: return 'INVALID'
        if a == b: return 'STILL'
        if a.x - b.x == 1: return 'UP'
        if a.x - b.x == -1: return 'DOWN'
        if a.y - b.y == 1: return 'LEFT'
        if a.y - b.y == -1: return 'RIGHT'
    def shouldAvoid(self, player, table=table):
        if table.get(self) == player.unstableId: return True
        if table.get(player.pos) == player.unstableId and self == player.lastPos and self.isBaseOf(player): return True
        return False
    def getAllSurroundingTiles(self, player, predicate):
        s = self
        q = Queue()
        q.put(s)
        trace = [[Tile.placeholder for x in range(NCOL)] for y in range(NROW)]
        trace[s.x][s.y] = s
        res = []
        while not q.empty():
            u = q.get()
            for v in u.adjacentTiles():
                if v.shouldAvoid(player) or trace[v.x][v.y] != Tile.placeholder: continue
                trace[v.x][v.y] = u
                if predicate(v): res.append(v)
                else: q.put(v)
        return res
    def isEncircled(self, player, table):
        s = self
        q = Queue()
        q.put(s)
        trace = [[Tile.placeholder for x in range(NCOL)] for y in range(NROW)]
        trace[s.x][s.y] = s
        while not q.empty():
            u = q.get()
            for v in u.adjacentTiles():
                # THE CODE BELOW IS IMPROVISED, REFACTOR LATER!
                if table.get(v) in [player.baseId, player.unstableId, you.unstableId] or trace[v.x][v.y] != Tile.placeholder: continue
                if v.isTableEdge(): return False
                trace[v.x][v.y] = u
                q.put(v)
        return True
    def distTo(self, player, target): # implement A*, => (dist, nextTile)
        s = self
        if isinstance(target, Player): t = target.pos
        else: t = target
        if s == t: return (0, s)
        q = PriorityQueue()
        trace = [[Tile.placeholder for x in range(NCOL)] for y in range(NROW)]
        q.put((s.manDistTo(t), s, 0))
        trace[s.x][s.y] = s
        while not q.empty():
            (_, u, du) = q.get()
            for v in u.adjacentTiles():
                if v.shouldAvoid(player) or trace[v.x][v.y] != Tile.placeholder: continue
                trace[v.x][v.y] = u
                if v == t:
                    _v = v
                    while trace[_v.x][_v.y] != s:
                        _v = trace[_v.x][_v.y]
                    return (du + 1, _v)
                q.put((v.manDistTo(t), v, du + 1))
        return (INF, Tile.placeholder)
    def distToSomeTile(self, player, predicate, _skip=0, table=table): # => (dist, path)
        skip = _skip
        s = self
        path = []
        q = Queue()
        trace = [[Tile.placeholder for y in range(NCOL)] for x in range(NROW)]
        q.put((s, 0))
        trace[s.x][s.y] = s
        while not q.empty():
            (u, du) = q.get()
            if predicate(u):
                if skip == 0:
                    _u = u
                    while trace[_u.x][_u.y] != s:
                        path.append(_u)
                        _u = trace[_u.x][_u.y]
                    path.append(_u)
                    path.reverse()
                    return (du, path)
                else: skip -= 1
            for v in u.adjacentTiles():
                if v.shouldAvoid(player, table) or trace[v.x][v.y] != Tile.placeholder: continue
                trace[v.x][v.y] = u
                q.put((v, du + 1))
        return (INF, path)
    def distToBaseOf(self, player): return self.distToSomeTile(player, lambda u: u.isBaseOf(player))
    def distToKill(self, player, target, table=table): return self.distToSomeTile(player, lambda u: table.get(u) == target.unstableId)
    def isBaseOf(self, player): return table.get(self) == player.baseId
    def isTableEdge(self): return self.x == 0 or self.x == NROW-1 or self.y == 0 or self.y == NCOL-1
    def distToUnoccupied(self, player, skip=0): return self.distToSomeTile(player, lambda u: not u.isBaseOf(player), skip)
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
    def distToBaseOf(self): return self.pos.distToBaseOf(self)
    def distToKill(self, target, table=table): return self.pos.distToKill(self, target, table)
    def distToUnoccupied(self, skip=0): return self.pos.distToUnoccupied(self, skip)
    def inBase(self): return table.get(self.pos) == self.baseId
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
        nextTile = me.distToBaseOf()[1]
        me.moveToAdjTile(nextTile)
class Enemy(Player):
    pass
class Strategy(object):
    def __init__(self):
        self.targetTile = Tile.placeholder
    def setTargetTile(self):
        unoccupiedTiles = me.pos.getAllSurroundingTiles(me, lambda u: not u.isBaseOf(me))
        resTile = Tile.placeholder
        maxScore = -INF
        for tile in unoccupiedTiles:
            tileScore = Strategy.getUnoccupiedTileScore(tile)
            if tileScore > maxScore:
                maxScore = tileScore
                resTile = tile
        self.targetTile = resTile
    @staticmethod
    def getUnoccupiedTileScore(t):
        potentialWidth, potentialHeight = -1, -1
        i = t.x
        while i >= 0 and not Tile(i, t.y).isBaseOf(me):
            i -= 1
            potentialHeight += 1
        i = t.x
        while i < NROW and not Tile(i, t.y).isBaseOf(me):
            i += 1
            potentialHeight += 1
        i = t.y
        while i >= 0 and not Tile(t.x, i).isBaseOf(me):
            i -= 1
            potentialWidth += 1
        i = t.y
        while i < NCOL and not Tile(t.x, i).isBaseOf(me):
            i += 1
            potentialWidth += 1
        # print 'tile %s: potentialW %d potentialH %d score %d' %(t, potentialWidth, potentialHeight, potentialHeight * potentialWidth + t.manDistTo(you.pos) ** 2 - t.manDistTo(me.pos) ** 2)
        return potentialHeight * potentialWidth + t.manDistTo(you.pos) ** 2 - t.manDistTo(me.pos) ** 2
strat = Strategy()

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

    if me.inBase():
        if strat.targetTile == Tile.placeholder or strat.targetTile.isBaseOf(me): strat.setTargetTile()
        tiles = me.viableTiles()
        tiles.sort(key=lambda t: t.manDistTo(strat.targetTile))
        tile = Util.pickAtLeastOne(tiles, lambda t: t.distTo(me, you)[0] > 2)
        if tile != tiles[0]: strat.setTargetTile()
        me.moveToAdjTile(tile)
    else:
        tiles = me.viableTiles()
        def riskLevel(t):
            hypoTable = table.withPathToBaseOf(me, t)
            # print hypoTable
            (backDist, backPath) = t.distToBaseOf(me)
            killDist = you.pos.distToKill(observer, me, table=hypoTable)[0]
            if len(backPath) > 0: killDist = min(killDist, you.pos.manDistTo(backPath[-1]) - 1)
            # print 'tile %s: k %d b %d' %(t, killDist, backDist)
            return 0 if killDist > backDist + 1 else 1
        hypoTable = table.withPathToBaseOf(me, me.pos)
        def outsideLevel(t):
            if hypoTable.get(t) == me.unstableId: return 1
            if t.isEncircled(me, hypoTable): return 2
            return 0
        # tiles.sort(key=lambda t: (riskLevel(t), outsideLevel(t), -t.distTo(me, strat.lastPosInBase)[0], -t.distToBaseOf(me)[0], -t.distTo(me, you)[0]))
        tiles.sort(key=lambda t: (riskLevel(t), outsideLevel(t), -t.distTo(me, you)[0]))
        me.moveToAdjTile(tiles[0])
        