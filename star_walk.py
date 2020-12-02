import sys
import pygame 
import random
import numpy

# pylint: disable=maybe-no-member

def r_1():
    return random.choice((1,-1))

def add_ball():
    balls_true_pos.append([random.randint(100, 1500) * r_1(), random.randint(100, 1500) * r_1()])
    balls_w.append(random.randint(5,120))
    print("Star added! ")

def add_n_balls(n=1):
    for i in range(n):
        add_ball()

def mass_add(l, v):
    for i in range(len(l)):
        l[i] += v

def push_stars_down(acel_rate):
    # modify index 1
    for i in range(len(balls_true_pos)):
        balls_true_pos[i][1] += acel_rate

def push_stars_up(acel_rate):
    push_stars_down(-acel_rate)

def push_stars_right(acel_rate):
    for i in range(len(balls_true_pos)):
        balls_true_pos[i][0] += acel_rate

def push_stars_left(acel_rate):
    push_stars_right(-acel_rate)

# Generate fake star background
size = width, height = 640, 480
bg = numpy.ndarray((width, height, 3))
for i in range(width):
    for j in range(height):
        if random.randint(0,1000) == 0:
            bg[i,j,0] = 30 
            bg[i,j,1] = 70
            bg[i,j,2] = 70
        else:
            bg[i,j] = 0
            bg[i,j,1] = 0
            bg[i,j,2] = 0

bg_game = pygame.surfarray.make_surface(bg)

FPS = 144

acel = 0.05
game_clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
ball = pygame.image.load("demoDot.png")
ball_cw = ball.get_width()/2
ball_ch = ball.get_height()/2

# for each element in the list, index 0 is the x value, index 1 y
balls_true_pos = [] # (999,999),(1500,1000), (800,400), (1500,200)]
balls_w = [] # 15,80,20,30]

# x is measured from the left most corner (of the ball)
# y is measured from the top most corner 

# control constants
reduce_w = False
increase_w = False
pan_left = False
pan_right = False
pan_up = False
pan_down = False

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            if event.button == 1: add_ball() # left click
            elif event.button == 2: add_n_balls(3)# middle mouse click
            elif event.button == 3: add_n_balls(5)# right click
        elif event.type == pygame.KEYDOWN:
            # 72 is down, 80 is up
            # A-30, W-17, S-31, P-32
            if event.scancode == 72: 
                reduce_w = True
            elif event.scancode == 80:
                increase_w = True
            elif event.scancode == 30:
                pan_left = True
            elif event.scancode == 31:
                pan_down = True
            elif event.scancode == 32:
                pan_right = True
            elif event.scancode == 17:
                pan_up = True
        elif event.type == pygame.KEYUP:
            if event.scancode == 72: 
                reduce_w = False
            elif event.scancode == 80:
                increase_w = False 
            elif event.scancode == 30:
                pan_left = False
            elif event.scancode == 31:
                pan_down = False
            elif event.scancode == 32:
                pan_right = False
            elif event.scancode == 17:
                pan_up = False
    if reduce_w: mass_add(balls_w, -acel)
    if increase_w: mass_add(balls_w, acel)
    if pan_up: push_stars_down(acel*100)
    if pan_down: push_stars_up(acel*100)
    if pan_left: push_stars_right(acel*100)
    if pan_right: push_stars_left(acel*100)

    # Render, and update screen
    screen.fill((0,0,0))
    screen.blit(bg_game, (0,0))
    for i in range(len(balls_w)):
        w = balls_w[i]
        if w > 0:
            ball_perspective_x = width/2 + (balls_true_pos[i][0] / w)
            ball_perspective_y = height/2 + (balls_true_pos[i][1] / w)
        if ball_perspective_x < width+10 and ball_perspective_y < height+10 and w > 0.005 and w < 20:
            screen.blit(ball, (ball_perspective_x, ball_perspective_y))

    game_clock.tick_busy_loop(FPS)
    pygame.display.flip()