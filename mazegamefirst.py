import turtle
import math
import random
import pygame
from tkinter import *
from pygame import mixer
import winsound
counter=0
winsound.PlaySound("shhit",winsound.SND_FILENAME)
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("THE SOLVE & HIT")
wn.setup(700, 700)
wn.tracer(0)
wn.clear()

image = ["plright.gif","plleft.gif","deleft.gif","deright.gif","WALL 2.gif","TREASURE.gif"]
for image in image:
    turtle.register_shape(image)


class pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("black")
        self.penup()
        self.speed(0)

class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("plright.gif")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold = 0

    def go_up(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor()+24

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        move_to_x = self.xcor()-24
        move_to_y = self.ycor()

        self.shape("plleft.gif")

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()

        self.shape("plright.gif")

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def is_collision(self, other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a**2)+(b**2))

        if distance < 5:
            return True
        else:
            return False

class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("TREASURE.gif")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold=100
        self.goto(x, y)
    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("deleft.gif")
        self.color("red")
        self.penup()
        self.speed(0)
        self.gold = 25
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
            self.shape("deleft.gif")
        elif self.direction == "right":
            dx = 24
            dy = 0
            self.shape("deright.gif")
        else:
            dx = 0
            dy = 0

        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction = "left"
            elif player.xcor() > self.xcor():
                self.direction = "right"
            elif player.ycor() < self.ycor():
                self.direction = "down"
            elif player.ycor() > self.ycor():
                self.direction = "up"

        move_to_x = self.xcor()+dx
        move_to_y = self.ycor()+dy

        if (move_to_x, move_to_y)not in walls:
            self.goto(move_to_x, move_to_y)
        else:
            self.direction = random.choice(["up", "down", "right", "left"])

        turtle.ontimer(self.move, t=random.randint(100, 300))
    def is_close(self,other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a**2)+(b**2))

        if distance < 75:
            return True
        else:
            return False

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

levels = ["y"]

level_1 = [
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "xx     xx    x    xxxx     xxx",
    "x   x      xxx   xx      xxxxx",
    "x  xxP  x  xxxxxxx      xxxxxx",
    "xxxx    xxxxxx   x xxxxxx   xx",
    "xxxxx      x     xxx        xx",
    "xx      xxxxxxxxx        xxxxx",
    "xxxx     xxxxx     Ex      xxx",
    "xxxE    xxxx    x      x     x",
    "xx        xxxx     xx    xxxxx",
    "xxxxx   xxxxxxxx   xx    xxxxx",
    "xxx        xxxx  E  xxxxxxxxxx",
    "xxxxx     xxx       xx     xxx",
    "x         xxxxxxxxx      xxxxx",
    "xxx    E xxx      xxxxxxxxxxxx",
    "xxxxx      xxx       xxxxxxxxx",
    "xx     x      xx        xxxxxx",
    "xxx        x       xx       xx",
    "xxxx   x    xxxx        xxxxxx",
    "xxxx          xxxxx  T     xxx",
    "xxxxxxxx      xxxxxxxxxxxxxxxx",
    "xx         x      xxxxx    xxx",
    "xxxx     xxxxx       xxxxxxxxx",
    "xxxx   x     xxxxx       xxxxx",
    "x       xxx      xxx     xxxxx",
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
]
treasures = []

enemies = []

levels.append(level_1)

def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]

            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            if character == "x":
                pen.goto(screen_x, screen_y)

                pen.stamp()
                walls.append((screen_x, screen_y))
            if character == "P":
                player.goto(screen_x, screen_y)
            if character == "T":
                treasures.append(Treasure(screen_x, screen_y))
            if character == "E":
                enemies.append(Enemy(screen_x, screen_y))

pen = pen()
player = Player()
walls = []
setup_maze(levels[1])

turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")

wn.tracer(0)
wn.bgpic("Backss.gif")

for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)

pygame.init()
music = pygame.mixer.music.load("title.mp3")
pygame.mixer.music.play(-1)


while True:

    for treasure in treasures:
        if player.is_collision(treasure):

            player.gold += treasure.gold
            winsound.PlaySound("laser", winsound.SND_FILENAME)
            print("player gold: {}".format(player.gold))
            import quizany
            quizany.start()

            treasure.destroy()

            treasures.remove(treasure)

    for enemy in enemies:
        if player.is_collision(enemy):
            sound = mixer.Sound("explosion.wav")
            sound.play()
            counter += 1
            print(counter)
            if counter >= 10:
                sys.exit()
            print("dies")

        wn.update()
    pass
