from tkinter import Tk, BOTH, Canvas
import time, random


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
    def __init__(self, window: Window | None = None, i: int | None = None, j: int | None = None):
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

        self.visited = False
        self.i = i
        self.j = j


    def draw(self, x1: int | float, y1: int | float, x2: int | float, y2: int | float):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        
        left_line = Line(Point(x1, y1), Point(x1, y2))
        right_line = Line(Point(x2, y1), Point(x2, y2))
        top_line = Line(Point(x1, y1), Point(x2, y1))
        bottom_line = Line(Point(x1, y2), Point(x2, y2))



        if self.__win != None:           
            if self.has_left_wall == True:                
                self.__win.draw_line(left_line, "black")
            if self.has_left_wall == False:
                self.__win.draw_line(left_line, "#d9d9d9")

            elif self.has_right_wall == True:
                self.__win.draw_line(right_line, "black")
            elif self.has_right_wall == False:
                self.__win.draw_line(right_line, "#d9d9d9")

            if self.has_top_wall == True:
                self.__win.draw_line(top_line, "black")
            if self.has_top_wall == False:
                self.__win.draw_line(top_line, "#d9d9d9")

            if self.has_bottom_wall == True:
                self.__win.draw_line(bottom_line, "black")
            if self.has_bottom_wall == False:
                self.__win.draw_line(bottom_line, "#d9d9d9")


    def draw_move(self: "Cell", to_cell: "Cell", undo=False):
        fill_color = "red" if not undo else "gray"
        
        from_cell_center_x = (self.__x1 + self.__x2) / 2
        from_cell_center_y = (self.__y1 + self.__y2) / 2
        
        to_cell_center_x = (to_cell.__x1 + to_cell.__x2) / 2
        to_cell_center_y = (to_cell.__y1 + to_cell.__y2) / 2

        move_line = Line(Point(from_cell_center_x, from_cell_center_y), Point(to_cell_center_x, to_cell_center_y))
        if self.__win != None:
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
        win: Window | None = None,
        seed: int | None = None
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
        if seed != None:
            random.seed(seed)


    def __create_cells(self):
        self.__cells = [[Cell(self.win) for rows in range(self.num_rows)]for cols in range(self.num_cols)]
        if self.win != None:    
            for j in range(self.num_rows):

                for i in range(self.num_cols):
                    self.__cells[i][j].i = i
                    self.__cells[i][j].j = j
                    self.__draw_cell(i, j)


    def __draw_cell(self, i, j):

        x = self.x1 + (i * self.cell_size_x)
        y = self.y1 + (j * self.cell_size_y)

        cell = self.__cells[i][j]
        if self.win != None:
            cell.draw(x, y, x + self.cell_size_x, y + self.cell_size_y)
            self._animate()


    def _animate(self, timer=0.00):
        def __init__(self):
            self.timer = timer
        if self.win != None:
            self.win.redraw()
            time.sleep(timer)
        

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0,0)
        self.__cells[self.num_rows - 1][self.num_cols - 1].has_bottom_wall = False
        self.__draw_cell(self.num_rows - 1, self.num_cols - 1)


    def __break_walls_r(self, i, j):
        current_cell = self.__cells[i][j]
        current_cell.visited = True

        while 1:

            need_to_visit = []
            right_cell = None
            bottom_cell = None
            left_cell = None
            top_cell = None
            # right cell check
            if i + 1 < self.num_cols and self.__cells[i + 1][j].visited == False:
                right_cell = self.__cells[i + 1][j]
                need_to_visit.append(right_cell)
            # bottom cell check
            if j + 1 < self.num_rows and self.__cells[i][j + 1].visited == False:
                bottom_cell = self.__cells[i][j + 1]
                need_to_visit.append(bottom_cell)
            # left cell check
            if  i - 1 >= 0 and self.__cells[i - 1][j].visited == False:
                left_cell = self.__cells[i - 1][j]
                need_to_visit.append(left_cell)
            # top cell check
            if j - 1 >= 0 and self.__cells[i][j - 1].visited == False:
                top_cell = self.__cells[i][j - 1]
                need_to_visit.append(top_cell)
            
            if len(need_to_visit) == 0:
                self.__draw_cell(i,j)
                return
            next_cell = random.choice(need_to_visit)
            
            #right cell wallbreak
            if next_cell == right_cell:
                next_cell.has_left_wall = False
                current_cell.has_right_wall = False
            # bottom cell wallbreak
            if next_cell == bottom_cell:
                next_cell.has_top_wall = False
                current_cell.has_bottom_wall = False
            # left cell wallbreak
            if next_cell == left_cell:
                next_cell.has_right_wall = False
                current_cell.has_left_wall = False
            # top cell wallbreak
            if next_cell == top_cell:
                next_cell.has_bottom_wall = False
                current_cell.has_top_wall = False
            self.__draw_cell(i,j)
            self.__break_walls_r(next_cell.i, next_cell.j)


    def __reset_cells_visited(self):
        for j in range(self.num_cols):
            for i in range(self.num_rows):
                self.__cells[j][i].visited = False
        return
    
    def solve(self):
        self._solve_r(0,0)
        return self._solve_r(0,0)

    def _solve_r(self, i, j):
        self._animate(0.02)
        end_cell = self.__cells[self.num_cols - 1][self.num_rows - 1]
        current_cell = self.__cells[i][j]
        current_cell.visited = True
        
        if current_cell == end_cell:
            return True

        # right cell check
        if i + 1 < self.num_cols and self.__cells[i + 1][j].visited == False and self.__cells[i + 1][j].has_left_wall == False:
            right_cell = self.__cells[i + 1][j]
            current_cell.draw_move(right_cell)
            if self._solve_r(i + 1, j):
                return True
            right_cell.draw_move(current_cell, undo=True)


        # bottom cell check
        if j + 1 < self.num_rows and self.__cells[i][j + 1].visited == False and self.__cells[i][j + 1].has_top_wall == False:
            bottom_cell = self.__cells[i][j + 1]
            current_cell.draw_move(bottom_cell)
            if self._solve_r(i, j + 1):
                return True
            bottom_cell.draw_move(current_cell, undo=True)


        # left cell check
        if  i - 1 >= 0 and self.__cells[i - 1][j].visited == False and self.__cells[i - 1][j].has_right_wall == False:
            left_cell = self.__cells[i - 1][j]
            current_cell.draw_move(left_cell)
            if self._solve_r(i - 1, j):
                return True
            left_cell.draw_move(current_cell, undo=True)


        # top cell check
        if j - 1 >= 0 and self.__cells[i][j - 1].visited == False and self.__cells[i][j - 1].has_bottom_wall == False:
            top_cell = self.__cells[i][j - 1]
            current_cell.draw_move(top_cell)
            if self._solve_r(i, j - 1):
                return True
            top_cell.draw_move(current_cell, undo=True)
        return False

        


