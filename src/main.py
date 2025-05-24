from classes import Window, Line, Point, Cell, Maze


def main():
    win = Window(800, 600)
    maze_1 = Maze(50, 50, 50, 50, 25, 25, win)
    maze_1._Maze__break_entrance_and_exit()
    win.wait_for_close()






main()

