# pylint: disable=all
import sys

NROW, NCOL = 20, 30

class player:
    def updatePos(self, row, col):
        self.row, self.col = row, col

numberOfPlayers = int(sys.stdin.readline())
myPlayerId = int(sys.stdin.readline()) - 1

table = [[0 for x in range(NCOL)] for y in range(NROW)]
players = [player() for x in range(numberOfPlayers)]
myPlayer = players[myPlayerId]

def readTable():
    for row in range(0, NROW):
        rowString = sys.stdin.readline()
        for col in range(0, NCOL):
            table[row][col] = int(rowString[col])
    for playerId in range(numberOfPlayers):
        coord = sys.stdin.readline().split(' ')
        players[playerId].updatePos(int(coord[0]), int(coord[1]))

moves = ['LEFT\n', 'UP\n', 'RIGHT\n', 'DOWN\n']
movesIndex = 0
while True:
    readTable()
    sys.stdout.write(moves[movesIndex])
    movesIndex = (movesIndex + 1) % 4



