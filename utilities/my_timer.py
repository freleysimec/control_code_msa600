import time
t0 = time.time()

def setT0():
    global t0
    t0 = time.time()

def timeSinceT0():
    return str(round(time.time() - t0, 2)) +'s'




    