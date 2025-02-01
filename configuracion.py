import pygame  

volumen_musica = 0.5

def establecer_volumen(valor):
    global volumen_musica
    volumen_musica = valor
    pygame.mixer.music.set_volume(volumen_musica)  

def obtener_volumen():
    return volumen_musica
