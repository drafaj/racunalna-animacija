import numpy as np

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

def ucitaj(obj, skaliraj):
    f = open(obj, "r")
    vertices=[]
    surfaces=[]
    maks = -10000
    mini = 10000
    for line in f:
        if line.startswith("v"):
            l = line.replace("v", "")
            l = l.strip()
            res = tuple(map(float, l.split(" ")))
            if max(res) > maks:
                maks = max(res)
            if min(res) < mini:
                mini = min(res)
            vertices.append(res)
        if line.startswith("f"):
            l = line.replace("f", "")
            l = l.strip()
            res = tuple(map(int, l.split(" ")))
            surfaces.append(res)

    if skaliraj:
        vertices2 = []
        for v in vertices:
            res = []
            for br in v:
                novi = (((br - mini) * (1 + 1)) / (maks - mini)) - 1
                res.append(novi)
            vertices2.append(res)

        vertices = vertices2

    return vertices, surfaces

def krivulja(file):
    control=[]
    f = open(file, "r")
    for line in f:
        res = tuple(map(float, line.split(" ")))
        control.append(res)

    return control

def Draw():
    glBegin(GL_TRIANGLES)
    glColor3fv((0,0.2,0.5))
    for surface in surfaces:
        for vertex in surface:
            glVertex3fv(vertices[vertex-1])
    glEnd()

B = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
Btang = np.array([[-1, 3, -3, 1], [2, -4, 2, 0], [-1, 0, 1, 0]])

def Spline():
    glBegin(GL_POINTS)
    glColor3fv((1,1,1))
    for vertex in control:
        glVertex3fv(vertex)
    glEnd()
    
    for i in range(len(control) - 3):
        R = np.array([control[i], control[i+1], control[i+2], control[i+3]])
        glBegin(GL_LINE_STRIP)
        glColor3fv((1,0,0))
        for t in np.arange(0.0, 1.1, 0.1):
            T  = np.array([t**3, t**2, t, 1])
            T = T*1/6
            a = np.matmul(T, B)
            p = np.matmul(a, R)

            Ttang  = np.array([t**2, t, 1])
            Ttang = Ttang*1/2
            a = np.matmul(Ttang, Btang)
            ptang = np.matmul(a, R)
            
            glVertex3fv(p)
            
        glEnd()
        
        glBegin(GL_LINES)
        glColor3fv((1,1,1))
        glVertex3fv(p)
        r = p + ptang*1/2
        glVertex3fv(r)
        glEnd()

def Rotation(e):
    s = np.array([0.0, 0.0, 1.0])
    os =np.array([s[1]*e[2] - e[1]*s[2], -s[0]*e[2] + e[0]*s[2], s[0]*e[1] - s[1]*e[0]])

    skalarni = np.dot(s, e)
    nazivnik = np.linalg.norm(s) * np.linalg.norm(e)
    kosinus = skalarni/nazivnik
    rad = np.arccos(kosinus)
    kut = np.degrees(rad)

    return os, kut

vertices, surfaces = ucitaj("tetrahedron.txt", True)
control = krivulja("srce.txt")

if __name__=="__main__":
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    glMatrixMode(GL_PROJECTION);
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, 0.0, -15)
    #glRotatef(30, -1, 0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #glRotatef(1, 3, 1, 1)
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #Cube()
        #Spiral()
        glPushMatrix()
        
        for i in range(len(control) - 3):
            R = np.array([control[i], control[i+1], control[i+2], control[i+3]])
            for t in np.arange(0.0, 1.1, 0.1):
                T  = np.array([t**3, t**2, t, 1])
                T = T*1/6
                a = np.matmul(T, B)
                p = np.matmul(a, R)

                Ttang  = np.array([t**2, t, 1])
                Ttang = Ttang*1/2
                a = np.matmul(Ttang, Btang)
                ptang = np.matmul(a, R)

                os, kut = Rotation(ptang)

                glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                
                glPushMatrix()
                Spline()
                glPopMatrix()
                
                glMatrixMode(GL_MODELVIEW)
                glPushMatrix()
                glTranslatef(p[0], p[1], p[2])
                glRotatef(kut, os[0], os[1], os[2])
                glScalef(1.8, 1.8, 1.8)
                Draw()
                glPopMatrix()
                pygame.display.flip()
                pygame.time.wait(50)

        glPopMatrix()
        #pygame.display.flip()
        #pygame.time.wait(10)

