import numpy as np
import math
import random

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

def Draw():
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_TRIANGLES)
    #glColor3fv((0,0.2,0.5))
    for surface in surfaces:
        for index in surface:
            glTexCoord2fv(texcoords[index-1])
            glVertex3fv(vertices[index-1])
            
    glEnd()

def Rotation(e):
    s = np.array([0.0, 0.0, -1.0])
    os =np.array([s[1]*e[2] - e[1]*s[2], -s[0]*e[2] + e[0]*s[2], s[0]*e[1] - s[1]*e[0]])

    skalarni = np.dot(s, e)
    nazivnik = np.linalg.norm(s) * np.linalg.norm(e)
    kosinus = skalarni/nazivnik
    rad = np.arccos(kosinus)
    kut = np.degrees(rad)

    return os, kut

class Cestica:
    def __init__(self, texture, trajanje, brzina, velicina, x_pocetni, ociste):
        self.trajanje = trajanje
        self.brzina = brzina
        self.texture = texture
        self.s = velicina
        self.x = x_pocetni
        self.ociste = ociste
        self.pocetak = pygame.time.get_ticks()
        self.iteracija = 0
        self.kut = random.uniform(0, 359)

    def draw(self):
        if pygame.time.get_ticks() - self.pocetak < self.trajanje:
            x_transl = math.sin(math.radians(self.kut)) + self.x
            os, kut = Rotation(self.ociste)
            
            glPushMatrix()
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texture)

            glTranslatef(x_transl , 3.0 - self.iteracija * self.brzina , 0.0)
            #glRotatef(self.kut, 0, 0, 1)
            glRotatef(kut, os[0], os[1], os[2])
            glScalef(self.s, self.s, self.s)
            
            Draw()
        
            glPopMatrix()

            self.iteracija+=1
            self.kut+=2.0

            if self.kut > 360.0:
                self.kut = 0.0

            if self.s > 0.2:
                self.s = self.s - 0.002

            return True

        else:
            return False #isteklo je vrijeme, cestica je mrtva



def instanciraj():
    trajanje = random.uniform(2000, 6000)
    brzina = random.uniform(0.01, 0.07)
    velicina = random.uniform(0.4, 0.7)
    x = random.uniform(-4.0, 6.0)

    return trajanje, brzina, velicina, x
    
        

#vertices, surfaces = ucitaj("kvadrat.txt", False)
vertices = [(-0.5, -0.5, 0.0),
            (0.5, -0.5, 0.0),
            (-0.5, 0.5, 0.0),
            (0.5, 0.5, 0.0)]
texcoords = [(0.0, 0.0),
            (1.0, 0.0),
            (0.0, 1.0),
            (1.0, 1.0)]
surfaces = [(1, 2, 3),
           (2, 4, 3)]

if __name__=="__main__":
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    clock = pygame.time.Clock()

    glMatrixMode(GL_PROJECTION);
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    
    ociste = np.array([0.0, 0.0, -8.0])
    gluLookAt(ociste[0], ociste[1], ociste[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    image = pygame.image.load("snow.bmp").convert()
    image_width,image_height = image.get_rect().size
    img_data = pygame.image.tostring(image,'RGB')
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,image_width,image_height,0,GL_RGB,GL_UNSIGNED_BYTE,img_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    krug = pygame.time.get_ticks()
    cestice = []
    mrtve = []
    for i in range(20):
        trajanje, brzina, velicina, x_pocetni = instanciraj()
        cestice.append(Cestica(texture, trajanje, brzina, velicina, x_pocetni, ociste))
    broj_cestica = 20
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ociste[0] = ociste[0] - 1.0
                if event.key == pygame.K_RIGHT:
                    ociste[0] = ociste[0] + 1.0

                if event.key == pygame.K_DOWN:
                    ociste[1] = ociste[1] - 1.0
                if event.key == pygame.K_UP:
                    ociste[1] = ociste[1] + 1.0

            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            gluLookAt(ociste[0], ociste[1], ociste[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
                    
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        
        if broj_cestica < 40 and pygame.time.get_ticks() - krug > 500:
            broj_cestica += 5
            for i in range(5):
                trajanje, brzina, velicina, x_pocetni = instanciraj()
                cestice.append(Cestica(texture, trajanje, brzina, velicina, x_pocetni, ociste))
            krug = pygame.time.get_ticks()
        

        for i in range(len(cestice)):
            if cestice[i].draw() == False:
                mrtve.append(i)

        if len(mrtve) > 0:
            del cestice[mrtve[len(mrtve)-1]]
            mrtve.pop()
            broj_cestica -= 1


        pygame.display.flip()
        clock.tick(30)

        
