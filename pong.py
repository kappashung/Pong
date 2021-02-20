import math
from tkinter import *

root = Tk()
root.title("Pong")

WIDTH = root.winfo_screenwidth() * 0.45
HEIGHT = root.winfo_screenheight() * 0.4
COLOURS = ["grey", "blue", "pink", "red", "orange", "white", "purple", "pink", "yellow", "olive", "cyan"]
ball_rad = 15
hole_rad = 28
count = 15

Balls = []
Holes = []


class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.len = math.sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __mul__(self, other):
        self.x *= other
        self.y *= other
        return self


class Ball(object):

    def __init__(self, x, y, vx=0, vy=0):
        self.num = 0
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.vec = Vector(self.vx, self.vy)
        self.id = c.create_oval(self.x - ball_rad,
                                self.y - ball_rad,
                                self.x + ball_rad,
                                self.y + ball_rad, fill="white")


class Hole(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = c.create_oval(self.x - hole_rad,
                                self.y - hole_rad,
                                self.x + hole_rad,
                                self.y + hole_rad, fill="black")


c = Canvas(root, width=WIDTH, height=HEIGHT, background="#003300")
c.create_rectangle(0, 0, WIDTH, HEIGHT, fill='green', outline='brown', width=30)
c.pack()

main_ball = Ball(450, 214, 1, 0)
Balls.append(main_ball)
cue_line = c.create_line(main_ball.x, main_ball.y, main_ball.x, main_ball.y, fill="white")


def on_move(event):
    global cue_line
    c.delete(cue_line)
    cue_line = c.create_line(main_ball.x, main_ball.y, event.x, event.y, fill="white")


def onClick(event):
    global cue_line
    c.delete(cue_line)
    cue(event)


def cue(event):
    global cue_line
    main_ball.vec.x = (-event.x + main_ball.x) * 0.01
    main_ball.vec.y = (-event.y + main_ball.y) * 0.01


c.bind('<B1-Motion>', on_move)
c.bind('<ButtonRelease>', onClick)


def minus(vec):
    return Vector(-vec.x, -vec.y)


def vec_cos(v1, v2):
    if v1.len == 0 or v2.len == 0:
        return 0
    return (v1.x * v2.x + v1.y * v2.y) / (v1.len * v2.len)


def in_hole(ball):
    global main_ball
    for h in Holes:
        if (ball.x - h.x) ** 2 + (ball.y - h.y) ** 2 < hole_rad ** 2:
            c.delete(ball.id)
            Balls.remove(ball)


def hit_wall(ball):
    if ball.x - ball_rad <= 15 or ball.x + ball_rad >= WIDTH - 15:
        ball.vec.x *= -1
    if ball.y - ball_rad <= 15 or ball.y + ball_rad >= HEIGHT - 15:
        ball.vec.y *= -1


def hit_ball(ball1, ball2):
    if math.sqrt((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2) <= 2 * ball_rad:
        hit_vec = Vector((ball2.x - ball1.x) / (2 * ball_rad), (ball2.y - ball1.y) / (2 * ball_rad))
        ball2_vec = Vector(hit_vec.x * ball1.vec.len * vec_cos(ball1.vec, hit_vec),
                           hit_vec.y * ball1.vec.len * vec_cos(ball1.vec, hit_vec))
        ball1_vec = Vector(hit_vec.x * ball2.vec.len * vec_cos(ball2.vec, hit_vec),
                           hit_vec.y * ball2.vec.len * vec_cos(ball2.vec, hit_vec))
        ball1_vec1 = minus(ball2_vec)
        ball2_vec1 = minus(ball1_vec)
        ball1.vec += ball1_vec + ball1_vec1
        ball2.vec += ball2_vec + ball2_vec1
        ball1.x += minus(ball1.vec).x * 0.001
        ball1.y += minus(ball1.vec).y * 0.001
        ball2.x += minus(ball2.vec).x * 0.001
        ball2.y += minus(ball2.vec).y * 0.001
        c.move(ball1.id, ball1.vec.x * 0.001, ball1.vec.y * 0.001)
        c.move(ball2.id, ball2.vec.x * 0.001, ball2.vec.y * 0.001)


def hit_check(ball):
    hit_wall(ball)
    for i in Balls:
        if i == ball:
            continue
        hit_ball(ball, i)


def change_velocity(vec):
    if vec.len == 0:
        return
    var = Vector(-vec.x * 0.005 / vec.len, -vec.y * 0.005 / vec.len)
    if vec.len < var.len:
        vec.x = 0
        vec.y = 0
    vec += var


def move_ball(i):
    change_velocity(i.vec)
    hit_check(i)
    in_hole(i)
    i.x += i.vec.x
    i.y += i.vec.y
    c.move(i.id, i.vec.x, i.vec.y)


def begin():
    global main_ball
    Holes.append(Hole(15, 15))
    Holes.append(Hole(WIDTH - 15, 15))
    Holes.append(Hole(15, HEIGHT - 15))
    Holes.append(Hole(WIDTH - 15, HEIGHT - 15))
    Holes.append(Hole(WIDTH/2, 5))
    Holes.append(Hole(WIDTH/2, HEIGHT - 5))
    indent = 150
    for i in range(0, 5):
        for j in range(0, 5 - i):
            new_ball = Ball(50 + i * 30, indent + j * 32, 1, 0)
            Balls.append(new_ball)
        indent += 16
    c.delete(main_ball.id)
    main_ball.id = c.create_oval(main_ball.x - ball_rad,
                                 main_ball.y - ball_rad,
                                 main_ball.x + ball_rad,
                                 main_ball.y + ball_rad, fill="red")
    #Balls.append(Ball(800, 100))


def main():
    if main_ball not in Balls:
        c.create_text(430, 214, font="Times 30 italic bold", text="GAME OVER")
        return
    for i in Balls:
        move_ball(i)
    if Balls == [main_ball]:
        c.create_text(430, 214, font="Times 30 italic bold", text="END")
    root.after(5, main)


main_ball.id = c.create_oval(main_ball.x - ball_rad,
                             main_ball.y - ball_rad,
                             main_ball.x + ball_rad,
                             main_ball.y + ball_rad, fill="red")
# Balls.append(Ball(650, 244, Vector(0, 0)))
# Balls.append(Ball(650, 274, 0, 1))

begin()
main()

root.mainloop()
