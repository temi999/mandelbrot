import sys
import time

stdout = sys.stdout

BAILOUT = 16
MAX_ITERATIONS = 100


def averageTime(points):
    borderCount = 0
    borderTime = 0
    innerCount = 0
    innerTime = 0
    outerCount = 0
    outerTime = 0

    for i in range(1, 80, 1):
        for j in range(1, 80, 1):
            if points[i][j]['isInRange']:
                innerCount += 1
                innerTime += points[i][j]['timeToCalculate']
            elif points[i][j]['isBorder']:
                borderCount += 1
                borderTime += points[i][j]['timeToCalculate']
            else:
                outerCount += 1
                outerTime += points[i][j]['timeToCalculate']

    return innerTime / innerCount, borderTime / borderCount, outerTime / outerCount


def sumTime(points):
    borderTime = 0
    innerTime = 0
    outerTime = 0

    for i in range(1, 80, 1):
        for j in range(1, 80, 1):
            if points[i][j]['isInRange']:
                innerTime += points[i][j]['timeToCalculate']
            elif points[i][j]['isBorder']:
                borderTime += points[i][j]['timeToCalculate']
            else:
                outerTime += points[i][j]['timeToCalculate']

    return innerTime, borderTime, outerTime


class Iterator:
    points = [[0] * 81 for i in range(81)]

    def __init__(self):
        pass

    def render(self):
        self.clearList()

        for y in range(-39, 39):
            # stdout.write('\n') # закомментировано в целях чистоты вывода
            for x in range(-39, 39):
                timeToCalculate = time.clock()
                i = self.mandelbrot(x / 40.0, y / 40.0)
                timeToCalculate = time.clock() - timeToCalculate
                self.points[y + 40][x + 40]['timeToCalculate'] = timeToCalculate

                if i == 0:
                    # stdout.write('*') # закомментировано в целях чистоты вывода
                    self.points[y + 40][x + 40]['isInRange'] = True
                else:
                    pass
                    # stdout.write(str(i) + ' ') # закомментировано в целях чистоты вывода

    def clearList(self):
        for i in range(81):
            for j in range(81):
                self.points[i][j] = {'isInRange': False, 'isBorder': False, 'timeToCalculate': 0.0}

    def checkBorders(self):
        for i in range(1, 80, 1):
            for j in range(1, 80, 1):
                if self.points[i][j]['isInRange']:
                    continue
                elif (self.points[i + 1][j]['isInRange']
                      or self.points[i][j + 1]['isInRange']
                      or self.points[i - 1][j]['isInRange']
                      or self.points[i][j - 1]['isInRange']):
                    self.points[i][j]['isBorder'] = True

    def mandelbrot(self, x, y):
        cr = y - 0.5
        ci = x
        zi = 0.0
        zr = 0.0
        i = 0

        while True:
            i += 1
            temp = zr * zi
            zr2 = zr * zr
            zi2 = zi * zi
            zr = zr2 - zi2 + cr
            zi = temp + temp + ci

            if zi2 + zr2 > BAILOUT:
                return i
            if i > MAX_ITERATIONS:
                return 0


if __name__ == '__main__':
    test = Iterator()
    testCounter = 0
    currentInnerSum = 0
    currentInnerAverageSum = 0
    currentBorderSum = 0
    currentBorderAverageSum = 0
    currentOuterSum = 0
    currentOuterAverageSum = 0
    while True:
        if testCounter % 20 == 0 and testCounter != 0:
            print('---------------------------------')
            print('Test #{0} with MAX_ITERATIONS={1} passed. Results:'.format(int(testCounter / 20), MAX_ITERATIONS))
            print('Inner average:', currentInnerAverageSum / 20)
            print('Border average:', currentBorderAverageSum / 20)
            print('Outer average:', currentOuterAverageSum / 20)
            print('Inner average sum:', currentInnerSum / 20)
            print('Border average sum:', currentBorderSum / 20)
            print('Outer average: sum', currentOuterSum / 20)
            print('---------------------------------')
            currentInnerAverageSum = 0
            currentBorderAverageSum = 0
            currentOuterAverageSum = 0
            MAX_ITERATIONS *= 10
        if testCounter == 100:
            break
        test.render()
        test.checkBorders()

        innerAverage, borderAverage, outerAverage = averageTime(test.points)
        currentInnerAverageSum += innerAverage
        currentBorderAverageSum += borderAverage
        currentOuterAverageSum += outerAverage

        innerSum, borderSum, outerSum = sumTime(test.points)
        currentInnerSum += innerSum
        currentBorderSum += borderSum
        currentOuterSum += outerSum
        testCounter += 1
