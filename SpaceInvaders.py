#  Space Invaders
import turtle
import os
import math
import random
import platform
from pygame import mixer



#  Set Up the Screen
from pip._vendor.distlib.compat import raw_input

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("space_invaders_background.gif")
wn.tracer(0)
#  register the shapes
wn.register_shape("player.gif")
wn.register_shape("invader.gif")
 #  Draw Border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

#  set the score to 0
score = 0

#  Draw score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290,280)
scorestring = "Score: %s" %score
score_pen.write(scorestring,False,align ="left",font = ("Arial",14,"normal"))
score_pen.hideturtle()

#  Create the player turtle
player= turtle.Turtle()
player.setposition(0,-250)
player.color("green")
player.shape("player.gif")
player.penup()
player.tilt(90)
player.pensize(25)
player.speed(0)
player.speed = 0


#  choose number of enemies
number_of_enemies = 30
#  create an empty list of enemies
enemies = []

#  Add enemies to the list
for i in range(number_of_enemies):
    #  Create enemy
    enemies.append(turtle.Turtle())

enemy_start_x =-225
enemy_start_y = 250
enemy_number = 0

for enemy in enemies:
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(20)
    x = enemy_start_x + (50 * enemy_number)
    y = enemy_start_y
    enemy.setposition(x,y)
    enemy_number +=1
    if enemy_number == 10:
        enemy_start_y -= 50
        enemy_number = 0


enemyspeed = 0.2

#  Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.hideturtle()

bulletspeed = 5

#  Define bullet state
#  ready-ready to fire
#  fire- bullet is firing
bulletstate = "ready"

#  Move left and right
def move_left():
    player.speed =-1

def move_right():
    player.speed = 1

def move_player():
    x = player.xcor()
    x += player.speed
    if x< -280:
        x= -280
    if x> 280:
        x= 280
    player.setx(x)


def move_up():
    y=player.ycor()
    y +=player.speed+5
    if y>150:
        y=150
    player.sety(y)

def move_down():
    y = player.ycor()
    y -= player.speed + 5
    if y <-235:
        y = -235
    player.sety(y)

def fire_bullet():
    #  Deckare bulletstate as a global if it needs changed
    global bulletstate

    if bulletstate == "ready":
        play_sound("laser.wav")
        bulletstate = "fire"
        #  Move the bullet above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x,y)
        bullet.showturtle()

#  Collision formula
def isCollision(t1,t2):
        distance= math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
        if distance <15:
            return True
        else:
            return False

def play_sound(sound_file):
    mixer.init()
    mixer.music.load(sound_file)
    mixer.music.play()



#  Create keybord bindings
wn.listen()
wn.onkey(move_left,"Left")
wn.onkey(move_right,"Right")
wn.onkey(move_up, "Up")
wn.onkey(move_down, "Down")
turtle.onkey(fire_bullet,"space")

#  Play Background music

#  Main game loop
while True:

    wn.update()
    move_player()
    #  Move enemy
    for enemy in enemies:
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        #  Move the enemy back and down
        if enemy.xcor() >280:
            #  Moves all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
                #  Change Direction
            enemyspeed *= -1

        if enemy.xcor() <-280:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemyspeed *= -1

        #   Check collision player-enemy
        if isCollision(bullet,enemy):
            play_sound("explosion.wav")
            #   reset bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0,-400)
            #   reset enemy
            enemy.setposition(0,10000)
            #   Update score
            score +=10
            scorestring = "Score: %s" %score
            score_pen.clear()
            score_pen.write(scorestring,False,align ="left",font = ("Arial",14,"normal"))

        if isCollision(player,enemy):
            play_sound("explosion.wav")
            player.hideturtle()
            e.hideturtle()
            print("Game Over")
            break

    #   Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    #   Check to see if bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"
