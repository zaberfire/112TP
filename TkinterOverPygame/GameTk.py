import math
import random
from Asteroid import Asteroid
from Tkinter import *
from PIL import Image
from PIL import ImageTk

def init(data):
    data.timerCalled = 0
    data.mode = "title"
    data.level = 1
    
    data.fieldSizeW = 3 * data.width
    data.fieldSizeH = 3 * data.height
    data.scrollX = data.width
    data.scrollY = data.height
    data.scrollMarginX = data.width/2
    data.scrollMarginY = data.height/2
    
    Asteroid.init()
    data.asteroids = []
    data.margin = 51
    
    for i in range(5):
        x = random.randint(data.margin, data.fieldSizeW-data.margin)
        y = random.randint(data.margin, data.fieldSizeH-data.margin)
        data.asteroids.append(Asteroid(x,y,data.level))
    
    data.paused = False
    
    
    pilImg = baseImg = Image.open("images/asteroids2.png")
    data.astimage2 = [pilImg, baseImg, ImageTk.PhotoImage(pilImg)]
    data.angle = 0
    data.angleSpeed = 10
    
    data.background = Image.open("images/starryspace.png")
    data.background = data.background.resize((data.fieldSizeW, data.fieldSizeH), \
                                                Image.ANTIALIAS)
    data.background = ImageTk.PhotoImage(data.background)
    
    # testing scroll
    data.pX = data.fieldSizeW/2.
    data.pY = data.fieldSizeH/2.
    data.scrollSpeedX = data.width/10.
    data.scrollSpeedY = data.height/10.
    
def mousePressed(event, data):
    pass

def keyPressed(event, data):
    if data.mode == "title":
        titleKeyPressed(event, data)
    elif data.mode == "shop":
        shopKeyPressed(event, data)
    elif data.mode == "play":
        playKeyPressed(event, data)
    elif data.mode == "help":
        helpKeyPressed(event, data)
        
def timerFired(data):
    data.timerCalled += 1
    if data.mode == "title":
        titleTimerFired(data)
    elif data.mode == "shop":
        shopTimerFired(data)
    elif data.mode == "play":
        playTimerFired(data)
    elif data.mode == "help":
        helpTimerFired(data)
        
def redrawAll(canvas, data):
    canvas.create_image(0 - data.scrollX,0 - data.scrollY, anchor = NW, \
                                image = data.background)
    if data.mode == "title":
        titleRedrawAll(canvas,data)
    elif data.mode == "shop":
        shopRedrawAll(canvas,data)
    elif data.mode == "play":
        playRedrawAll(canvas,data)
    elif data.mode == "help":
        helpRedrawAll(canvas,data)

#### title screen events

def titleKeyPressed(event, data):
    if event.keysym.lower() == "p":
        data.mode = "play"
    elif event.keysym.lower() == "h":
        data.mode = "help"
    
def titleTimerFired(data):
    data.angle += data.angleSpeed
    PILimg = data.astimage2[0]
    baseImg = data.astimage2[1]
    PILimg = baseImg.rotate(data.angle)
    data.astimage2 = [PILimg, baseImg, ImageTk.PhotoImage(PILimg)]

def titleRedrawAll(canvas, data):
    
    canvas.create_image(data.width/2.,data.height/2., image = data.astimage2[2])
    canvas.create_text(data.width/2, 0, text = "Title Screen", anchor = N, \
                            font = ("Arial bold", 77), fill = "white")

#### play screen events

def playKeyPressed(event, data):
    if ((event.keysym.lower() == "a") or (event.keysym == "Left")):
        movePlayer(-data.scrollSpeedX, 0, data)
    elif ((event.keysym.lower() == "d") or (event.keysym == "Right")):
        movePlayer(data.scrollSpeedX, 0, data)
    elif ((event.keysym.lower() == "w") or (event.keysym == "Up")):
        movePlayer(0, -data.scrollSpeedY, data)
    elif ((event.keysym.lower() == "s") or (event.keysym == "Down")):
        movePlayer(0, data.scrollSpeedY, data)

def movePlayer(dx, dy, data):
    data.pX += dx
    data.pY += dy
    
    # scroll to make map visible as needed
    if (data.pX < data.scrollX + data.scrollMarginX):
        data.scrollX = data.pX - data.scrollMarginX
    if (data.pX > data.scrollX + data.width - data.scrollMarginX):
        data.scrollX = data.pX - data.width + data.scrollMarginX
    if (data.pY < data.scrollY + data.scrollMarginY):
        data.scrollY = data.pY - data.scrollMarginY
    if (data.pY > data.scrollY - data.height + data.scrollMarginY):
        data.scrollY = data.pY - data.scrollMarginY
    
def playTimerFired(data):
    if data.timerCalled % int(100 * (4./5)**data.level) == 0:
        x = random.randint(data.margin, data.fieldSizeW-data.margin)
        y = random.randint(data.margin, data.fieldSizeH-data.margin)
        ast = Asteroid(x,y)
        print(ast)
        data.asteroids.append(ast)
        
    for ast in data.asteroids:
        ast.update()
    

def playRedrawAll(canvas, data):
    for ast in data.asteroids:
        ast.draw(canvas, data)
    canvas.create_text(data.width/2, 0, text = "Play Screen", anchor = N, \
                            font = ("Arial bold", 77), fill = "white")

#### help screen events

def helpKeyPressed(event, data):
    if event.keysym.lower() == "b":
        data.mode = "title"
    
def helpTimerFired(data):
    pass

def helpRedrawAll(canvas, data):
    canvas.create_text(data.width/2, 0, text = "Help Screen", anchor = N, \
                            font = ("Arial bold", 77), fill = "white")

#### shop screen events

def shopKeyPressed(event, data):
    pass
    
def shopTimerFired(data):
    pass

def shopRedrawAll(canvas, data):
    pass

#################################################################
# use the run function as-is
#################################################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(777, 777)