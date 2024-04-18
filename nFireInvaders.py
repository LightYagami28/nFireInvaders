import turtle
import random
import time
import pygame

# Initialize pygame for music management
pygame.init()

# Define constants for audio file names
TITLE_SCREEN_MUSIC = "mp3/TitleScreen.mp3"
GAME_OVER_MUSIC = "mp3/GameOver.mp3"
BATTLE_MUSIC = "mp3/InvaderHomeworld.mp3"
WIN_MUSIC = "mp3/LevelClear.mp3"

# Function to play the introduction music
def play_intro_music():
    pygame.mixer.music.load(TITLE_SCREEN_MUSIC)
    pygame.mixer.music.play(-1)  # Play in a loop

# Function to stop the introduction music
def stop_intro_music():
    pygame.mixer.music.stop()

# Function to play the game over sound
def play_game_over_sound():
    pygame.mixer.music.load(GAME_OVER_MUSIC)
    pygame.mixer.music.play()

# Function to stop the battle music
def stop_battle_music():
    pygame.mixer.music.stop()

# Function to play the battle music
def play_battle_music():
    pygame.mixer.music.load(BATTLE_MUSIC)
    pygame.mixer.music.play(-1)  # Play in a loop

# Function to play the win music
def play_win_music():
    pygame.mixer.music.load(WIN_MUSIC)
    pygame.mixer.music.play(-1)  # Play in a loop

# Initialize the Turtle screen
win = turtle.Screen()
win.title("nFire Invaders")
win.bgcolor("black")
win.setup(width=600, height=600)
win.tracer(0)

# Global variables
score = 0
powerups = []

# Initialize the introduction music
play_intro_music()

# Function to generate a power-up
def generate_powerup():
    powerup = turtle.Turtle()
    powerup.shape("square")
    powerup.color("blue")
    powerup.penup()
    powerup.speed(0)
    x = random.randint(-290, 290)
    y = random.randint(100, 250)
    powerup.goto(x, y)
    return powerup

def move_powerup(powerup):
    y = powerup.ycor()
    y -= invader_speed + 10
    powerup.sety(y)

def move_alien(alien):
    x = alien.xcor()
    x += alien.direction * 5
    alien.setx(x)

    # Change direction and lower the alien ship when it hits the edges
    if x > 290 or x < -290:
        alien.direction *= -1
        y = alien.ycor()
        y -= 40
        alien.sety(y)

def update_score():
    score_display.clear()
    score_display.write("SCORE: {}".format(score), align="left", font=("Courier", 12, "normal"))

def update_health_bar(health_bar, health):
    health_bar.clear()
    health_bar.write("HEALTH: {}".format(health), align="right", font=("Courier", 12, "normal"))

score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(-290, 260)
update_score()

# Health bar for the alien ship
health_bar = turtle.Turtle()
health_bar.speed(0)
health_bar.color("white")
health_bar.penup()
health_bar.hideturtle()
health_bar.goto(280, 260)
alien_health = 100
update_health_bar(health_bar, alien_health)

player = turtle.Turtle()
player.shape("triangle")
player.color("white")
player.penup()
player.speed(0)
player.goto(0, -250)
player.setheading(90)

player_speed = 30
bullet_speed = 3

def move_left():
    x = player.xcor()
    x -= player_speed
    if x < -290:
        x = -290
    player.setx(x)

def move_right():
    x = player.xcor()
    x += player_speed
    if x > 290:
        x = 290
    player.setx(x)

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

win.listen()
win.onkey(move_left, "Left")
win.onkey(move_right, "Right")
win.onkey(fire_bullet, "space")

num_invaders = 7
invaders = []

for _ in range(num_invaders):
    invader = turtle.Turtle()
    invader.shape("circle")
    invader.color("red")
    invader.penup()
    invader.speed(0)
    x = random.randint(-290, 290)
    y = random.randint(100, 250)
    invader.goto(x, y)
    invaders.append(invader)

stop_intro_music()  # Stop the introduction music before starting the battle

alien = turtle.Turtle()
alien.shape("square")
alien.color("green")
alien.penup()
alien.speed(0)
alien.goto(0, 200)
alien.direction = 1

invader_speed = 2
bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("yellow")
bullet.penup()
bullet.speed(10)
bullet.shapesize(stretch_wid=0.5, stretch_len=0.5)  # Make the alien ship's bullet thinner
bullet.hideturtle()
bullet_state = "ready"

def move_invaders():
    for invader in invaders:
        y = invader.ycor()
        y -= invader_speed
        invader.sety(y)

        if player.distance(invader) < 20:
            player.hideturtle()
            invader.hideturtle()
            print("GAME OVER!!!")
            play_game_over_sound()  # Play the game over sound
            win.bye()

        if y < -290:
            player.hideturtle()
            invader.hideturtle()
            print("GAME OVER!!!")
            play_game_over_sound()  # Play the game over sound
            win.bye()
    
    move_alien(alien)

    for powerup in powerups:
        move_powerup(powerup)

    win.update()
    win.ontimer(move_invaders, 100)

move_invaders()
play_battle_music()  # Start the battle music

start_time = time.time()
while True:
    if random.randint(1, 10000) == 1:
        powerup = generate_powerup()
        powerups.append(powerup)

    for powerup in powerups:
        if player.distance(powerup) < 20:
            powerup.hideturtle()
            powerups.remove(powerup)
            player_speed = 60
            invader_speed = 1

    if bullet_state == "fire":
        y = bullet.ycor()
        y += bullet_speed
        bullet.sety(y)

        for invader in invaders:
            if bullet.distance(invader) < 15:
                bullet.hideturtle()
                bullet_state = "ready"
                invader.hideturtle()
                score += 10
                update_score()

        if y > 290:
            bullet.hideturtle()
            bullet_state = "ready"

    if time.time() - start_time > 1000000:
        if alien.isvisible():
            move_alien(alien)

    # Check if player's bullet hits the alien ship
    if bullet_state == "fire" and bullet.distance(alien) < 15:
        bullet.hideturtle()
        bullet_state = "ready"
        alien_health -= 10
        update_health_bar(health_bar, alien_health)

        if alien_health <= 0:
            alien.hideturtle()
            print("YOU WIN!!!")
            win.bye()
            stop_battle_music()  # Stop the battle music
            play_win_music()  # Play the win music
