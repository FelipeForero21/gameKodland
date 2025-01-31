import pygame

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("El último Marin en Pie")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (200, 0, 0)
AZUL = (0, 0, 200)

fuente = pygame.font.Font(None, 50)

opciones = ["Modo Campaña", "Modo Libre", "Opciones"]
opcion_seleccionada = 0

def dibujar_menu():
    pantalla.fill(NEGRO)
    for i, opcion in enumerate(opciones):
        color = ROJO if i == opcion_seleccionada else BLANCO
        texto = fuente.render(opcion, True, color)
        pantalla.blit(texto, (ANCHO // 3, 200 + i * 60))
    pygame.display.flip()

def transicion_campana():
    for alpha in range(0, 255, 15):
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(alpha)
        overlay.fill(NEGRO)
        pantalla.blit(overlay, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)
    print("Entrando al Modo Campaña...")

def transicion_libre():
    for x in range(0, ANCHO, 20):
        pantalla.fill(NEGRO)
        pygame.draw.rect(pantalla, ROJO, (x, 0, ANCHO, ALTO))
        pygame.display.flip()
        pygame.time.delay(20)
    print("Entrando al Modo Libre...")

def transicion_opciones():
    for i in range(0, 50):
        pantalla.fill((i * 5, i * 5, i * 5))
        pygame.display.flip()
        pygame.time.delay(20)
    print("Entrando a Opciones...")

def manejar_eventos():
    global opcion_seleccionada
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
            elif evento.key == pygame.K_DOWN:
                opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
            elif evento.key == pygame.K_RETURN:
                if opcion_seleccionada == 0:
                    transicion_campana()
                elif opcion_seleccionada == 1:
                    transicion_libre()
                elif opcion_seleccionada == 2:
                    transicion_opciones()
    return True

ejecutando = True
while ejecutando:
    ejecutando = manejar_eventos()
    dibujar_menu()
    
pygame.quit()