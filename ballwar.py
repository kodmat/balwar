import pygame
import random
import time
import numpy as np
from tensorflow.python.keras.models import load_model

model = load_model("ballwar.h5")


pygame.init()


ekran_genisligi = 600
ekran_yuksekligi = 900
daire_r = 40
dikdorgenin_genisligi = 200
dikdorgenin_yuksekligi = 80
colors = [(100,90,160),(0,0,0),(255,0,0),(60,60,100)]
fps = pygame.time.Clock()
data = []
sonuc = []

ekran = pygame.display.set_mode((ekran_genisligi,ekran_yuksekligi))


class dikdortgen:

    def __init__(self):
        self.gen = dikdorgenin_genisligi
        self.yuk = dikdorgenin_yuksekligi
        self.x = ekran_genisligi // 2
        self.y = ekran_yuksekligi - self.yuk


    def ciz_dikdortgen(self):
        pygame.draw.rect(ekran,colors[1],[self.x,self.y,self.gen,self.yuk])


class daire:

    def __init__(self):
        self.r = daire_r
        self.x = random.randint(self.r, ekran_genisligi - self.r)
        self.y = 0

    def ciz_daire(self):
        pygame.draw.circle(ekran, colors[1], [self.x, self.y],self.r)



def object_label(message, font, color):
    message_rt = font.render(message, True, colors[color])
    return message_rt, message_rt.get_rect()


def mesaj_kaybettin(message):
    font = pygame.font.Font("freesansbold.ttf", 48)
    message_label, message_obj = object_label(message, font, 2)
    message_obj.center = (ekran_genisligi // 2, ekran_yuksekligi / 2)
    ekran.blit(message_label, message_obj)
    pygame.display.update()
    time.sleep(1.0)


def mesaj_puan(message):
    font = pygame.font.Font("freesansbold.ttf", 36)
    message_label, message_obj = object_label("puan : " + str(message), font, 3)
    message_obj.center = (ekran_genisligi // 2, 20)
    ekran.blit(message_label, message_obj)
    pygame.display.update()





n_dikdortgen = dikdortgen()
n_daire = daire()
birim = 0
puan = 0
bitis = 0


while True:

    n_daire.y += 20

    if n_daire.y >= ekran_yuksekligi:
        n_daire.y = 0
        n_daire.x = random.randint(daire_r, ekran_genisligi - daire_r)
        puan += 10


    if bitis == 5:
        pygame.quit()
        break


    if model.predict(np.array([n_dikdortgen.x , n_daire.x, n_daire.y]).reshape(-1,3) / 600) < 0.5:
        birim = -15
    else:
        birim = 15


    if n_dikdortgen.x + birim < 0 or n_dikdortgen.x + birim + dikdorgenin_genisligi > ekran_genisligi:
        pass
    else:
        n_dikdortgen.x += birim


    if n_daire.y > ekran_yuksekligi - dikdorgenin_yuksekligi:

        if n_daire.x >= n_dikdortgen.x and n_daire.x <= n_dikdortgen.x + dikdorgenin_genisligi:
            mesaj_kaybettin("Kaybettiniz")
            n_daire.y = 0
            n_daire.x = random.randint(daire_r, ekran_genisligi - daire_r)
            puan = 0
            bitis += 1

    ekran.fill(colors[0])

    if birim != 0:
        data += [[n_dikdortgen.x , n_daire.x, n_daire.y]]
        sonuc += [birim]
    n_dikdortgen.ciz_dikdortgen()
    n_daire.ciz_daire()
    mesaj_puan(puan)
    pygame.display.update()

    fps.tick(48 + puan * 0.1)


kayit_giris = "kayit_giris"
kayit_cikis = "kayit_cikis"

try:
    np.save(kayit_giris, np.concatenate((np.load(kayit_giris), np.array(data).reshape(-1, 3))))
    np.save(kayit_cikis, np.concatenate((np.load(kayit_cikis), np.array(sonuc).reshape(-1, ))))
except:
    np.save(kayit_giris, np.array(data).reshape(-1, 3))
    np.save(kayit_cikis, np.array(sonuc).reshape(-1, ))