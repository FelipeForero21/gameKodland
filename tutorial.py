import pygame
import sys
import math
import random

pygame.init()

ANCHO = 800
ALTO = 600

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Marin, Huye del Enemigo")

# Cargar imágenes
fondo = pygame.image.load("imagenes/fondo_tutorial.png")
jugador_img = pygame.image.load("imagenes/marin.png")
enemigo_imgs = [pygame.image.load(f"imagenes/enemigo_{i}.png") for i in range(1, 4)]
powerup_img = pygame.transform.scale(pygame.image.load("imagenes/powerup.png"), (50, 50))

pygame.mixer.music.load("sonidos/tutorial.mp3")
pygame.mixer.music.set_volume(0.5)
class Jugador:
    def __init__(self):
        self.image = pygame.transform.scale(jugador_img, (50, 50))
        self.rect = self.image.get_rect(topleft=(100, 100))
        self.velocidad = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidad

        self.rect.x = max(0, min(self.rect.x, ANCHO - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, ALTO - self.rect.height))

class Enemigo:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(random.choice(enemigo_imgs), (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidad = 2

    def mover_hacia_jugador(self, jugador):
        dx = jugador.rect.centerx - self.rect.centerx
        dy = jugador.rect.centery - self.rect.centery
        distancia = math.sqrt(dx ** 2 + dy ** 2)

        if distancia != 0:
            dx /= distancia
            dy /= distancia

        self.rect.x += dx * self.velocidad
        self.rect.y += dy * self.velocidad

    def colision_con_jugador(self, jugador):
        return self.rect.colliderect(jugador.rect)

class PowerUp:
    def __init__(self, x, y):
        self.image = powerup_img
        self.rect = self.image.get_rect(topleft=(x, y))

    def colision_con_jugador(self, jugador):
        return self.rect.colliderect(jugador.rect)

def tutorial(pantalla, ANCHO, ALTO):
    pygame.mixer.music.stop()  
    pygame.mixer.music.load("sonidos/tutorial.mp3")  
    pygame.mixer.music.play(-1)  

    jugador = Jugador()
    enemigos = [Enemigo(500, 300)]
    powerups = []
    tiempo_inicio = pygame.time.get_ticks()
    tiempo_limite = 60000
    reloj = pygame.time.Clock()
    game_over = False
    
    fuente = pygame.font.Font(None, 30)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return  
                if game_over and event.key == pygame.K_RETURN:
                    return 

        tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio
        tiempo_restante = (tiempo_limite - tiempo_transcurrido) // 1000
        if tiempo_transcurrido >= tiempo_limite:
            print("¡Has completado el tutorial!")
            break

        if not game_over:
            if tiempo_transcurrido // 10000 > len(enemigos) - 1:
                enemigos.append(Enemigo(random.randint(0, ANCHO - 50), random.randint(0, ALTO - 50)))
            if tiempo_transcurrido // 20000 > len(powerups):
                powerups.append(PowerUp(random.randint(50, ANCHO - 50), random.randint(50, ALTO - 50)))

            for powerup in powerups[:]:
                if powerup.colision_con_jugador(jugador):
                    jugador.velocidad += 2
                    powerups.remove(powerup)
                    if enemigos:
                        enemigos.pop(random.randint(0, len(enemigos) - 1))

            jugador.update()
            for enemigo in enemigos:
                enemigo.mover_hacia_jugador(jugador)
                if enemigo.colision_con_jugador(jugador):
                    game_over = True

        pantalla.blit(fondo, (0, 0))
        pantalla.blit(jugador.image, jugador.rect.topleft)
        for enemigo in enemigos:
            pantalla.blit(enemigo.image, enemigo.rect.topleft)
        for powerup in powerups:
            pantalla.blit(powerup.image, powerup.rect.topleft)
        
        instrucciones1 = fuente.render("Usa las flechas para moverte y evita a los enemigos.", True, BLANCO)
        instrucciones2 = fuente.render("Cada 10s aparece uno nuevo.", True, BLANCO)
        instrucciones3 = fuente.render("Recoge poderes para aumentar velocidad y eliminar enemigos. (20sg)", True, BLANCO)
        
        pantalla.blit(instrucciones1, ((ANCHO - instrucciones1.get_width()) // 2, 10))
        pantalla.blit(instrucciones2, ((ANCHO - instrucciones2.get_width()) // 2, 40))
        pantalla.blit(instrucciones3, ((ANCHO - instrucciones3.get_width()) // 2, 70))
        
        tiempo_texto = fuente.render(f"Tiempo restante: {tiempo_restante}s", True, BLANCO)
        pantalla.blit(tiempo_texto, (ANCHO // 2 - tiempo_texto.get_width() // 2, 100))
        
        if game_over:
            mensaje = fuente.render("¡Game Over! Presiona ENTER para reiniciar o ESC para salir", True, BLANCO)
            pantalla.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO // 2))
        
        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    tutorial(pantalla, ANCHO, ALTO)
