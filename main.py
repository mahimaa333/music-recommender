import math
from random import randint

class Board:

    def __init__(self):
        self.size = 9

    def getColoumn(self,index, arr2d):
        coloumn = []
        for row in arr2d:
            coloumn.append(row[index])
        return coloumn

    def getInnerMatrix(self,x, y, arr):
        innerMatrix = []
        sizeOfInnerMatrix = int(math.sqrt(self.size))
        x1 = 0
        y1 = 0

        while((x1 + sizeOfInnerMatrix) <= x):
            x1+=sizeOfInnerMatrix

        while((y1 + sizeOfInnerMatrix) <= y):
            y1+=sizeOfInnerMatrix
            
        x2 = x1 + sizeOfInnerMatrix
        y2 = y1 + sizeOfInnerMatrix
        for i in range(x1, x2):
            for j in range(y1, y2):
                innerMatrix.append(arr[i][j])
        return innerMatrix    

    def find_empty_location(self,arr,l):
        for row in range(9):
            for col in range(9):
                if(arr[row][col]==0):
                    l[0]=row
                    l[1]=col
                    return True
        return False
        
    def solveBoard(self,arr2d):
        l=[0,0]
        if(not self.find_empty_location(arr2d, l)):
            return True
        row=l[0]
        col=l[1]
        for num in range(1,self.size+1):
            safeList = self.getAllPossibleNumbersInPlace(row, col, arr2d)
            if num in safeList:
                arr2d[row][col] = num
                if(self.solveBoard(arr2d)):
                    return True
                arr2d[row][col] = 0
        return False

    def shuffleBoard(self,arr2d):
        chooseNumber = -1
        replacingNumber = -1
        while(replacingNumber == chooseNumber):
            chooseNumber = randint(1, self.size)
            replacingNumber = randint(1, self.size)
        for i in range(0, self.size):
            for j in range(0, self.size):
                if(arr2d[i][j] == chooseNumber):
                    arr2d[i][j] = replacingNumber
                elif(arr2d[i][j] == replacingNumber):
                    arr2d[i][j] = chooseNumber

        sizeOfInnerMatrix = int(math.sqrt(self.size))
        if (sizeOfInnerMatrix > 1):
            chooseRowIndex = -1
            replacingRowIndex = -1
            while(chooseRowIndex == replacingRowIndex):
                chooseRowIndex = randint(1, sizeOfInnerMatrix)
                replacingRowIndex = randint(1, sizeOfInnerMatrix)
            multiplier = randint(0, sizeOfInnerMatrix-1)
            chooseRowIndex+=(multiplier*sizeOfInnerMatrix)
            replacingRowIndex+=(multiplier*sizeOfInnerMatrix)
            arr2d[chooseRowIndex - 1], arr2d[replacingRowIndex - 1] = arr2d[replacingRowIndex -1], arr2d[chooseRowIndex - 1]
            arr2d = [[x[i] for x in arr2d] for i in range(self.size)]
            chooseRowIndex-=(multiplier*sizeOfInnerMatrix)
            replacingRowIndex-=(multiplier*sizeOfInnerMatrix)
            multiplier = randint(0, sizeOfInnerMatrix-1)
            chooseRowIndex+=(multiplier*sizeOfInnerMatrix)
            replacingRowIndex+=(multiplier*sizeOfInnerMatrix)
            arr2d[chooseRowIndex - 1], arr2d[replacingRowIndex - 1] = arr2d[replacingRowIndex -1], arr2d[chooseRowIndex - 1]
            
        return arr2d

    def getAllPossibleNumbersInPlace(self,rowIndex, colIndex, arr2d):
        row = arr2d[rowIndex]
        col = self.getColoumn(colIndex, arr2d)
        innerMatrix = self.getInnerMatrix(rowIndex, colIndex, arr2d)
        posibilities = [x for x in range(1, self.size+1) if ((x not in row) and (x not in col) and (x not in innerMatrix))]
        
        return posibilities

    def removeLogically(self,arr2d, cutOff=35):
        removedItems = 0
        for _ in range(self.size*500):
            i = randint(0, self.size-1)
            j = randint(0, self.size-1)
            temp = arr2d[i][j]
            if(temp == 0):
                continue
            arr2d[i][j] = 0
            if(len(self.getAllPossibleNumbersInPlace(i, j, arr2d)) != 1):
                arr2d[i][j] = temp
            else:
                removedItems+=1
            if(removedItems == cutOff):
                return

    def makeBoard(self):
        board = [[0 for _ in range(self.size)] for _ in range(self.size)]

        for i in range(0, self.size):
            for j in range(0, self.size):
                board[i][j] = int((i * math.sqrt(self.size) + int(i / math.sqrt(self.size)) + j) % self.size) + 1

        randomInt = randint(8, 15)
        for _ in range(randomInt):
            board = self.shuffleBoard(board)

        return board


    def makePuzzleBoard(self,board, level="easy"):
        sizeSquare = self.size*self.size
        levels = {
            "easy" : ((int(sizeSquare/2) - int(sizeSquare/10)),0),
            "moderate" : (int(sizeSquare), int(sizeSquare/15)),
            "difficult" : (int(sizeSquare), int(sizeSquare/10))
            }
        logicalCutOff = levels[level][0]
        self.removeLogically(board, logicalCutOff)
        return board
        
