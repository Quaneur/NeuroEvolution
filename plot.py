import matplotlib.pyplot as pl
import json as j
from tkinter import filedialog as fd
import numpy

f = fd.askopenfilename(filetypes=[["json File",".json"]], initialdir="", title="Open Simulation's Timeline")

tl = j.load(open(f))

x = []
cells = []
foods = []
enC = []

for obj in tl:
    print(obj)
    x.append(obj["time"])
    cells.append(obj["cells"])
    foods.append(obj["food"])
    enC.append(obj["allCellsEnergy"])

x = numpy.array(x)
cells = numpy.array(cells)
foods = numpy.array(foods)
enC = numpy.array(enC)

pl.plot(x, cells, x, foods, x, enC/cells)


pl.show()