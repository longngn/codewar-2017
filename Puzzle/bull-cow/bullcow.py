# pylint: disable=all
import random
import subprocess
import pexpect
import re

def hasDupeDigits(_x):
    x = str(_x)
    for i in range(0, len(x) - 1):
        for j in range(i+1, len(x)):
            if x[i] == x[j]:
                return False
    return True

def isCompatible(_checkNumber, _guessedNumber, expectedNumberOfMatchingDigits, expectedNumberOfExistedDigits):
    checkNumber = str(_checkNumber)
    guessedNumber = str(_guessedNumber)
    actualNumberOfMatchingDigits, actualNumberOfExistedDigits = 0, 0
    remainedDigitsOfCheckNumber, remainedDigitsOfGuessedNumber = [], []
    for i in range(0, len(checkNumber)):
        if checkNumber[i] == guessedNumber[i]:
            actualNumberOfMatchingDigits += 1
        else:
            remainedDigitsOfCheckNumber.append(checkNumber[i])
            remainedDigitsOfGuessedNumber.append(guessedNumber[i])
    for x in remainedDigitsOfCheckNumber:
        for y in remainedDigitsOfGuessedNumber:
            if x == y:
                actualNumberOfExistedDigits += 1
    return actualNumberOfExistedDigits == expectedNumberOfExistedDigits and actualNumberOfMatchingDigits == expectedNumberOfMatchingDigits

def createNumberList(numberOfDigits):
    res = []
    for i in range(10 ** (numberOfDigits - 1), 10 ** numberOfDigits):
        res.append(i)
    res = list(filter(hasDupeDigits, res))
    return res

numberLists = {}
for i in range(4, 7):
    numberLists[i] = createNumberList(i)

candidates = []
first_time = True
def start(numberOfDigits):
    global candidates, first_time
    candidates = numberLists[numberOfDigits]
    first_time = True

pattern = re.compile('\nIt\'s a ([0-9])-digit number. Your answer: *')
nc = pexpect.spawn('nc bullandcow-challenge.framgia.vn 2015')

while True:
    nc.expect(pattern)
    print '---Before is: \n' + nc.before + '\n----end'
    print '---After is: \n' + nc.after + '\n----end'
    if 'secret number' in nc.before or 'another number' in nc.before:
        numberOfDigits = pattern.match(nc.after).group(1)
        start(int(numberOfDigits))
    else:
        numberOfMatchingDigits = nc.before.count('bull')
        numberOfExistedDigits = nc.before.count('cow')
        candidates = list(filter(lambda x: isCompatible(x, candidate, numberOfMatchingDigits, numberOfExistedDigits), candidates))
    candidate = candidates[0]
    print '---Candidate: %d, (total: %d)\n' % (candidate, len(candidates))
    nc.sendline(str(candidate))
    candidates.remove(candidate)
    first_time = False
