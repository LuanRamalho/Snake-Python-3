import json
from turtle import *
import time
import random

score = 0
execution_delay = 0.1

# Carregar ou inicializar o HighScore
highscore_file = "highscore.json"
try:
    with open(highscore_file, "r") as file:
        highscore_data = json.load(file)
        highscore = highscore_data.get("HighScore", 0)
except (FileNotFoundError, json.JSONDecodeError):
    highscore = 0

root = Screen()
root.title('Snake Game')
root.setup(width=600, height=600)
root.bgcolor('black')
root.bgpic('border.gif')
root.tracer(False)
root.addshape('upmouth.gif')
root.addshape('food.gif')
root.addshape('downmouth.gif')
root.addshape('leftmouth.gif')
root.addshape('rightmouth.gif')
root.addshape('body.gif')

head = Turtle()
head.shape('upmouth.gif')
head.penup()
head.goto(0, 0)
head.direction = 'stop'

food = Turtle()
food.shape('food.gif')
food.penup()
food.goto(0, 100)

text = Turtle()
text.penup()
text.goto(0, 268)
text.hideturtle()
text.color('white')
text.write(f'Score: 0  HighScore: {highscore}', font=('courier', 25, 'bold'), align='center')

lost = Turtle()
lost.color('white')
lost.penup()
lost.hideturtle()

def move_snake():
    if head.direction == 'up':
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == 'down':
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == 'right':
        x = head.xcor()
        head.setx(x + 20)
    if head.direction == 'left':
        x = head.xcor()
        head.setx(x - 20)

def go_up():
    if head.direction != 'down':
        head.direction = 'up'
        head.shape('upmouth.gif')

def go_down():
    if head.direction != 'up':
        head.direction = 'down'
        head.shape('downmouth.gif')

def go_left():
    if head.direction != 'right':
        head.direction = 'left'
        head.shape('leftmouth.gif')

def go_right():
    if head.direction != 'left':
        head.direction = 'right'
        head.shape('rightmouth.gif')

root.listen()
root.onkeypress(go_up, 'Up')
root.onkeypress(go_down, 'Down')
root.onkeypress(go_left, 'Left')
root.onkeypress(go_right, 'Right')

segments = []
while True:
    root.update()

    if head.xcor() > 260 or head.xcor() < -260 or head.ycor() > 260 or head.ycor() < -260:
        lost.write('Game Lost', align='center', font=('courier', 34, 'bold'))
        time.sleep(1)
        lost.clear()
        time.sleep(1)
        head.goto(0, 0)
        head.direction = 'stop'

        for bodies in segments:
            bodies.goto(1000, 1000)

        segments.clear()
        if score > highscore:
            highscore = score
            with open(highscore_file, "w") as file:
                json.dump({"HighScore": highscore}, file)

        score = 0
        execution_delay = 0.1
        text.clear()
        text.write(f'Score: 0  HighScore: {highscore}', font=('courier', 25, 'bold'), align='center')

    if head.distance(food) < 20:
        x = random.randint(-255, 255)
        y = random.randint(-255, 255)
        food.goto(x, y)
        execution_delay -= 0.003

        body = Turtle()
        body.penup()
        body.shape('body.gif')
        segments.append(body)

        score += 10
        text.clear()
        text.write(f'Score: {score}  HighScore: {highscore}', font=('courier', 25, 'bold'), align='center')

    for i in range(len(segments) - 1, 0, -1):
        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()
        segments[i].goto(x, y)

    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move_snake()

    for bodies in segments:
        if bodies.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = 'stop'

            for bodies in segments:
                bodies.goto(1000, 1000)

            segments.clear()
            if score > highscore:
                highscore = score
                with open(highscore_file, "w") as file:
                    json.dump({"HighScore": highscore}, file)

            score = 0
            execution_delay = 0.1
            lost.write('Game Lost', align='center', font=('courier', 34, 'bold'))
            time.sleep(1)
            lost.clear()
            text.clear()
            text.write(f'Score: 0  HighScore: {highscore}', font=('courier', 25, 'bold'), align='center')

    time.sleep(execution_delay)
