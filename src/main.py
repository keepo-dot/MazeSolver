from classes import Window, Line, Point


def main():
    win = Window(800, 600)
    line_1 = Line(Point(0, 100), Point(45, 70))
    line_2 = Line(Point(32, 64), Point(21, 83))
    win.draw_line(line_1, "black")
    win.draw_line(line_2, "black")
    win.wait_for_close()






main()

