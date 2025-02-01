import pygame
import opciones as mod_opciones
import partida as mod_partida
import configuracion

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("El último Marin en Pie - Felipe F.")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDEMILITAR = (85, 107, 47)

fuente = pygame.font.Font(None, 50)
fuente_titulo = pygame.font.Font(None, 74)

opciones = ["Juega", "Opciones"]
opcion_seleccionada = 0

pygame.mixer.music.load("sonidos/IntroMenuPrincipal.mp3") 
pygame.mixer.music.set_volume(configuracion.obtener_volumen())  
pygame.mixer.music.play(-1) 

sonido_seleccion = pygame.mixer.Sound("sonidos/clickSeleccion.mp3")
sonido_seleccion.set_volume(0.3)

fondo = pygame.transform.scale(pygame.image.load("imagenes/marin_fondo.png"), (ANCHO, ALTO))

def dibujar_menu():
    pantalla.blit(fondo, (0, 0)) 
    pantalla.blit(fuente_titulo.render("El último Marin en Pie", True, NEGRO), (ANCHO // 2 - 220, 50))
    for i, opcion in enumerate(opciones):
        color = VERDEMILITAR if i == opcion_seleccionada else BLANCO
        pantalla.blit(fuente.render(opcion, True, color), (ANCHO // 3, 200 + i * 60))
    pygame.display.flip()

def manejar_eventos():
    global opcion_seleccionada
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
                sonido_seleccion.play() 
            elif evento.key == pygame.K_DOWN:
                opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
                sonido_seleccion.play()  
            elif evento.key == pygame.K_RETURN:
                if opciones[opcion_seleccionada] == "Juega":
                    pygame.mixer.music.stop()  
                    mod_partida.partida(pantalla, ANCHO, ALTO)
                    pygame.mixer.music.play(-1) 
                elif opciones[opcion_seleccionada] == "Opciones":
                    mod_opciones.opciones(pantalla, ANCHO, ALTO) 
                    
    return True

while manejar_eventos():
    dibujar_menu()

pygame.mixer.music.stop()
pygame.quit()
