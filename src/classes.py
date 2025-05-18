from tkinter import Tk, BOTH, Canvas


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
        self.window_running = False
        self.__root.destroy


class Point:
    def __init__(self, x, y):
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


