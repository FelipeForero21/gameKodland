import pygame
import sys

def opciones(pantalla, ancho, alto):
    pygame.init()
    
    fuente = pygame.font.Font(None, 36)
    fuente_titulo = pygame.font.Font(None, 48)
    
    volumen_musica = 0.5
    
    pygame.mixer.music.set_volume(volumen_musica)
    
    opcion_seleccionada = 0
    opciones_texto = ["Volumen Música: ", "Volver"]
    
    fondo = pygame.image.load("imagenes/opciones_fondo.png")
    fondo = pygame.transform.scale(fondo, (ancho, alto))
    
    while True:
        pantalla.blit(fondo, (0, 0))
        
        titulo = fuente_titulo.render("Usa las flechas para ajustar el volumen", True, (255, 255, 255))
        pantalla.blit(titulo, (ancho // 2 - titulo.get_width() // 2, 50))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    opcion_seleccionada = (opcion_seleccionada + 1) % 2
                elif evento.key == pygame.K_UP:
                    opcion_seleccionada = (opcion_seleccionada - 1) % 2
                elif evento.key == pygame.K_LEFT:
                    if opcion_seleccionada == 0 and volumen_musica > 0.0:
                        volumen_musica -= 0.1
                        pygame.mixer.music.set_volume(volumen_musica)
                elif evento.key == pygame.K_RIGHT:
                    if opcion_seleccionada == 0 and volumen_musica < 1.0:
                        volumen_musica += 0.1
                        pygame.mixer.music.set_volume(volumen_musica)
                elif evento.key == pygame.K_RETURN:
                    if opcion_seleccionada == 1:
                        return  
                        
        for i, texto in enumerate(opciones_texto):
            color = (255, 255, 255) if i == opcion_seleccionada else (180, 180, 180)
            renderizado = fuente.render(f"{texto} {round(volumen_musica, 1) if i == 0 else ''}", True, color)
            pantalla.blit(renderizado, (ancho // 2 - 100, 150 + i * 50))
        
        pygame.display.flip()
