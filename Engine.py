import Vectors as v
import NN as neur
import math
import pygame
import random
import numpy as np
import asyncio;

conf_file = open("engine_conf.conf", "r")
conf = conf_file.readlines()
conf_file.close()
del conf_file

dea_scg=5
dea_vwg=15
dea_spg=2
dea_atg=1
dea_esg=100
memDatScale = 5
genRandcoof = 0

for line in conf:
    data = line.split(":")
    if len(data) < 2:
        continue
    otherdat = data[1].split("\n")
    if len(otherdat) > 1:
        otherdat.pop(len(data[1].split("\n"))-1)

    if data[0] == "deafult_cell_memorNums":
        memDatScale = int(otherdat[0])
    elif data[0] == "deafult_cell_scg":
        dea_scg = float(otherdat[0])
    elif data[0] == "deafult_cell_vwg":
        dea_vwg = float(otherdat[0])
    elif data[0] == "deafult_cell_spg":
        dea_spg = float(otherdat[0])
    elif data[0] == "deafult_cell_atg":
        dea_atg = float(otherdat[0])
    elif data[0] == "deafult_cell_esg":
        dea_esg = float(otherdat[0])
    elif data[0] == "gen_rand_coof":
        genRandcoof = float(otherdat[0])

del data
del otherdat

def linear_num(a, b, pos):
    """Get a number, posited a>x>b, or a<x<b"""
    return a*(1-pos)+b*(pos)

def linear_col(col_a, col_b, pos, rounded: bool = True):
    """Return a smooth color, positioned middle 2 colors"""
    r = linear_num(col_a[0], col_b[0], pos)
    g = linear_num(col_a[1], col_b[1], pos)
    b = linear_num(col_a[2], col_b[2], pos)
    if rounded:
        return (round(r), round(g), round(b))
    return(r, g, b)

class Food:
    def __init__(self, col: tuple = (214, 152, 43), pos: v.Vector2D = v.Vector2D(0, 0), energyCount: float = 20):
        self.rad = math.sqrt((energyCount/40)/math.pi)/3
        self.pos = pos
        self.enAdd = energyCount
        self.col = col
        self.vec = v.Vector2D(0, 0)

    def Update(self, deltaTime):
        self.enAdd -= 0.25*deltaTime
        if self.enAdd <=0:
            return int(-1)
        self.rad = math.sqrt((self.enAdd/40)/math.pi)/3
        return int(0)

    def toJSON(self):
        data = {"type":"food", "col":self.col, "rad":self.rad, "energy":self.enAdd, "vec":self.vec.toJSON(), "pos":self.pos.toJSON()}
        return data

    def fromJSON(self, data):
        self.rad = data["rad"]
        self.pos = v.Vector2D(0,0)
        self.pos.fromJSON(data["pos"])
        self.enAdd = data["energy"]
        self.col = data["col"]
        self.vec = v.Vector2D(0,0)
        self.vec.fromJSON(data["vec"])



class Cell:
    def __init__(self, neural: neur.NeuralNetwork = neur.NeuralNetwork(14+memDatScale, 5, 3, 5, 2+memDatScale, lambda x: neur.sigmoid(x), lambda x: neur.sigmoid(x), lambda x: neur.sigmoid(x), lambda x: neur.advancedRELU(x)), pos: v.Vector2D = v.Vector2D(0, 0), vec: v.Vector2D = v.Vector2D(0, 0), energy: float = 100, col: tuple = (0, 255, 255), rad: float = 1):
        self.n = neural
        self.pos = pos
        self.vec = vec
        self.energy = energy
        self.col = col
        self.rad = rad
        self.viewGen = dea_vwg + (2*random.random()-1)*genRandcoof
        self.sizeGen = dea_scg + (2*random.random()-1)*genRandcoof
        self.speedGen = dea_spg + (2*random.random()-1)*genRandcoof
        self.attGen = dea_atg + (2*random.random()-1)*genRandcoof
        self.energySplitGen = dea_esg + (2*random.random()-1)*genRandcoof
        self.collideOUT = 0
        self.move_neuro = v.Vector2D(0, 0)
        self.memoryData = []
        for i in range(memDatScale):
            self.memoryData.append(0)

    async def Update(self, deltaTime, minF: Food, minC, time: float, space):
        await asyncio.sleep(0)
        if self.collideOUT >= 2:
            return int(-1)

        self.vec *= linear_num(1, 0.6, deltaTime)

        if minF == None:
            centredF = v.Vector2D(0, 0)
        else:
            centredF = minF.pos-self.pos

        if minC == None:
            centredC = v.Vector2D(0, 0)
            cell_vec = (0, 0)
        else:
            centredC = minC.pos-self.pos
            cell_vec = minC.vec.vec
        
        #print(centred.len(), centred)
        if minF != None:
            if centredF.len()-(self.rad+minF.rad) <= 0:
                self.energy += minF.enAdd
                space.delObject(minF)
        
        fnorm = centredF.Normalise()
        cnorm = centredC.Normalise()
        
        
        cCol = (0, 0, 0)
        if minC != None:
            cCol = minC.col

        inp_data = [1, self.energy/100, fnorm.vec[0],
                                     fnorm.vec[1], centredF.len()/self.viewGen, centredC.len()/self.viewGen,
                                     cnorm.vec[0], cnorm.vec[1], abs(cCol[0]-self.col[0])/255, abs(cCol[1]-self.col[1])/255,
                                     abs(cCol[2]-self.col[2])/255, cell_vec[0]/2, cell_vec[1]/2, math.cos(time)]
        for dat in self.memoryData:
            inp_data.append(dat)

        out = self.n.predict(np.array(inp_data))

        for ind in range(2, 1+len(self.memoryData)):
            self.memoryData[ind-2] = linear_num(self.memoryData[ind-2], out[ind], deltaTime)
        self.energy -= 0.1*deltaTime+((self.sizeGen)*0.05)*deltaTime+(self.speedGen*0.01)*deltaTime+v.Vector2D(out[0], out[1]).len()*deltaTime/2
        
        if centredC.len()-self.rad == 0 and out[2] >= 0.8:
            minC.energy -= self.attGen*deltaTime
            self.energy += self.attGen*deltaTime

        if self.energy <= 0.5:
            return int(-1)
            
        self.rad = math.sqrt((self.energy/40)/math.pi*self.sizeGen)/2

        if self.energy >= self.energySplitGen:
            self.energy /= 2
            c = Cell()
            c.fromJSON(self.toJSON())
            for i in range(len(self.memoryData)):
                c.memoryData[i] = 0
            c.Mutate(0.2)
            space.AddObject(c)

        self.vec += v.Vector2D(out[0]*self.speedGen, out[1]*self.speedGen)*deltaTime
        self.move_neuro = v.Vector2D(out[0]*self.speedGen, out[1]*self.speedGen)

        return int(1)

    def toJSON(self):
        data = {"type":"cell", "neuralN":self.n.Save(None, True), "pos":self.pos.toJSON(), "vec":self.vec.toJSON(), "col":self.col,
               "energy":self.energy, "rad":self.rad, "colOUT":self.collideOUT, "spGen":self.speedGen, "szGen":self.sizeGen,
               "esGen":self.energySplitGen, "vwGen":self.viewGen, "akGen":self.attGen, "memDat":self.memoryData}   
        return data

    def Mutate(self, coof):
        szRand = 0
        esRand = 0
        vwRand = 0
        spRand = 0
        akRand = 0

        if random.random()*100 >= 75:
            szRand = (random.random()*2-1)*coof
        if random.random()*100 >= 75:
            akRand = (random.random()*2-1)*coof
        if random.random()*100 >= 75:
            esRand = (random.random()*2-1)*coof
        if random.random()*100 >= 75:
            vwRand = (random.random()*2-1)*coof*2.5
        if random.random()*100 >= 75:
            spRand = (random.random()*2-1)*coof
        if random.random()*100 <= 70:
            self.n.Mutate(coof)
        self.sizeGen = max(0.2, self.sizeGen+szRand)
        self.energySplitGen = max(25, self.energySplitGen+esRand)
        self.speedGen = max(0.2, self.speedGen+spRand)
        self.viewGen = max(0.2, self.viewGen+vwRand)
        self.attGen = max(0, self.attGen+akRand)
        self.col = (min(max(0, self.col[0] + random.randint(-10, 10)), 255),
                    min(max(0, self.col[1] + random.randint(-10, 10)), 255),
                    min(max(0, self.col[2] + random.randint(-10, 10)), 255))
        

    def fromJSON(self, data):
        self.n = neur.NeuralNetwork(2, 2, 2, 2, 2, neur.nothing, neur.nothing, neur.nothing, neur.nothing)
        self.n.Load(data["neuralN"])
        self.pos = v.Vector2D(0, 0)
        self.pos.fromJSON(data["pos"])
        self.vec = v.Vector2D(0, 0)
        self.vec.fromJSON(data["vec"])
        self.energy = data["energy"]
        self.col = data["col"]
        self.rad = data["rad"]
        self.speedGen = max(0.2, data["spGen"])
        self.sizeGen = max(0.2, data["szGen"])
        self.viewGen = max(0.2, data["vwGen"])
        self.energySplitGen = max(25, data["esGen"])
        self.attGen = max(0, data["akGen"])
        self.collideOUT = data["colOUT"]
        self.memoryData = data["memDat"]

class Space:
    def __init__(self, size):
        self.size = size
        self.objects = []
        self.coroutineTasks = []

    def AddObject(self, obj):
        self.objects.append(obj)

    def delObject(self, objec):
        try:
            if type(objec) == int:
                self.objects.pop(objec)
            else:
                self.objects.pop(self.objects.index(objec))

        except BaseException:
            objec.pos = v.Vector2D(9e200, 9e200)

    async def updateCell(self, obj, time, deltaTime):
        await asyncio.sleep(0)
        lf = obj.viewGen
        food = None
        cell = None
        lc = obj.viewGen
        cell = min(self.objects, key= lambda objecs: (objecs.pos-obj.pos).len()+999999999999*(type(objecs) == Food), default=Cell)
        food = min(self.objects, key= lambda objecs: (objecs.pos-obj.pos).len()+999999999999*(type(objecs) == Cell), default=Food)
        if cell.pos-obj.pos > obj.viewGen or type(food) != Cell:
            cell = None
        if food.pos-obj.pos > obj.viewGen or type(food) != Food:
            food = None
        
        return await obj.Update(deltaTime, food, cell, time, self)

    async def updateobjs(self, deltaTime, time):
        iterat = 0
        for obj in self.objects:
            await asyncio.sleep(0)
            res: int = 0
            if type(obj) == Food:
                #continue
                res = obj.Update(deltaTime)
            elif type(obj) == Cell:
                task = asyncio.create_task(self.updateCell(obj, time, deltaTime))
                res = await task

            if res == -1:
                self.delObject(obj)
            iterat += 1

        for obj in self.objects:
            obj.pos += obj.vec*deltaTime
            if  not (-self.size[0]/2 <= obj.pos.vec[0] <= self.size[0]/2):
                #self.delObject(obj)
                obj.vec *= v.Vector2D(-1, 1)
                obj.pos += obj.vec*deltaTime
                if type(obj) == Cell:
                    obj.collideOUT += 1
                
            if not( -self.size[1]/2 <= obj.pos.vec[1] <= self.size[1]/2):
                #self.delObject(obj)

                obj.vec *= v.Vector2D(1, -1)
                obj.pos += obj.vec*deltaTime
                if type(obj) == Cell:
                    obj.collideOUT += 1
            iterat += 1

        return iterat

    def clear_error_data(self):
        for obj in self.objects:
            if obj == None:
                self.delObject(obj)

    def render(self, scr, scrSize, camPos, Scale):
         scrmin = min(scrSize[0], scrSize[1])
         realscale = (Scale*20)
         posscale = realscale*(scrmin/20)
         spmax = max(self.size[0],self.size[1])
         need_draw_line = bool(Scale > 60)

         for obj in self.objects:
             scrpos = v.Vector2D((obj.pos.vec[0]-camPos.vec[0])*(Scale)+scrSize[0]/2, (obj.pos.vec[1]-camPos.vec[1])*(Scale)+scrSize[1]/2)
             if v.Vector2D(0, 0) <= scrpos <= v.Vector2D(scrSize[0], scrSize[1]):
                 pygame.draw.circle(scr, (20, 20, 20), (round(scrpos.vec[0]),round( scrpos.vec[1])), (obj.rad*1)*Scale)
                 pygame.draw.circle(scr, (round(obj.col[0]), round(obj.col[1]), round(obj.col[2])), (round(scrpos.vec[0]),round( scrpos.vec[1])), (obj.rad*0.85)*Scale)
                 if type(obj) == Cell:
                     pygame.draw.circle(scr, linear_col((0, 0, 0), obj.col, 0.75), (round(scrpos.vec[0]),round( scrpos.vec[1])), math.sqrt((0.5/40)/math.pi*obj.sizeGen)/2*Scale)
                     pygame.draw.circle(scr, (round(obj.col[0]), round(obj.col[1]), round(obj.col[2])), (round(scrpos.vec[0]),round( scrpos.vec[1])), obj.viewGen*(Scale), 3)
                     if need_draw_line:
                         movepos = v.Vector2D((obj.pos.vec[0]-camPos.vec[0]+obj.move_neuro.vec[0]*obj.rad)*(Scale)+scrSize[0]/2, (obj.pos.vec[1]-camPos.vec[1]+obj.move_neuro.vec[1]*obj.rad)*(Scale)+scrSize[1]/2)
                         pygame.draw.line(scr, (30, 30, 30), (round(scrpos.vec[0]),round( scrpos.vec[1])), (round(movepos.vec[0]),round( movepos.vec[1])), round(0.025*Scale))
                         pygame.draw.circle(scr, (30, 30, 30), (round(movepos.vec[0]),round( movepos.vec[1])), round(0.025*Scale/math.pi*2))
                         pygame.draw.circle(scr, (30, 30, 30), (round(scrpos.vec[0]),round(scrpos.vec[1])), round(0.025*Scale/math.pi*2))

    def toJSON(self, time):
        lis = []
        for obj in self.objects:
            lis.append(obj.toJSON())
            print(obj.toJSON())

        data = {"size":self.size, "objs":lis, "time":time}
        return data

    def fromJSON(self, data):
        self.size = data["size"]
        objsl = []
        for jsonobj in data["objs"]:
            print(jsonobj)
            if jsonobj["type"] == "cell":
                cell = Cell()
                cell.fromJSON(jsonobj)
                objsl.append(cell)
                print(cell.fromJSON(jsonobj))
            elif jsonobj["type"] == "food":
                food = Food()
                food.fromJSON(jsonobj)
                objsl.append(food)
                print(food)

        self.objects = objsl
        return data["time"]