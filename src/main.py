from classes import Window, Line, Point, Cell, Maze
import sys
sys.setrecursionlimit(20000)  # or whatever number you need
WIN_HEIGHT = 768
WIN_WIDTH = 1024
def main():
    win = Window(WIN_WIDTH, WIN_HEIGHT)
    maze_1 = Maze(25, 25, 200, 200, 5, 5, win)
    maze_1._Maze__break_entrance_and_exit()
    maze_1._Maze__break_walls_r(15, 15)
    maze_1._Maze__reset_cells_visited()
    maze_1.solve()
    win.wait_for_close()






main()

