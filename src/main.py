from classes import Window, Line, Point, Cell, Maze


def main():
    win = Window(800, 600)
    maze_1 = Maze(50, 50, 20, 20, 25, 25, win)
    maze_1._Maze__break_entrance_and_exit()
    maze_1._Maze__break_walls_r(5,5)
    maze_1._Maze__reset_cells_visited()
    win.wait_for_close()






main()

