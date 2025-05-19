from tkinter import Tk, BOTH, Canvas
import time


class Window:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.bind('<Meta-q>', lambda e: self.close())
        self.canvas = Canvas(self.__root, width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=True)
        self.window_running = False


    def draw_line(self, line: "Line", fill_color: str):
        line.draw(self.canvas, fill_color)


    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
 

    def wait_for_close(self):
        self.window_running = True

        while self.window_running == True:
            self.redraw()


    def close(self):
        print("Closing window...")
        self.window_running = False
        self.__root.destroy()


class Point:
    def __init__(self, x: int | float, y: int | float):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point_1: Point, point_2: Point):
        self.point_1 = point_1
        self.point_2 = point_2


    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point_1.x, self.point_1.y, self.point_2.x, self.point_2.y, fill=fill_color, width=2
        )

class Cell:
    def __init__(self, window: Window):
        #Give the cell walls.
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1

        self.__win = window
    


    def draw(self, x1: int | float, y1: int | float, x2: int | float, y2: int | float):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        
        if self.has_left_wall == True:
            left_line = Line(Point(x1, y1), Point(x1, y2))
            self.__win.draw_line(left_line, "black")
        if self.has_right_wall == True:
            right_line = Line(Point(x2, y1), Point(x2, y2))
            self.__win.draw_line(right_line, "black")
        if self.has_top_wall == True:
            top_line = Line(Point(x1, y1), Point(x2, y1))
            self.__win.draw_line(top_line, "black")
        if self.has_bottom_wall == True:
            bottom_line = Line(Point(x1, y2), Point(x2, y2))
            self.__win.draw_line(bottom_line, "black")


    def draw_move(self: "Cell", to_cell: "Cell", undo=False):
        fill_color = "red" if not undo else "gray"
        
        from_cell_center_x = (self.__x1 + self.__x2) / 2
        from_cell_center_y = (self.__y1 + self.__y2) / 2
        
        to_cell_center_x = (to_cell.__x1 + to_cell.__x2) / 2
        to_cell_center_y = (to_cell.__y1 + to_cell.__y2) / 2

        move_line = Line(Point(from_cell_center_x, from_cell_center_y), Point(to_cell_center_x, to_cell_center_y))

        self.__win.draw_line(move_line, fill_color)


class Maze:
    def __init__(
        self,
        x1: int | float,
        y1: int | float,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.__cells = []
        self.__create_cells()


    def __create_cells(self):
        self.__cells = [[Cell(self.win) for rows in range(self.num_rows)]for cols in range(self.num_cols)]
        for j in range(self.num_rows):

            for i in range(self.num_cols):

                self.__draw_cell(i, j)


    def __draw_cell(self, i, j):

        x = self.x1 + (i * self.cell_size_x)
        y = self.y1 + (j * self.cell_size_y)

        cell = self.__cells[i][j]

        cell.draw(x, y, x + self.cell_size_x, y + self.cell_size_y)

        self.animate()


    def animate(self):
        self.win.redraw()
        time.sleep(0.50)
        

