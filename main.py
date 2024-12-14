from pynput import mouse, keyboard

def CheckShouldDrawGrid():
    print('Draw Grid Now')

hotkeys = keyboard.GlobalHotKeys({
    '<alt>+a': CheckShouldDrawGrid
})
hotkeys.start()

while True:
    continue
