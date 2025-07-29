import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from random import randrange
import threading
from colorama import Fore
from colorama import init as colorama_init
from time import time

colorama_init(autoreset=True)
rubik_cube = list()
solved_cube = list()


def faces(num_faces: str, face: str, translate: list, rotate: list, color_1="white", color_2="blue", color_3="white",
          color_line="black"):
    """Create the face base on color"""

    facesbuff = (
        (1, -1, -1),
        (1, 1, -1),
        (1, 1, 1),
        (1, -1, 1),  # One face stop len 4
        (-1, -1, 1),
        (-1, 1, 1),  # Two faces stop len 6
        (-1, 1, -1)
    )

    facesbordbuff = (
        (0, 1),
        (0, 3),
        (2, 3),
        (2, 1),  # One face stop len 4
        (2, 5),
        (3, 4),
        (5, 4),  # Two faces stop len 7 = 6 +1
        (5, 6),
        (6, 1)  # three faces stop len 10
    )

    insidefaces = (
        (0, 3, 2, 1),
        (2, 3, 4, 5),
        (1, 2, 5, 6)
    )

    numface = {"one": 4, "two": 7, "three": 10, "ONE": 0, "TWO": 1, "THREE": 2}
    numarea = {"one": 4, "two": 6, "three": 7}
    pair_colors = {"white": (1, 1, 1), "blue": (0, 0, 1), "red": (1, 0.2, 0.3), "orange": (1, 0.5, 0.1),
                   "green": (0, 1, 0), "yellow": (1, 1, 0), "black": (0, 0, 0)}

    glTranslated(translate[0], translate[1], translate[2])
    glRotated(rotate[0], rotate[1], rotate[2], rotate[3])

    glBegin(GL_QUADS)
    if face == "ONE":
        for vertex in insidefaces[numface.get(face)]:
            glColor3fv(pair_colors.get(color_1))
            glVertex3fv(facesbuff[vertex])
    elif face == "TWO":
        for vertex in insidefaces[numface.get("ONE")]:
            glColor3fv(pair_colors.get(color_1))
            glVertex3fv(facesbuff[vertex])
        for vertex in insidefaces[numface.get(face)]:
            glColor3fv(pair_colors.get(color_2))
            glVertex3fv(facesbuff[vertex])
    elif face == "THREE":
        for vertex in insidefaces[numface.get("ONE")]:
            glColor3fv(pair_colors.get(color_1))
            glVertex3fv(facesbuff[vertex])
        for vertex in insidefaces[numface.get("TWO")]:
            glColor3fv(pair_colors.get(color_2))
            glVertex3fv(facesbuff[vertex])
        for vertex in insidefaces[numface.get(face)]:
            glColor3fv(pair_colors.get(color_3))
            glVertex3fv(facesbuff[vertex])
    glEnd()

    glBegin(GL_LINES)
    count = 0
    for line in facesbordbuff:
        if count < numface.get(num_faces):
            for point in line:
                glColor3fv(pair_colors.get(color_line))
                glVertex3fv(facesbuff[point])
            count += 1
        else:
            break
    glEnd()

    # glTranslated(-(translate[0]), -(translate[1]), -(translate[2]))
    glRotated(-rotate[0], (rotate[1]), (rotate[2]), (rotate[3]))

def main():
    """Main code"""

    # Manual definition of layers
    first_layer = [["orange", "blue", "white"], ["white", "orange"], ["green", "orange", "white"],
                   ["green", "white"], ["green", "white", "red"], ["white", "red"], ["blue", "red", "white"],
                   ["blue", "white"], ["white"]]

    second_layer = [["orange", "blue"], ["orange"], ["orange", "green"], ["green"], ["red", "green"],
                    ["red"],
                    ["red", "blue"], ["blue"]]

    third_layer = [["blue", "orange", "yellow"], ["yellow", "orange"], ["yellow", "orange", "green"],
                   ["green", "yellow"], ["green", "red", "yellow"], ["yellow", "red"], ["yellow", "red", "blue"],
                   ["blue", "yellow"], ["yellow"]]

    # Build the cube base on previous layers
    global rubik_cube
    global solved_cube
    for layer in (first_layer, second_layer, third_layer):
        lay = layer
        for face in lay:
            rubik_cube.append(face)

    solved_cube = rubik_cube

    # Initialize pygame gui
    pygame.init()
    pygame.font.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    icon = pygame.image.load('rubik.png')
    pygame.display.set_icon(icon)
    font = pygame.font.SysFont('lucinda console', 64)
    pygame.display.set_caption("Rubik Cube")

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(6.0, -1.0, -20)  # Camera view
    glRotatef(45, 1, 1, 1)  # Prospective view

    # No overlapping
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    # Extra variables
    u_first_key = False
    u_key = False
    r_key = False
    m_key = False
    m_first_key = False
    z_key = False
    x_first_key = False
    shuffle_key = False
    sexy_key = False
    first_white_key = False
    cycle = 0
    m = 1
    prev_pos_x = 0
    prev_pos_y = 0

    # Show the cube on screen
    while True:

        # Check for pressed keys
        for event in pygame.event.get():
            # print(rubik_cube)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:  # Change camera view
                    glRotatef(20, 0, -1, 0)
                if event.key == pygame.K_f:  # Change camera view
                    glRotatef(20, 0, 1, 0)
                # if event.key == pygame.K_s:  # Change camera view
                #     glRotatef(10, 0, 2, 1)
                if event.key == pygame.K_d:  # Change camera view
                    glRotatef(90, 1, 0, 0)
                if event.key == pygame.K_ESCAPE:  # Exit
                    exit()

                # U' Move
                if event.key == pygame.K_f:
                    u_first_key = True

                # U Move
                if event.key == pygame.K_j:
                    u_key = True

                if event.key == pygame.K_r:
                    r_key = True

                # M Move
                if event.key == pygame.K_6:
                    rubik_cube = m_move(rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    m_key = True

                # M' Move
                if event.key == pygame.K_x:
                    rubik_cube = m_first_move(rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    m_first_key = True

                # Z Move
                if event.key == pygame.K_a:
                    z_key = True

                # X' Move
                if event.key == pygame.K_b:
                    x_first_key = True

                # Sexy Move
                if event.key == pygame.K_s:
                    sexy_key = True

                # Shuffle Move
                if event.key == pygame.K_a:
                    cycle = randrange(5, 100)
                    shuffle_key = True

                # First White
                if event.key == pygame.K_q:
                    first_white_key = True

        # Mouse Camera
        for event in pygame.mouse.get_pressed(3):
            if event:
                if abs(prev_pos_x - pygame.mouse.get_pos()[0]) == 0:
                    glRotatef(20, 1, 0, 0)  # Camera view
                elif abs(prev_pos_y - pygame.mouse.get_pos()[1]) == 0:
                    glRotatef(20, 0, 1, 0)  # Camera view
                elif abs(prev_pos_y - pygame.mouse.get_pos()[1]) > 1 and abs(
                        prev_pos_x - pygame.mouse.get_pos()[0]) > 1:
                    glRotatef(20, 1, 1, 0)  # Camera view
            prev_pos_x = pygame.mouse.get_pos()[0]
            prev_pos_y = pygame.mouse.get_pos()[1]

        # Clear view
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if u_first_key:
            rubik_cube = u_first_move(rubik_cube)
            u_first_key = False
        elif u_key:
            rubik_cube = u_move(rubik_cube)
            u_key = False
        elif r_key:
            rubik_cube = d_move(rubik_cube)
            r_key = False
        elif m_key:
            m_key = False
        elif m_first_key:
            m_first_key = False
        elif x_first_key:
            rubik_cube = x_first_move(rubik_cube)
            x_first_key = False
        elif z_key:
            rubik_cube = z_move(rubik_cube)
            z_key = False
        elif shuffle_key:
            rubik_cube = shuffle(cycle, rubik_cube)
            shuffle_key = False
        elif sexy_key:
            rubik_cube = sexy_move(rubik_cube)
            sexy_key = False
        elif first_white_key:
            threading.Thread(target=solving()).start()
            first_white_key = False

        # Show updated layer
        f_layer(rubik_cube[:9])
        s_layer(rubik_cube[9:17])
        t_layer(rubik_cube[17:])
        pygame.display.flip()
        pygame.time.wait(20)