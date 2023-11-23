import pygame
import Vectors as v

class Slider:
    def __init__(self, x = 0, y = 0, width = 30, height = 5, circleSize = 1, minVal = 1, maxVal = 1, startVal = 0, steps = 0, lineCol = (255, 255, 255), circleCol = (round(255/4*3), round(255/4*3), round(255/4*3))):
        self.line = pygame.Rect(x ,y, width, height)
        self.normalcoof = 1/(maxVal-minVal)
        self.poscoof = width*self.normalcoof
        self.poscenter = v.Vector2D(x+width/2, y+height/2)
        if minVal <= startVal <= maxVal:
            self.circlePos = v.Vector2D(startVal*self.poscoof-self.line.width/2, 0)
        else:
            if minVal > startVal:
                raise ValueError(f"startVal don't in range --> {startVal} < {minVal}")
            else:
                raise ValueError(f"startVal don't in range --> {startVal} > {maxVal}")
        self.circleSize = circleSize
        self.minVal = minVal
        self.maxVal = maxVal
        self.val = startVal
        self.steps = steps
        self.lcol = lineCol
        self.ccol = circleCol
        self.uses = False

    def __str__(self):
        return f"Slider<line:{self.line}, poscenter:{self.poscenter}, circlePos: {self.circlePos}, range: {self.maxVal-self.minVal}, normalcoof: {self.normalcoof}>"

    def MoveMouse(self, mousepos):
        mv = v.Vector2D(mousepos[0], mousepos[1])
        norm = mv - self.poscenter
        preval = max(0, min(norm.vec[0] + self.line.width/2 ,self.line.width))
        if self.steps >= 2:
            stepVal = round(preval/self.poscoof*self.normalcoof*(self.steps-1))/(self.steps-1)/self.normalcoof+self.minVal
            self.val = stepVal
        else:
            self.val = preval/self.poscoof+self.minVal
        self.circlePos = v.Vector2D(self.val*self.poscoof-self.line.width/2, 0)

    def checkclick(self, clickPos):
        pos = v.Vector2D(clickPos[0], clickPos[1])
        normalise = pos-(self.circlePos+self.poscenter)
        if normalise.len() <= self.circleSize:
            return True
        return False

    def render(self, scr):
        circlepos = self.circlePos+self.poscenter
        pygame.draw.rect(scr, self.lcol, self.line)
        pygame.draw.circle(scr, self.ccol, circlepos.vec, self.circleSize)

class Circle:
    def __init__(self, pos: v.Vector2D, rad: float, col, width: float = 0):
        self.pos = pos
        self.rad = rad
        self.col = col
        self.width = width
        self.ret = None

    def render(self, surf):
        if self.width > 0:
            pygame.draw.circle(surf, self.col, (round(self.pos.vec[0]), round(self.pos.vec[1])), self.rad, self.width)
        else:
            pygame.draw.circle(surf, self.col, (round(self.pos.vec[0]), round(self.pos.vec[1])), self.rad)

class Window:
    def __init__(self, position:v.Vector2D, Size: tuple = (256, 256), baseCol: tuple = (20, 20, 20), RescaleCoof: float = 1, topcol: tuple = (128, 128+64, 128), name:str = "Window"):
        super().__init__()
        self.objects = []
        self.rescaleSize = RescaleCoof
        self.windowScr = pygame.Surface(Size)
        self.pos = position
        self.bgCol = baseCol
        self.topCol = topcol
        self.name = name
        self.events_buffer = []
        self.ret = "surf"

    def events(self, events: list|tuple):
        events_list = events
        for event in events_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.Rect(self.pos.vec[0]+self.windowScr.get_width()+2-18, self.pos.vec[1]+2, 16, 16), event.pos)
                if pygame.Rect(self.pos.vec[0]+self.windowScr.get_width()+2-18, self.pos.vec[1]+2, 16, 16).collidepoint(event.pos):
                    return -1
        return 0

    def Addobj(self, obj: Circle|Slider):
        self.objects.append(obj)

    def render(self):
        self.windowScr.fill(self.bgCol)
        for obj in self.objects:
            if obj.ret == "surf":
                surf = obj.render()
                self.windowScr.blit(surf, round(obj.pos.vec))
            else:
                obj.render(self.windowScr)

        topSurf = pygame.Surface((self.windowScr.get_width()+2, 20))
        topSurf.fill(self.topCol)
        font = pygame.font.SysFont("Arial", 16)
        if font.size(self.name)[0] > self.windowScr.get_size()[0]//1.5:
            txt = self.name[:10]+"..."
        else:
            txt = self.name
        nameRend = font.render(txt, 1, (10, 10, 10))
        topSurf.blit(nameRend, (2, 1))

        pygame.draw.rect(topSurf, (128+64+32, 50, 50), pygame.Rect(topSurf.get_size()[0]-18, 2, 16, 16))
        pygame.draw.aaline(topSurf, (10, 10, 10), (topSurf.get_size()[0]-16, 4), (topSurf.get_size()[0]-4, 16), 255)
        pygame.draw.aaline(topSurf, (10, 10, 10), (topSurf.get_size()[0]-16, 16), (topSurf.get_size()[0]-4, 4), 255)
        pygame.draw.aaline(topSurf, (10, 10, 10), (topSurf.get_size()[0]-15, 4), (topSurf.get_size()[0]-4, 15), 255)
        pygame.draw.aaline(topSurf, (10, 10, 10), (topSurf.get_size()[0]-15, 16), (topSurf.get_size()[0]-4, 5), 255)
        pygame.draw.aaline(topSurf, (10, 10, 10), (topSurf.get_size()[0]-16, 5), (topSurf.get_size()[0]-5, 16), 255)
        pygame.draw.aaline(topSurf, (10, 10, 10), (topSurf.get_size()[0]-16, 15), (topSurf.get_size()[0]-5, 4), 255)

        resBlit = pygame.Surface((self.windowScr.get_width()+2, self.windowScr.get_height()+21))
        resBlit.fill(self.topCol)
        resBlit.blits(((self.windowScr, (1, 20)), (topSurf, (0, 0))))
        resBlit = pygame.transform.scale(resBlit, (round(resBlit.get_size()[0]*self.rescaleSize), round(resBlit.get_size()[1]*self.rescaleSize)))
        return resBlit

