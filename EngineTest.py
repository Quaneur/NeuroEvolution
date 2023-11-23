from Vectors import *
from Engine import *
from NN import *
import pygame
import random
import UI
import json
import time as ttt
import asyncio

conf_file = open("engine_conf.conf", "r")
conf = conf_file.readlines()
conf_file.close()
del conf_file
global memDatScale
global startDelta
global win_name
win_name = "Neuro Evolution v0.1"
memDatScale = 5
startDelta = 30

for line in conf:
    data = line.split(":")
    if len(data) < 2:
        continue
    else:
        otherdat = data[1].split("\n")
        if len(otherdat) > 1:
            otherdat.pop(len(data[1].split("\n"))-1)

        if data[0] == "deafult_cell_memorNums":
            memDatScale = int(otherdat[0])
        elif data[0] == "start_delta":
            startDelta = int(otherdat[0])
        elif data[0] == "window_name":
            win_name = otherdat[0]

del data
del otherdat

print(memDatScale, startDelta)


class TimeLineSave:
    timeline = []
    def __init__(self):
        self.timeline = []

    def AddTimeLine(self, time, cellsCount, foodCount, cellsEn):
        self.timeline.append({"time":time, "cells":cellsCount, "food":foodCount, "allCellsEnergy":cellsEn})

    def JSON(self):
        return self.timeline

def main():
    print(memDatScale, startDelta)
    seed = round(ttt.time()*10000)
    size = (2**11, 2**11)
    winsize = (2**10, 2**10)
    resizecoof = (size[0]/winsize[0], size[1]/winsize[1])
    fps = 30
    tl = TimeLineSave()
    tlLastTime = 0
    tlAddDelay = 0.1
    
    userinp = int(input("Load the saved simulation?\n1 - yes\n0 - no\n>>"))
    if userinp == 1:
        userinp2 = input("Enter the name of file >>")
        with open(f"{userinp2}.SEOS", "r") as f:
            sp = Space((0,0))
            time = sp.fromJSON(json.load(f))
            lastTimeSpawn = time
            currentTime = time
            sp.clear_error_data()
    else:

        sp = Space((250, 250))
        for i in range(1000):
            sp.AddObject(Food((214, 152, 43), v.Vector2D(random.randint(round(-sp.size[0]/2*100), round(sp.size[0]/2*100))/100, random.randint(round(-sp.size[1]/2*100), round(sp.size[1]/2*100))/100), random.randint(10000, 50000)/1000))
        
        for i in range(20):
            sp.AddObject(Cell(NeuralNetwork(14+memDatScale, 10, 10, 10, 2+memDatScale, neur.sigmoid, neur.sigmoid, neur.sigmoid, neur.advancedRELU),energy = 40, pos = v.Vector2D(random.randint(round(-sp.size[0]/2*100), round(sp.size[0]/2*100))/100, random.randint(round(-sp.size[1]/2*100), round(sp.size[1]/2*100))/100), col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
            lastTimeSpawn = 0
            currentTime = 0

    slD = UI.Slider(15, 300, 500, 25, 25, 1, 1000, startDelta, 1000)
    pygame.init()
    scr = pygame.Surface(size)
    wind = pygame.display.set_mode(winsize, pygame.SCALED|pygame.FULLSCREEN)
    pygame.display.set_caption(win_name)
    time = pygame.time
    clock = time.Clock()
    #sp.AddObject(Food((214, 152, 43), v.Vector2D(0, 0), 50000))

    delta = 1/round(slD.val)
    spawnDelay = 0.02
    useDelta = True
    f = pygame.font.Font("fonts/PressStart2P-vaV7.ttf", 24)
    pos = Vector2D(0, 0)
    scale = 20

    #control
    down = False
    up = False
    left = False
    right = False
    pause = False

    spawnfood = True

    rewind = False

    run = True
    render = True
    fpsmiddle = []
    for i in range(30):
        fpsmiddle.append(0)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

                elif event.key==pygame.K_SPACE:
                    pause = not pause;

                elif event.key == pygame.K_DOWN:
                    down = True
                elif event.key == pygame.K_UP:
                    up = True
                elif event.key == pygame.K_LEFT:
                    left = True
                elif event.key == pygame.K_RIGHT:
                    right = True

                elif event.key == pygame.K_BACKSPACE:
                    for obj in sp.objects:
                        if type(obj) == Food:
                            sp.delObject(obj)
                elif event.key == pygame.K_r:
                    render = not render
                elif event.key == 13:
                    rewind = True

                elif event.key == pygame.K_d:
                    useDelta = not useDelta
                elif event.key == pygame.K_i:
                    spawnfood = not spawnfood
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not render:
                    if slD.checkclick((event.pos[0]*resizecoof[0], event.pos[1]*resizecoof[1])):# and event.button == 0:
                        slD.uses = True
            elif event.type == pygame.MOUSEBUTTONUP:
                slD.uses = False
            elif event.type == pygame.MOUSEWHEEL:
                scale += (scale*event.y)/60
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    down = False
                elif event.key == pygame.K_UP:
                    up = False
                elif event.key == pygame.K_LEFT:
                    left = False
                elif event.key == pygame.K_RIGHT:
                    right = False

        if rewind:
            f = open(f"neuro-id{seed%2**20}.json", "w")
            json.dump(tl.JSON(), f)
            f.close()
            rewind = False

            random.seed(round(ttt.time()))
            seed = round(ttt.time()*10000)

            size = (2048, 2048)
                    
            tl = TimeLineSave()
            tlLastTime = 0
            tlAddDelay = 0.1

            sp = Space((250, 250))
            for i in range(1000):
                sp.AddObject(Food((214, 152, 43), v.Vector2D(random.randint(round(-sp.size[0]/2*100), round(sp.size[0]/2*100))/100, random.randint(round(-sp.size[1]/2*100), round(sp.size[1]/2*100))/100)))
            #sp.AddObject(Food((214, 152, 43), v.Vector2D(0, 0), 50000))
            for i in range(20):
                sp.AddObject(Cell(NeuralNetwork(14+memDatScale, 3, 4, 3, 2+memDatScale, neur.advancedRELU, neur.advancedRELU, neur.advancedRELU, neur.advancedRELU),energy = 40, pos = v.Vector2D(random.randint(round(-sp.size[0]/2*100), round(sp.size[0]/2*100))/100, random.randint(round(-sp.size[1]/2*100), round(sp.size[1]/2*100))/100), col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

            lastTimeSpawn = 0

            delta = 1/round(slD.val)
            currentTime = 0
            lastTimeSpawn = currentTime
            spawnDelay = 0.25
            f = pygame.font.Font("fonts/PressStart2P-vaV7.ttf", 24)

        if slD.uses:
            slD.MoveMouse((pygame.mouse.get_pos()[0]*resizecoof[0], pygame.mouse.get_pos()[1]*resizecoof[1]))
            delta = 1/round(slD.val)

        if not pause:
            lastTime = currentTime
            if useDelta:
                currentTime += delta
            else:
                currentTime = time.get_ticks()/1000

        popul = 0
        foodc = 0
        enC = 0
        cenC = 0
        for obj in sp.objects:
            if type(obj) == Cell:
                popul += 1
                cenC += obj.energy
            else:
                foodc += 1
                enC += obj.enAdd
        if popul == 0:
            rewind = True

        elif foodc >1000:
            lastTimeSpawn = currentTime-spawnDelay

        for i in range(len(fpsmiddle)-1):
            fpsmiddle[i] = fpsmiddle[i+1]
        try:
            fpsmiddle[len(fpsmiddle)-1] = clock.get_fps()
        except ZeroDivisionError:
            fpsmiddle[len(fpsmiddle)-1] = 9999

        if not pause:
            ite = asyncio.run(sp.updateobjs(currentTime-lastTime, currentTime))
            if currentTime-tlLastTime >= tlAddDelay:
                tl.AddTimeLine(currentTime, popul, foodc, cenC)
                tlLastTime = currentTime
            if currentTime-lastTimeSpawn >= spawnDelay and spawnfood and foodc <= 1000:
                while currentTime - lastTimeSpawn > spawnDelay:
                    sp.AddObject(Food((214, 152, 43), v.Vector2D(random.randint(round(-sp.size[0]/2*100), round(sp.size[0]/2*100))/100, random.randint(round(-sp.size[1]/2*100), round(sp.size[1]/2*100))/100), 50))
                    lastTimeSpawn += spawnDelay
            elif foodc >1000:
                lastTimeSpawn = currentTime-spawnDelay


        if down:
            pos += (0, 240*2/scale/clock.get_fps())
        if up:
            pos += (0, -240*2/scale/clock.get_fps())
        if left:
            pos += (-240*2/scale/clock.get_fps(), 0)
        if right:
            pos += (240*2/scale/clock.get_fps(), 0)
        if not pause:
            tl.AddTimeLine(currentTime, popul, foodc, cenC)
            tlLastTime = currentTime

        if render:
            scr.fill((128, 128, 128))
            sp.render(scr, size, pos, scale)
        else:
            scr.fill((0, 0, 0))
            text1 = f.render(f"Time: {round(currentTime*1000)/1000}, Population: {popul}", True, (255, 255, 255))
            text6 = f.render(f"food Objects Count: {foodc}. Summary food energy Count: {round(enC)}", True, (255, 255, 255))
            text3 = f.render(f"Summnary Cells energy Count: {cenC}", True, (255, 255, 255))
            text2 = f.render(f"Iterations Count: {ite}, SliderVal:{slD.val}", True, (255, 255, 255))
            text5 = f.render(f"lasttlTime: {tlLastTime}", True, (255, 255, 255))
            scr.blit(text1, (0, 50))
            scr.blit(text6, (0, 100))
            scr.blit(text3, (0, 150))
            scr.blit(text2, (0, 200))
            scr.blit(text5, (0, 350))
            slD.render(scr)
            if useDelta:
                text4 = f.render(f"USING DELTA", False, (255, 50, 50))
                scr.blit(text4, (0, 250))

        fr = 0
        for fp in fpsmiddle:
            fr += fp
        fr /= len(fpsmiddle)

        text = f.render(f"FPS: {round(fr*10)/10}", True, (255, 255, 255))
        scale_render = f.render(f"Scale:{round(scale*100)/100}", True, (255, 255, 255))
        scr.blit(text, (0, 0))
        scr.blit(scale_render, (size[0]-400, 50))
        wind.blit(pygame.transform.smoothscale(scr, winsize), (0,0))
        pygame.display.update()
        clock.tick()

    f = open(f"neuro-id{seed%2**20}.json", "w")
    json.dump(tl.JSON(), f)
    f.close()
    pygame.quit()

    userinp = int(input("Save the simulation?\n1:yes\n0:no\n>>"))

    if userinp == 1:
        userinp2 = input("Enter the name of file >>")
        with open(f"{userinp2}.SEOS", "w") as f:
            data = sp.toJSON(currentTime)
            json.dump(data, f)


def UITest():
    pygame.init()

    Size = (512, 512)

    scr = pygame.display.set_mode(Size)
    clock = pygame.time.Clock()

    objects = [UI.Window(v.Vector2D(128, 128), name="TestWindow Hehehe")]
    objects[0].Addobj(UI.Circle(v.Vector2D(128, 128), 64, (255, 255, 255)))
    #window.Addobj(window)

    run = True
    i = 0
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        scr.fill((0, 0, 0))
        for obj in objects:
            if type(obj) == UI.Window:
                res = obj.events(events)
                if res == -1:
                    objects.remove(obj)
                    continue
                scr.blit(obj.render(), (round(obj.pos.vec[0]), round(obj.pos.vec[1])))

        pygame.display.flip()
        i += 1/15
        pygame.time.Clock().tick(60)


if __name__=="__main__":
    main()