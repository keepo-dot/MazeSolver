from classes import Window, Line, Point, Cell, Maze


def main():
    win = Window(800, 600)
    maze_1 = Maze(50, 50, 20, 20, 50, 50, win)
    win.wait_for_close()






main()

