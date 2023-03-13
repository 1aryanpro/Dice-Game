from random import randint
import re

SIZE = 4
DICE_SIZE = 6
COLOR_NUM = 3
DICE_NUM = 3
FGCODES = ['\x1b[39m', '\x1b[31m', '\x1b[32m', '\x1b[33m', '\x1b[34m']
BGCODES = ['\x1b[49m', '\x1b[41m', '\x1b[42m', '\x1b[43m', '\x1b[44m']

state = [[-1]*SIZE for i in range(SIZE)]
dice = []
score = 0


def diceInfo(n):
    n = n-1
    return n//DICE_SIZE + 1, n % DICE_SIZE + 1


def drawBoard():
    rowtext = '·---'*SIZE+'·'
    print(rowtext)
    for row in state:
        s = '| '
        for val in row:
            if val == -1:
                s += ' '  # ·
            else:
                c, n = diceInfo(val)
                s += FGCODES[c] + str(n) + FGCODES[0]
            s += ' | '
        print(s)
        print(rowtext)


def drawDice():
    s = []
    for d in dice:
        c, n = diceInfo(d)
        s.append(FGCODES[c] + str(n) + FGCODES[0])
    print('Dice:', ', '.join(s))


def randomize():
    if len(dice) != 0:
        return

    for i in range(DICE_NUM):
        dice.append(randint(1, DICE_SIZE*COLOR_NUM))


def clearLines():
    global score

    rowRemovals = []
    colRemovals = []
    for i in range(SIZE):
        rCheck = True
        for x in range(SIZE):
            if state[i][x] == -1:
                rCheck = False
                break

        cCheck = True
        for y in range(SIZE):
            if state[y][i] == -1:
                cCheck = False
                break

        if rCheck:
            rowRemovals.append(i)
        if cCheck:
            colRemovals.append(i)

    for r in rowRemovals:
        for x in range(SIZE):
            state[r][x] = -1
        score += 2

    for c in colRemovals:
        for y in range(SIZE):
            state[y][c] = -1
        score += 2


def addToBoard(x, y, die):
    global score

    if (state[y][x] != -1):
        raise Exception

    val = dice.pop(die)
    state[y][x] = val
    score += 1


def doTurn():
    global score

    randomize()
    print('Score:', score)
    drawBoard()
    drawDice()
    print()
    try:
        die = int(input('Which die? ')) - 1
        if die < 0 or die >= len(dice):
            raise Exception
        # TODO: Draw board showing allowed spots

        match = re.compile(r'(.),\s*(.)').match(input('coords: '))

        x = int(match.group(1)) - 1
        y = int(match.group(2)) - 1
        addToBoard(x, y, die)

    except Exception:
        print('something went wrong, try again')
        return

    clearLines()


if __name__ == '__main__':
    while True:
        doTurn()
    pass
