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
selectionIndex = 0

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

    gridWin.bind('<Escape>', lambda e: CancelSelection())
    gridWin.bind('<Return>', lambda e: MakeSelectionMiddle())
    gridWin.bind('a', lambda e: UpdateGrid(0))
    gridWin.bind('s', lambda e: UpdateGrid(1))
    gridWin.bind('d', lambda e: UpdateGrid(2))
    gridWin.bind('f', lambda e: UpdateGrid(3))
    gridWin.bind('j', lambda e: UpdateGrid(4))
    gridWin.bind('k', lambda e: UpdateGrid(5))
    gridWin.bind('l', lambda e: UpdateGrid(6))
    gridWin.bind(';', lambda e: UpdateGrid(7))

    gridWin.focus_force()

def CancelSelection():
    global gridWin
    global isDrawingGrid

    gridWin.destroy()
    isDrawingGrid = False

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

def UpdateGrid(index):
    global gridStartX, gridStartY
    global gridWidth, gridHeight
    global selectionsMade
    global selectionIndex
    global isDrawingGrid

    selectionIndex = index

    selectionsMade += 1
    if (selectionsMade >= maxSelections):
        MakeSelection()
        return

    gridHeight /= 2
    gridWidth /= 4

    gridStartX += gridWidth * (index % 4)
    if index > 3:
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
    global gridWin
    global isDrawingGrid
    global mouse

    mouse.position = GetGridMiddle()
    mouse.press(Button.left)
    mouse.release(Button.left)

    gridWin.destroy()
    isDrawingGrid = False

def MakeSelectionMiddle():
    global gridWin
    global gridWidth, gridHeight
    global gridStartX,gridStartY
    global isDrawingGrid
    global mouse

    x = gridStartX + gridWidth / 2
    y = gridStartY + gridHeight / 2

    mouse.position = (x, y)
    mouse.press(Button.left)
    mouse.release(Button.left)

    gridWin.destroy()
    isDrawingGrid = False

def GetGridMiddle():
    global gridWidth, gridHeight
    global gridStartX, gridStartY
    global selectionIndex

    column = selectionIndex % 4
    row = 0 if selectionIndex < 4 else 1

    cellWidth = gridWidth / 4
    cellHeight = gridHeight / 2

    middleX = gridStartX + column * cellWidth + cellWidth / 2
    middleY = gridStartY + row * cellHeight + cellHeight / 2

    return middleX, middleY

def Exit():
    print('exit')

keyboard.add_hotkey('alt+a', CheckShouldDrawGrid)
keyboard.add_hotkey('ctrl+c', Exit)

keyboard.wait('ctrl+c')