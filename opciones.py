import pygame
import sys
import configuracion

def opciones(pantalla, ancho, alto):
    pygame.init()
    
    fuente = pygame.font.Font(None, 36)
    fuente_titulo = pygame.font.Font(None, 48)
    
    volumen_musica = configuracion.obtener_volumen()  
    pygame.mixer.music.set_volume(volumen_musica)
    
    opciones_texto = ["Volumen Música: ", "Volver"]
    opcion_seleccionada = 0
    
    fondo = pygame.transform.scale(pygame.image.load("imagenes/opciones_fondo.png"), (ancho, alto))
    
    while True:
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(fuente_titulo.render("Usa las flechas para ajustar el volumen", True, (255, 255, 255)), (ancho // 2 - 250, 50))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    opcion_seleccionada = (opcion_seleccionada + 1) % 2
                elif evento.key == pygame.K_UP:
                    opcion_seleccionada = (opcion_seleccionada - 1) % 2
                elif evento.key == pygame.K_LEFT and opcion_seleccionada == 0 and volumen_musica > 0:
                    volumen_musica -= 0.1
                    configuracion.establecer_volumen(volumen_musica)
                elif evento.key == pygame.K_RIGHT and opcion_seleccionada == 0 and volumen_musica < 1:
                    volumen_musica += 0.1
                    configuracion.establecer_volumen(volumen_musica)
                elif evento.key == pygame.K_RETURN and opcion_seleccionada == 1:
                    return
                
        for i, texto in enumerate(opciones_texto):
            color = (255, 255, 255) if i == opcion_seleccionada else (180, 180, 180)
            renderizado = fuente.render(f"{texto} {round(volumen_musica, 1) if i == 0 else ''}", True, color)
            pantalla.blit(renderizado, (ancho // 2 - 100, 150 + i * 50))
        
        pygame.display.flip()
