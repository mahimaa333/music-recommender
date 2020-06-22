import pygame, sys
from pygame.locals import *
from buttons import *
from board import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
BOXSIZE = 50
BOARDSIZE = 9
TOTALBOARDSIZE = BOARDSIZE*BOXSIZE

BLACK = (0,0,0)
WHITE = (255 , 255, 255)
BLUE = (135,206,235)
RED = (250,128,114)
GRAY = (169,169,169)

gridPosition = (20,60)

board = Board()

class Sudoku:    
    def __init__(self):
        pygame.init()
        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT));
        self.mouseClicked = None
        self.mousePos = None
        self.finished = False
        self.cellChanged = False
        self.playingButton = []
        self.incorrectCells = []
        self.unlockedCells = []
        self.getBoard("easy")

    def getBoard(self,difficulty):
        self.makeboard = board.makeBoard()
        self.board1 = board.makePuzzleBoard(self.makeboard,difficulty)
        self.grid = self.board1
        self.load()

    def solve(self):
        if board.solveBoard(self.makeboard):
            self.grid1 = self.makeboard

    def resetBoard(self): 
        for m, row in enumerate(self.board1):
            for n, num in enumerate(row):
                if([n,m] in self.unlockedCells):
                    self.board1[m][n] = 0
            
    def main(self):    
        while True:  
            self.DISPLAYSURF.fill(WHITE)
            self.checkForKeyPress()
            self.update()
            self.draw()
     
    def terminate(self):
        pygame.quit()
        sys.exit()
            
    def checkForKeyPress(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                 self.terminate() 
            elif event.type == MOUSEBUTTONDOWN:
                mouseClicked = self.clickedOnBoard()
                if mouseClicked:        
                    self.mouseClicked = mouseClicked
                else:
                    self.mouseClicked = None
                    for buttons in self.playingButton:
                        if buttons.highlighted:
                            buttons.click()

            if event.type == KEYDOWN:
                if self.mouseClicked != None and self.mouseClicked not in self.lockedCells:
                    if self.isInt(event.unicode):
                        self.grid[self.mouseClicked[1]][self.mouseClicked[0]] = int(event.unicode)
                        self.cellChanged = True    
                        
    def update(self):
        self.mousePos = pygame.mouse.get_pos()
        for button in self.playingButton:
            button.update(self.mousePos)
            
        if self.cellChanged:
            self.incorrectCells = []

            for row in self.grid:
                y = 1
                for n in row:
                    if n == 0:
                        y = 0

            if y == 1:
                self.checkAllCells()
                if self.incorrectCells == []:
                    print('You Won!!')
                    font = pygame.font.Font('freesansbold.ttf', 20)
                    pygame.draw.rect(self.DISPLAYSURF, WHITE, (300, 30,400 ,50 ))
                    textSurf = font.render('HURRAY!! YOU SOLVED IT', True, BLACK)
                    textRect = textSurf.get_rect()
                    self.DISPLAYSURF.blit(textSurf, textRect)
                
    
    def draw(self):      
        if self.mouseClicked:
            self.drawSelection(self.DISPLAYSURF,self.mouseClicked)
                    
        for button in self.playingButton:
            button.draw(self.DISPLAYSURF)
          
        self.drawDarkColor(self.DISPLAYSURF,self.lockedCells,self.unlockedCells)
        
        self.shadeWrongCells(self.DISPLAYSURF,self.incorrectCells)
        self.drawNumbers()
        self.drawBoard()
        pygame.display.update()
        self.cellChanged = False
    
    def drawBoard(self):
        pygame.draw.rect(self.DISPLAYSURF, BLACK, (gridPosition[0],gridPosition[1],
                     WINDOWWIDTH-150, WINDOWHEIGHT-150),2)
        for i in range(9):
            thickness = 1
            if(i%3 == 0):
                thickness = 2
            pygame.draw.line(self.DISPLAYSURF,BLACK,(gridPosition[0] +(i*BOXSIZE),gridPosition[1]),(gridPosition[0] +(i*BOXSIZE),gridPosition[1] + BOARDSIZE*BOXSIZE),thickness)
            pygame.draw.line(self.DISPLAYSURF,BLACK,(gridPosition[0],gridPosition[1] +(i*BOXSIZE)),(gridPosition[0] + BOARDSIZE*BOXSIZE,gridPosition[1] +(i*BOXSIZE)),thickness)
               
    def drawSelection(self,window,click):
        if click in self.unlockedCells:
            pygame.draw.rect(window,BLUE,((click[0]*BOXSIZE)+gridPosition[0],
                                     (click[1]*BOXSIZE)+gridPosition[1],BOXSIZE,BOXSIZE))
       
    def drawDarkColor(self,display,lockedCells,unlockedCells):
        for m,row in enumerate(self.grid):
            for i in range(9):
                if([i,m] in lockedCells):
                    pygame.draw.rect(display,GRAY,((i*BOXSIZE)+gridPosition[0],
                                                                    (m*BOXSIZE)+gridPosition[1],BOXSIZE,BOXSIZE))
                #elif([i,m] in unlockedCells):
                #   pygame.draw.rect(display,WHITE,((i*BOXSIZE)+gridPosition[0],
                #                                                  (m*BOXSIZE)+gridPosition[1],BOXSIZE,BOXSIZE))

    def shadeWrongCells(self,display,incorrectCells):       
        for n in incorrectCells:
            pygame.draw.rect(display,RED,((n[0]*BOXSIZE)+gridPosition[0],
                                                            (n[1]*BOXSIZE)+gridPosition[1],BOXSIZE,BOXSIZE))
    
    def drawNumbers(self):
        for m, row in enumerate(self.board1):
            for n, num in enumerate(row):
                if(num!=0):
                    pos = [(n*BOXSIZE)+gridPosition[0] ,(m*BOXSIZE)+gridPosition[1]]
                    self.textToScreen(str(num),pos)
       
    def clickedOnBoard(self):
        if (self.mousePos[0] < gridPosition[0] or self.mousePos[1] < gridPosition[1]):
            return False
        elif self.mousePos[0] > gridPosition[0]+TOTALBOARDSIZE or self.mousePos[1] > gridPosition[1]+TOTALBOARDSIZE:
            return False
        return ((self.mousePos[0]-gridPosition[0])//BOXSIZE, (self.mousePos[1]-gridPosition[1])//BOXSIZE)
    
    def load(self):
        self.loadbuttons()
        self.lockedCells = []
        self.incorrectCells = []
        self.unlockedCells = []
        self.finished = False
        for m, row in enumerate(self.grid):
            for n, num in enumerate(row):
                if(num!=0):
                    self.lockedCells.append([n,m])
                else:
                    self.unlockedCells.append([n,m])

    def loadbuttons(self):
        
        self.playingButton.append(Button(490,320,100,40,function=self.getBoard,
                                        color=(27,147,207),text = 'Easy',params="easy"))
        self.playingButton.append(Button(490,380,100,40,function=self.getBoard,
                                        color=(27,147,207),text = 'Moderate',params="moderate"))
        self.playingButton.append(Button(490,440,100,40,function=self.getBoard,
                                        color=(27,147,207),text = 'Hard',params="difficult"))
        self.playingButton.append(Button(20,540,100,40,function=self.resetBoard,
                                        color=(27,147,207),text = 'Reset'))
        self.playingButton.append(Button(140,540,100,40,function=self.solve,
                                        color=(27,147,207),text = 'Solve'))
        self.playingButton.append(Button(260,540,100,40,function=self.checkAllCells,
                                        color=(27,147,207),text = 'Check'))

    def textToScreen(self,text,pos):
        basicFont = pygame.font.Font('freesansbold.ttf', 20)
        textSurf = basicFont.render(text,False,BLACK)
        textWidth = textSurf.get_width()
        textHeight = textSurf.get_height()
        pos[0] = pos[0] + (BOXSIZE-textWidth)//2
        pos[1] = pos[1] + (BOXSIZE-textHeight)//2
        self.DISPLAYSURF.blit(textSurf,pos)
        
        
    def checkAllCells(self):
        self.checkRows()
        self.checkColumns()
        self.checkGrid()
        
    def checkRows(self):
        for m,row in enumerate(self.grid):
            moves = [1,2,3,4,5,6,7,8,9]
            for i in range(9):
                if self.grid[m][i] in moves:
                    moves.remove(self.grid[m][i])
                elif([i,m] not in self.lockedCells) and ([i,m] not in self.incorrectCells):
                    self.incorrectCells.append([i,m])    
                elif([i,m] in self.lockedCells):
                       for j in range(9):
                           if self.grid[m][j] == self.grid[m][i] and [j,m] not in self.lockedCells:
                               self.incorrectCells.append([j,m])

    def checkColumns(self):
        for i in range(9):
            moves = [1,2,3,4,5,6,7,8,9]
            for m,row in enumerate(self.grid):
                if self.grid[m][i] in moves:
                    moves.remove(self.grid[m][i])
                elif([i,m] not in self.lockedCells) and ([i,m] not in self.incorrectCells):
                    self.incorrectCells.append([i,m])
                elif([i,m] in self.lockedCells):
                       for j,row in enumerate(self.grid):
                           if self.grid[j][i] == self.grid[m][i] and [i,j] not in self.lockedCells:
                               self.incorrectCells.append([i,j])

    def checkGrid(self):
        for i in range(3):
            for j in range(3):
                moves = [1,2,3,4,5,6,7,8,9] 
                for x in range(3):
                    for y in range(3):
                        m = i*3 + x
                        n = j*3 + y
                        if self.grid[n][m] in moves:
                            moves.remove(self.grid[n][m])
                        elif([m,n] not in self.lockedCells) and ([m,n] not in self.incorrectCells):
                            self.incorrectCells.append([m,n])
                        elif([m,n] in self.lockedCells):
                            for k in range(3):
                                for l in range(3):
                                    o = i*3 + k
                                    p = j*3 + l
                                    if self.grid[p][o] == self.grid[n][m] and [o,p] not in self.lockedCells:
                                        self.incorrectCells.append([o,p])

    def isInt(self,string):
        try:
            int(string)
            return True
        except:
            return False

if __name__ == '__main__':
    sudoku = Sudoku()
    sudoku.main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        

