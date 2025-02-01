import pygame
import sys
import math
import random
import configuracion

pygame.init()

ANCHO, ALTO = 800, 600
NEGRO, BLANCO = (0, 0, 0), (255, 255, 255)
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Marin, Huye del Enemigo")

fondo = pygame.image.load("imagenes/fondo_partida.png")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
jugador_img = pygame.image.load("imagenes/marin.png")
enemigo_imgs = [pygame.image.load(f"imagenes/enemigo_{i}.png") for i in range(1, 4)]
powerup_img = pygame.transform.scale(pygame.image.load("imagenes/powerup.png"), (50, 50))

pygame.mixer.init()
try:
    pygame.mixer.music.load("sonidos/partida.mp3")
    pygame.mixer.music.set_volume(configuracion.obtener_volumen())
except pygame.error as e:
    print(f"Error al cargar la música: {e}")

class Jugador:
    def __init__(self):
        self.image = pygame.transform.scale(jugador_img, (70, 70))
        self.rect = self.image.get_rect(topleft=(100, 100))
        self.velocidad = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.rect.x -= self.velocidad
        if keys[pygame.K_RIGHT]: self.rect.x += self.velocidad
        if keys[pygame.K_UP]: self.rect.y -= self.velocidad
        if keys[pygame.K_DOWN]: self.rect.y += self.velocidad
        self.rect.x = max(0, min(self.rect.x, ANCHO - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, ALTO - self.rect.height))

class Enemigo:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(random.choice(enemigo_imgs), (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidad = 2

    def mover_hacia_jugador(self, jugador):
        dx, dy = jugador.rect.centerx - self.rect.centerx, jugador.rect.centery - self.rect.centery
        distancia = math.sqrt(dx ** 2 + dy ** 2)
        if distancia != 0:
            dx, dy = dx / distancia, dy / distancia
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

def partida(pantalla, ANCHO, ALTO):
    pygame.mixer.music.stop()
    pygame.mixer.music.load("sonidos/partida.mp3")
    pygame.mixer.music.set_volume(configuracion.obtener_volumen())
    pygame.mixer.music.play(-1)

    jugador = Jugador()
    enemigos, powerups = [Enemigo(500, 300)], []
    tiempo_inicio, tiempo_limite = pygame.time.get_ticks(), 60000
    reloj, game_over, nivel = pygame.time.Clock(), False, 1
    fuente = pygame.font.Font(None, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or (game_over and event.key == pygame.K_RETURN):
                    pygame.mixer.music.stop()
                    return

        tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio
        if tiempo_transcurrido >= tiempo_limite:
            nivel += 1
            tiempo_inicio = pygame.time.get_ticks()

        if not game_over:
            if tiempo_transcurrido // 10000 > len(enemigos) - 1:
                enemigos.append(Enemigo(random.randint(0, ANCHO - 50), random.randint(0, ALTO - 50)))
            if tiempo_transcurrido // 20000 > len(powerups):
                powerups.append(PowerUp(random.randint(50, ANCHO - 50), random.randint(50, ALTO - 50)))

            for powerup in powerups[:]:
                if powerup.colision_con_jugador(jugador):
                    jugador.velocidad += 2
                    powerups.remove(powerup)
                    if enemigos: enemigos.pop(random.randint(0, len(enemigos) - 1))

            jugador.update()
            for enemigo in enemigos:
                enemigo.mover_hacia_jugador(jugador)
                if enemigo.colision_con_jugador(jugador): game_over = True

        pantalla.blit(fondo, (0, 0))
        pantalla.blit(jugador.image, jugador.rect.topleft)
        for enemigo in enemigos: pantalla.blit(enemigo.image, enemigo.rect.topleft)
        for powerup in powerups: pantalla.blit(powerup.image, powerup.rect.topleft)


        pantalla.blit(fuente.render(f"Nivel: {nivel}", True, BLANCO), (10, 10))
        pantalla.blit(fuente.render(f"Tiempo restante: {(tiempo_limite - tiempo_transcurrido) // 1000}s", True, BLANCO), (ANCHO // 2 - 130, 40))
        pantalla.blit(fuente.render("¡Nuevo enemigo cada 10s!", True, BLANCO), (10, 60))
        pantalla.blit(fuente.render("¡Coje Las Estrellas!!! Elimina enemigos y corre más rápido!", True, BLANCO), (10, 90))

        if game_over:
            pantalla.blit(fuente.render("¡Game Over! Presiona ENTER para reiniciar o ESC para salir", True, BLANCO), (ANCHO // 2 - 220, ALTO // 2))

        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    partida(pantalla, ANCHO, ALTO)
