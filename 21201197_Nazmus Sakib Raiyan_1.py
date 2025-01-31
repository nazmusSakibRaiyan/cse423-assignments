#Assignment 1 
#Task 1: Building a House in Rainfall
''' Task 1: Building a House in Rainfall
 i) Draw a house with a raindrop using the base primitives: points, lines, or
 triangles.
 You can use ONLY GL_POINTS, GL_LINES, or
 GL_TRIANGLES for designing this house. A diagram has been provided
 as an example. You can modify the house design to your liking. The
 rain drops should be animated to fall from top to bottom.
 ii) It has been raining unwantedly for the last few days, so let’s control its
 direction by designing a key that will change the direction of the rain when
 clicked (slightly bending the rainfall). Design this functionality such that the
 left arrow will gradually bend the rain to the left and the right arrow will
 gradually bend the rain to the right.
 iii) Formulate two more keys(assign whatever key you like); pressing one
 will gradually change the skin colour from dark to light simulating night to
 day, and the other will change it from light to dark simulating day to night .
 You must also consider the rain and the house visibility in different
 background colours'''

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random
W_Width, W_Height = 500, 500 #Window size

elements = []
for i in range(1000):
    temp = []
    temp.append(random.randint(0, W_Width))
    temp.append(random.randint(0, W_Height))
    temp.append(2)  # width of the drop
    temp.append(15)  # length of the drop
    elements.append(temp)


wind_direction = 0
fall_speed = 4
is_daytime = True
bg = 1


def drawHouse():
    global is_daytime, bg

    # Create a rectangle for the house
    #left triangle
    glColor3f(0.5, 0.5, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2d(100, 0) # bottom left
    glVertex2d(100, 250) # top left
    glVertex2d(400, 250) # top right
    glEnd()

    #right triangle
    glColor3f(0.5, 0.5, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2d(100, 0)
    glVertex2d(400, 0)
    glVertex2d(400, 250)
    glEnd()

    # Roof
    glColor3f(0.9, 0.9, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2d(100, 250)
    glVertex2d(250, 400)
    glVertex2d(400, 250)
    glEnd()

    # Door
    #1st triangle
    glColor3f(0.5, 0.35, 0.1)
    glBegin(GL_TRIANGLES)
    glVertex2d(200, 0)
    glVertex2d(200, 150)
    glVertex2d(300, 150)
    glEnd()

    #2nd triangle
    glColor3f(0.5, 0.35, 0.1)
    glBegin(GL_TRIANGLES)
    glVertex2d(200, 0)
    glVertex2d(300, 0)
    glVertex2d(300, 150)
    glEnd()


def draw_rains():
    global elements, wind_direction
    for drop in elements:
        glColor3f(0.0, 0.0, 1.0)
        glLineWidth(drop[2]) # width of the drop
        glBegin(GL_LINES)
        x_axis_drop = drop[0] - wind_direction 
        y_axis_drop = drop[1] # length of the drop
        glVertex2f(x_axis_drop, y_axis_drop) #Starting point of the rain
        glVertex2f(drop[0], drop[1] - drop[3]) #ending point of the rain
        glEnd()


# def keyboardListener(key, x, y):
#     glutPostRedisplay() 


def specialKeyListener(key, x, y):
    global wind_direction
    if key == GLUT_KEY_LEFT: 
        wind_direction -= 2
    if key == GLUT_KEY_RIGHT:
        wind_direction += 2
    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global is_daytime
    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            is_daytime = False # Night
    elif button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            is_daytime = True # Day
    glutPostRedisplay()


def display():
    global is_daytime, bg
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(bg, bg,
                 bg, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)

    draw_rains() #1st layer
    drawHouse() #2nd layer

    glutSwapBuffers()


def animate():
    global elements, W_Width, W_Height, fall_speed, wind_direction, is_daytime, bg

    bg = 1 if is_daytime else 0
    for raindrop in elements:
        raindrop[1] = (raindrop[1] - fall_speed) % W_Height
        if wind_direction:
            raindrop[0] = (raindrop[0] + wind_direction) % W_Width

    glutPostRedisplay()


def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W_Width, 0, W_Height, -1, 1)


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"Task 1:Building a House in Rainfall")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)

#glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()

















#Assignmet 1
#Task 2: Building the Amazing Box


# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import random
# import time

# W_Width, W_Height = 500, 500 # Window Width and Height
# Outer_Box_Size = 500
# Inner_Box_Size = 450

# points = [] 
# speed = 0.1 # Speed of the balls
# is_freeze = False
# blink_start_time = None
# is_flashing = False


# def convert_coordinate(x, y):
#     a = x
#     b = W_Height - y
#     return a, b


# def drawRectWithCoordinate(bottom_left_x, bottom_left_y, top_right_x, top_right_y):
#     glBegin(GL_TRIANGLES)
#     glVertex2d(bottom_left_x, bottom_left_y)
#     glVertex2d(top_right_x, bottom_left_y)
#     glVertex2d(bottom_left_x, top_right_y)
#     glVertex2d(top_right_x, bottom_left_y)
#     glVertex2d(bottom_left_x, top_right_y)
#     glVertex2d(top_right_x, top_right_y)
#     glEnd()


# def drawBox():
#     # inner box
#     glColor3f(0.0, 0.0, 0.0) # black
#     drawRectWithCoordinate(50, 50, 450, 450)


# def keyboardListener(key, x, y):
#     global is_freeze
#     if key == b' ': #press space to freeze
#         is_freeze = not is_freeze
#     glutPostRedisplay()


# def specialKeyListener(key, x, y):
#     global speed, is_freeze
#     if not is_freeze:
#         if key == GLUT_KEY_UP:
#             speed *= 2 #to faster the balls
#         if key == GLUT_KEY_DOWN:
#             speed /= 2
#     glutPostRedisplay()


# def mouseListener(button, state, x, y):
#     global points, is_freeze, blink_start_time, is_flashing
#     if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and x > 50 and x < 450 and y > 50 and y < 450 and not is_freeze: #add new ball in inner box
#         x, y = convert_coordinate(x, y)
#         color = (
#             round(random.uniform(0.3, 1), 2),
#             round(random.uniform(0.3, 1), 2),
#             round(random.uniform(0.3, 1), 2)
#         )
#         direction = random.choice(
#             ["tl", "tr", "bl", "br"]
#         )
#         points.append([x, y, color, direction])
#     if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and x > 50 and x < 450 and y > 50 and y < 450:
#         if not is_freeze and not is_flashing:
#             blink_start_time = time.time()
#             is_flashing = True

#     glutPostRedisplay()


# def drawPoints():
#     global points, is_freeze, is_flashing
#     glPointSize(10)
#     for point in points:
#         x, y, color, direction = point
#         if is_flashing:
#             glColor3f(0, 0, 0) 
#         else:
#             glColor3f(*color)
#         glBegin(GL_POINTS)
#         glVertex2d(x, y)
#         glEnd()


# def display():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glClearColor(0.7, 0.7, 0.7, 0) 
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()
#     glMatrixMode(GL_MODELVIEW)

#     drawBox()
#     drawPoints()

#     glutSwapBuffers()


# def animate():
#     global points, speed, is_freeze, blink_start_time, is_flashing
#     if not is_freeze:

#         if is_flashing:
#             current_time = time.time()
#             if current_time - blink_start_time >= 1:  # 1 second
#                 is_flashing = False
#                 blink_start_time = None

#         for point in points:
#             x, y, color, direction = point #tuple unpacking
#             if direction == "tl": #top left
#                 x -= speed
#                 y += speed
#             elif direction == "tr": #top right
#                 x += speed
#                 y += speed
#             elif direction == "bl": #bottom left
#                 x -= speed
#                 y -= speed
#             elif direction == "br": #bottom right
#                 x += speed
#                 y -= speed
#             if x >= 450 or x <= 50: #ball hits the wall
#                 if direction == "tl":
#                     direction = "tr"
#                 elif direction == "tr":
#                     direction = "tl"
#                 elif direction == "bl":
#                     direction = "br"
#                 elif direction == "br":
#                     direction = "bl"
#             if y >= 450 or y <= 50:
#                 if direction == "tl":
#                     direction = "bl"
#                 elif direction == "tr":
#                     direction = "br"
#                 elif direction == "bl":
#                     direction = "tl"
#                 elif direction == "br":
#                     direction = "tr"
#             point[0], point[1], point[3] = x, y, direction

#     glutPostRedisplay()


# def init():
#     glClearColor(0, 0, 0, 0)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(0, W_Width, 0, W_Height, -1, 1)


# glutInit()
# glutInitWindowSize(W_Width, W_Height)
# glutInitWindowPosition(0, 0)
# glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

# wind = glutCreateWindow(b"Task 2: Building the Amazing Box")
# init()

# glutDisplayFunc(display)
# glutIdleFunc(animate)

# glutKeyboardFunc(keyboardListener)
# glutSpecialFunc(specialKeyListener)
# glutMouseFunc(mouseListener)

# glutMainLoop()



