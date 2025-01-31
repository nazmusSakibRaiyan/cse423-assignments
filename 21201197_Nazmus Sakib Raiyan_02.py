import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import time


def getzone(x_start, y_start, x_end, y_end): #initial zone
    delta_x = x_end - x_start 
    delta_y = y_end - y_start
    if delta_x >= 0:
        if delta_y >= 0: # Zone 0 or 1
            return 0 if abs(delta_x) > abs(delta_y) else 1
        else: # Zone 7 or 6
            return 7 if abs(delta_x) > abs(delta_y) else 6
    else:
        if delta_y >= 0: # Zone 3 or 2
            return 3 if abs(delta_x) > abs(delta_y) else 2
        else: # Zone 4 or 5
            return 4 if abs(delta_x) > abs(delta_y) else 5


def convert_to_zone0(x_coord, y_coord, original_zone): 
    if original_zone == 0:
        return (x_coord, y_coord) 
    elif original_zone == 1:
        return (y_coord, x_coord) 
    elif original_zone == 2:
        return (y_coord, -x_coord)
    elif original_zone == 3:
        return (-x_coord, y_coord)
    elif original_zone == 4:
        return (-x_coord, -y_coord)
    elif original_zone == 5:
        return (-y_coord, -x_coord)
    elif original_zone == 6:
        return (-y_coord, x_coord)
    elif original_zone == 7:
        return (x_coord, -y_coord)


def convert_to_original_zone(x_coord, y_coord, original_zone): 
    if original_zone == 0:
        return (x_coord, y_coord)
    elif original_zone == 1:
        return (y_coord, x_coord)
    elif original_zone == 2:
        return (-y_coord, x_coord)
    elif original_zone == 3:
        return (-x_coord, y_coord)
    elif original_zone == 4:
        return (-x_coord, -y_coord)
    elif original_zone == 5:
        return (-y_coord, -x_coord)
    elif original_zone == 6:
        return (y_coord, -x_coord)
    elif original_zone == 7:
        return (x_coord, -y_coord)


def drawpixel(x, y, original_zone): 
    glPointSize(1)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def MidpointLine(x_start, y_start, x_end, y_end, color): #Midpoint Line Drawing Algorithm
    zone = getzone(x_start, y_start, x_end, y_end)
    x_start, y_start = convert_to_zone0(x_start, y_start, zone)
    x_end, y_end = convert_to_zone0(x_end, y_end, zone)
    glColor3f(*color)

    delta_x = x_end - x_start
    delta_y = y_end - y_start
    decision_param = 2 * delta_y - delta_x #initial decision parameter
    incrE = 2 * delta_y # decision parameter for E direction
    incrNE = 2 * (delta_y - delta_x) # decision parameter for NE direction

    current_x = x_start
    current_y = y_start

    while current_x < x_end: 
        if decision_param <= 0: #east
            decision_param += incrE
            current_x += 1
        else:
            decision_param += incrNE #north-east
            current_x += 1
            current_y += 1

        original_x, original_y = convert_to_original_zone(
            current_x, current_y, zone)
        drawpixel(original_x, original_y, zone)


def plotPoints(x_offset, y_offset, x_center, y_center): 
    glVertex2f(x_offset + x_center, y_offset + y_center) 
    glVertex2f(y_offset + x_center, x_offset + y_center)
    glVertex2f(-y_offset + x_center, x_offset + y_center)
    glVertex2f(-x_offset + x_center, y_offset + y_center)
    glVertex2f(-x_offset + x_center, -y_offset + y_center)
    glVertex2f(-y_offset + x_center, -x_offset + y_center)
    glVertex2f(y_offset + x_center, -x_offset + y_center)
    glVertex2f(x_offset + x_center, -y_offset + y_center)


def MidpointCircle(radius, x_center, y_center, color): #Midpoint Circle Drawing Algorithm
    current_x = 0
    current_y = radius
    decision_param = 1 - radius
    glColor3f(*color)

    glBegin(GL_POINTS)
    while current_x < current_y:
        if decision_param < 0:
            decision_param += 2 * current_x + 3 #east
            current_x += 1
        else:
            decision_param += 2 * (current_x - current_y) + 5 #south-east
            current_x += 1
            current_y -= 1
        plotPoints(current_x, current_y, x_center, y_center)
    glEnd()


WINDOW_X = 1200
WINDOW_Y = 1200


class Circle: 
    def __init__(self, x, num): 
        self.circle_color = (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1)) #random color for each circle
        self.x = x
        self.y = WINDOW_Y
        self.num = num 

    def draw(self):
        color = self.circle_color

        MidpointCircle(20, self.x, self.y - 20, color) #circle radius 20. center at (x, y-20), falling


class Bullet:
    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.dir_x = a
        self.dir_y = b

    def draw(self): 
        glColor3f(1.0, 0.0, 0.0)  
        num_parts = 50  
        radius = 6.0    
        glPointSize(2.0)  

        glBegin(GL_POINTS)
        for i in range(num_parts):
            angle = 2 * math.pi * i / num_parts  
            dx = radius * math.cos(angle)       
            dy = radius * math.sin(angle)       
            glVertex2f(self.x + dx, self.y + dy)
        glEnd()

spaceship_position = 0


class Game: 
    def __init__(self, game_paused, game_over):
        self.paused = game_paused
        self.game_over = game_over


class SpaceShip(Game):
    def __init__(self, game_paused, game_over): 
        super().__init__(game_paused, game_over) #inherit
        self.space_color = (255.0, 255.0, 0.0) 
        self.x = spaceship_position
        self.y = 1000 // 2
        self.r = 20 
        self.bullet_fired = []
        self.nose_x = self.x + 400 
        self.nose_y = 65

    def draw(self):
        color = self.space_color

        MidpointLine(400 + spaceship_position, 90,
                385 + spaceship_position, 50, color)
        MidpointLine(400 + spaceship_position, 90,
                415 + spaceship_position, 50, color)
        MidpointLine(385 + spaceship_position, 50,
                415 + spaceship_position, 50, color)

        MidpointLine(385 + spaceship_position, 50,
                385 + spaceship_position, 10, color)
        MidpointLine(415 + spaceship_position, 50,
                415 + spaceship_position, 10, color)
        MidpointLine(385 + spaceship_position, 10,
                415 + spaceship_position, 10, color)

        MidpointLine(385 + spaceship_position, 30,
                365 + spaceship_position, 10, color)
        MidpointLine(365 + spaceship_position, 10,
                385 + spaceship_position, 10, color)
        MidpointLine(415 + spaceship_position, 30,
                435 + spaceship_position, 10, color)
        MidpointLine(435 + spaceship_position, 10,
                415 + spaceship_position, 10, color)
        

        if not self.paused and not self.game_over: 
            for bullet in self.bullet_fired:
                if bullet.x > WINDOW_X or bullet.x < 0 or bullet.y > WINDOW_Y:
                    self.bullet_fired.remove(bullet) 
                else:
                    bullet.x += bullet.dir_x 
                    bullet.y += bullet.dir_y
                    bullet.draw()

    def shoot(self, dir_x, dir_y):
        bullet = Bullet(self.nose_x, self.nose_y, dir_x, dir_y)
        self.bullet_fired.append(bullet)  


WINDOW_X = 800 
WINDOW_Y = 600


game_paused = False
game_over = False
score = 0
count = 0

spaceship = SpaceShip(game_paused, game_over)
circles = []
circle_1 = 1 #initial speed of circle for level 1
circle_2 = 1 #initial speed of circle for level 2
click = False
circle_drawn_time = 0


def Pause():
    global game_paused, spaceship
    game_paused = not game_paused
    spaceship.paused = game_paused
    if game_paused:
        print("Game Paused")
    else:
        print("Game Resumed")


def reset_game_state(): 
    global game_paused, game_over, score, count, circle_1 ,circle_2
    game_paused = False
    game_over = False
    score = 0
    count = 0
    circle_1 = 1 
    circle_2 = 3


def reset_spaceship():
    global spaceship
    spaceship = SpaceShip(game_paused, game_over)


def reset_circles(no_of_circle):
    global circles
    circles = []
    create_circles(no_of_circle)


def restartGame():
    reset_game_state()
    reset_spaceship()
    reset_circles(3)
    glutPostRedisplay()


def draw_left_arrow():
    color = (0.8, 0.7, 0.0)
    MidpointLine(10, 580, 35, 580, color) 
    MidpointLine(10, 580, 20, 590, color) 
    MidpointLine(10, 580, 20, 570, color)


def draw_pause_symbol():
    color = (0.0, 1.0, 0.0)
    MidpointLine(10, 520, 10, 550, color)
    MidpointLine(15, 520, 15, 550, color)
    MidpointLine(30, 520, 30, 550, color)
    MidpointLine(35, 520, 35, 550, color)
    


def draw_play_symbol():
    color = (0.0, 1.0, 0.0)
    MidpointLine(10, 520, 10, 550, color)
    MidpointLine(35, 535, 10, 550, color)
    MidpointLine(35, 535, 10, 520, color)


def draw_cross():
    color = (1.0, 0.0, 0.0)
    MidpointLine(10, 500, 35, 475, color)
    MidpointLine(35, 500, 10, 475, color)


def draw_life1():
    color = (1.0, 0.0, 0.0)
    MidpointLine(10, 445, 22, 430, color)
    MidpointLine(10, 445, 16, 452, color)
    MidpointLine(16, 452, 22, 445, color)
    MidpointLine(34, 445, 28, 452, color)
    MidpointLine(28, 452, 22, 445, color)
    MidpointLine(22, 430, 34, 445, color)


def draw_life2():
    color = (1.0, 0.0, 0.0)
    MidpointLine(10, 415, 22, 400, color)
    MidpointLine(10, 415, 16, 422, color)
    MidpointLine(16, 422, 22, 415, color)
    MidpointLine(34, 415, 28, 422, color)
    MidpointLine(28, 422, 22, 415, color)
    MidpointLine(22, 400, 34, 415, color)


def draw_heart3():
    color = (1.0, 0.0, 0.0)
    MidpointLine(10, 385, 22, 370, color)
    MidpointLine(10, 385, 16, 392, color)
    MidpointLine(16, 392, 22, 385, color)
    MidpointLine(34, 385, 28, 392, color)
    MidpointLine(28, 392, 22, 385, color)
    MidpointLine(22, 370, 34, 385, color)


def update_background():
    global game_over
    if game_over:
        glClearColor(1.0, 1.0, 1.0, 0.0)
    else:
        glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)


def draw_life():
    global count
    if count == 0:
        draw_life1()
        draw_life2()
        draw_heart3()
    elif count == 1:
        draw_life2()
        draw_heart3()
    elif count == 2:
        draw_heart3()


def draw_ui_elements(): 
    draw_left_arrow() 
    if not game_paused: 
        draw_pause_symbol() 
    else:
        draw_play_symbol() 
    draw_cross()


def draw_circles():
    global circles, game_over
    if not game_over:
        for circle in circles:
            circle.draw()


def display():
    global spaceship
    update_background()
    spaceship.draw()
    draw_life()
    draw_ui_elements()
    draw_circles()
    glutSwapBuffers()


no_of_circle = 3


def create_circles(n):
    for i in range(n):
        circle = Circle(random.randint(5, WINDOW_X-5), i)
        circles.append(circle)


create_circles(no_of_circle)


def check_bullet_hits():
    global score, circle_1, circle_2, no_of_circle
    for bullet in spaceship.bullet_fired:
        for circle in circles:
            if bullet.x > circle.x - 40 and bullet.x < circle.x + 40 and bullet.y > circle.y - 60 and bullet.y < circle.y: #collision detection
                print('Hit!!')
                score += 1
                print("Score:", score)

                if score % 5 == 0 and score != 0:
                    circle_1 += 1 #speed increase
                    circle_2 += 1 
                    print("Speed Increased :()")

                spaceship.bullet_fired.remove(bullet)
                circles.remove(circle)
                no_of_circle -= 1


def update_circle_positions():
    global circles, count, no_of_circle, game_over
    for circle in circles:
        speed = random.randint(circle_1, circle_2) 
        circle.y -= speed
        if circle.y < 0:
            count += 1
            circles.remove(circle)
            no_of_circle -= 1
            print("Lost", count, "heart!")
        if count == 3:
            game_over = True
            print("Game Over!")
            print("Total score", score)


def regenerate_circles():
    global no_of_circle
    if no_of_circle <= 0:
        no_of_circle = random.randint(1, 5)
        create_circles(no_of_circle)


def animate(value):
    global game_over, game_paused

    if not game_over and not game_paused:
        check_bullet_hits()
        update_circle_positions()
        regenerate_circles()

    elif game_over:
        glutIdleFunc(None)

    glutTimerFunc(30, animate, 0) #30ms delay, 30fps
    glutPostRedisplay()


last_update_time = time.time()


def keyboard(key, x, y):
    global spaceship_position

    if not game_paused and not game_over:
        if key == b' ':
            spaceship.shoot(0, 2)

        elif key == b'a':
            spaceship_position -= 10
            if spaceship_position < -355:
                spaceship_position = -355 #restricting spaceship movement
        elif key == b'd':
            spaceship_position += 10
            if spaceship_position > 355:
                spaceship_position = 355

        spaceship.x = spaceship_position
        spaceship.nose_x = spaceship_position + 400 
        glutPostRedisplay()


def mouseClick(button, state, x, y):
    global game_over, game_paused, click

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN: 

        glutPostRedisplay()

        if 10 <= x <= 35 and 10 <= y <= 30:

            print("Starting over!") #
            restartGame()

        # elif 10 <= x <= 35 and 50 <= y <= 80:
        elif 50 <= x <= 55 and 80 <= y <= 110:
            Pause()

        elif 10 <= x <= 35 and 100 <= y <= 125:
            print("Goodbye!")
            glutLeaveMainLoop()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WINDOW_X, WINDOW_Y)
glutCreateWindow(b"Circle Shooter Game")
glClearColor(0.0, 0.0, 0.0, 0.0)
gluOrtho2D(0, 800, 0, 600)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouseClick)
glutTimerFunc(0, animate, 0)
glutKeyboardFunc(keyboard)
glutMainLoop()
