import pygame

class Button:
    def __init__(self,x,y,width,height,text=None,color=(73,73,73),
                 highlightedcolor=(189,189,189),function=None,params=None):
        self.image = pygame.Surface((width,height))
        self.pos = (x,y)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.text = text
        self.color = color
        self.highlightedcolor = highlightedcolor
        self.highlighted = False
        self.function = function
        self.params = params
        self.width = width
        self.height = height
      
    def update(self,mousepos):
        if self.rect.collidepoint(mousepos):
            self.highlighted = True
        else:
            self.highlighted = False
            
    def draw(self,window):
        if self.highlighted:
            self.image.fill(self.highlightedcolor)
        else:
            self.image.fill(self.color)
        if self.text:
            self.makeText(self.text)
        window.blit(self.image,self.pos)

    def click(self):
        if self.params:
            self.function(self.params)
        else:
            self.function()

    def makeText(self,text):
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(text,False,(0,0,0))
        width = text.get_width()
        height = text.get_height()
        x = (self.width-width)//2
        y = (self.height-height)//2
        self.image.blit(text,(x,y))
    









