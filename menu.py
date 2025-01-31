import pygame
import opciones as mod_opciones
import tutorial as mod_tutorial

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("El último Marin en Pie")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDEMILITAR = (85, 107, 47)

fuente = pygame.font.Font(None, 50)
fuente_titulo = pygame.font.Font(None, 74)

opciones = ["Tutorial", "Modo Campaña", "Opciones"] 
opcion_seleccionada = 0

pygame.mixer.music.load("sonidos/IntroMenuPrincipal.mp3") 
pygame.mixer.music.set_volume(1)  
pygame.mixer.music.play(-1) 

sonido_seleccion = pygame.mixer.Sound("sonidos/clickSeleccion.mp3")
sonido_seleccion.set_volume(0.3)

fondo = pygame.image.load("imagenes/marin_fondo.png")  
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO)) 

def dibujar_menu():
    titulo = fuente_titulo.render("El último Marin en Pie", True, NEGRO)
    pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 50))
    for i, opcion in enumerate(opciones):
        color = VERDEMILITAR if i == opcion_seleccionada else BLANCO
        texto = fuente.render(opcion, True, color)
        pantalla.blit(texto, (ANCHO // 3, 200 + i * 60))
    pygame.display.flip()

def transicion_tutorial():
    for i in range(0, 50):
        pantalla.fill((i * 5, i * 5, i * 5))
        pygame.display.flip()
        pygame.time.delay(20)
    print("Entrando al Tutorial...")
    mod_tutorial.tutorial(pantalla, ANCHO, ALTO) 


def transicion_opciones():
    for i in range(0, 50):
        pantalla.fill((i * 5, i * 5, i * 5))
        pygame.display.flip()
        pygame.time.delay(20)
    print("Entrando a Opciones...")
    mod_opciones.opciones(pantalla, ANCHO, ALTO) 

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
                if opciones[opcion_seleccionada] == "Tutorial":
                    transicion_tutorial()
                elif opciones[opcion_seleccionada] == "Opciones":
                    transicion_opciones()
                    
    return True

ejecutando = True
while ejecutando:
    ejecutando = manejar_eventos()
    pantalla.blit(fondo, (0, 0)) 
    dibujar_menu()
    
pygame.mixer.music.stop()
pygame.quit()
