import numpy

def Convert(listw: list|numpy.ndarray, t: bool = False):
    if t:
        return numpy.array(listw)
    else:
        l = []
        for lis in list(listw):
            l.append(list(lis))
        return l
