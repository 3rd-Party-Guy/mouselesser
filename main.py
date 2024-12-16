import tkinter
import keyboard
from pynput.mouse import Controller, Button

isDrawingGrid = False
gridWin = None
gridCanvas = None

maxSelections = 4

selectionsMade = 0
gridStartX = 0
gridStartY = 0
gridWidth = 0
gridHeight = 0

mouse = Controller()

def CreateGridWin():
    global gridWin

    print("Create Grid Win")
    gridWin = tkinter.Tk()
    gridWin.geometry('1280x720')
    gridWin.configure(bg='red')

    gridWin.attributes('-fullscreen', True)
    gridWin.attributes('-transparentcolor', 'red')
    gridWin.attributes('-toolwindow', True)

    gridWin.bind('<Escape>', lambda e: gridWin.destroy())
    gridWin.bind('a', lambda e: UpdateGrid(0))
    gridWin.bind('s', lambda e: UpdateGrid(1))
    gridWin.bind('d', lambda e: UpdateGrid(2))
    gridWin.bind('f', lambda e: UpdateGrid(3))
    gridWin.bind('j', lambda e: UpdateGrid(4))
    gridWin.bind('k', lambda e: UpdateGrid(5))
    gridWin.bind('l', lambda e: UpdateGrid(6))
    gridWin.bind(';', lambda e: UpdateGrid(7))

    gridWin.focus_force()

def CreateGridCanvas():
    global gridWin
    global gridCanvas

    gridCanvas = tkinter.Canvas(gridWin, width=gridWin.winfo_screenwidth(), height=gridWin.winfo_screenheight(), bg="red")
    gridCanvas.pack()

def CheckShouldDrawGrid():
    global isDrawingGrid
    
    if (isDrawingGrid == False):
        isDrawingGrid = True
        CreateGridWin()
        CreateGridCanvas()
        RestartGridState()
        DrawGrid()

def RestartGridState():
    global gridStartX, gridStartY
    global gridWidth, gridHeight
    global selectionsMade
    global gridWin

    selectionsMade = 0
    gridStartX = 0
    gridStartY = 0
    gridWidth = gridWin.winfo_screenwidth()
    gridHeight = gridWin.winfo_screenheight()

def UpdateGrid(selectIndex):
    global gridStartX, gridStartY
    global gridWidth, gridHeight
    global selectionsMade
    global isDrawingGrid

    print('called with')
    print(selectIndex)

    selectionsMade += 1
    if (selectionsMade >= maxSelections):
        gridWin.destroy()
        MakeSelection()
        isDrawingGrid = False
        return

    gridHeight /= 2
    gridWidth /= 4

    gridStartX += gridWidth * (selectIndex % 4)
    if selectIndex > 3:
        gridStartY += gridHeight

    DrawGrid()

def DrawGrid():
    global gridWidth
    global gridHeight
    global gridWin
    global gridCanvas

    print('Draw Grid')

    gridCubeWidth = gridWidth / 4
    gridCubeHeight = gridHeight / 2

    lineFill = 'black'
    lineSize = 2

    gridCanvas.delete('all')

    # horizontal line
    gridCanvas.create_line(gridStartX, gridStartY + gridCubeHeight, gridStartX + gridWidth, gridStartY + gridCubeHeight, fill=lineFill, width=lineSize)

    # vertical lines
    for i in range(3):
        x = gridStartX + gridCubeWidth * (i + 1)
        yStart = gridStartY
        yEnd = gridStartY + gridHeight
        gridCanvas.create_line(x, yStart, x, yEnd, fill=lineFill, width=lineSize)

    gridWin.mainloop()

def MakeSelection():
    mouseX = gridStartX + gridWidth / 2
    mouseY = gridStartY + gridHeight / 2

    mouse.position = (mouseX, mouseY)
    mouse.press(Button.left)
    mouse.release(Button.left)

def Exit():
    print('exit')

keyboard.add_hotkey('alt+a', CheckShouldDrawGrid)
keyboard.add_hotkey('ctrl+c', Exit)

keyboard.wait('ctrl+c')