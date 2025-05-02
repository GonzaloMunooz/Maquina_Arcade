import sys
import pygame
from hanoi.juego import TorreHanoi
from comunicacion.cliente import enviar_async  # Envío asíncrono de resultados

# Configuración gráfica
PEG_X = [150, 350, 550]
PEG_Y = 400
PEG_WIDTH = 10
DISK_HEIGHT = 20
FPS = 30


def main(discos=4):
    pygame.init()
    game = TorreHanoi(discos)
    screen = pygame.display.set_mode((700, 450))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    enviado = False
    seleccion = []

    running = True
    while running:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                x, _ = ev.pos
                # Detectar selección de poste
                for i, px in enumerate(PEG_X):
                    if abs(x - px) < 50:
                        seleccion.append(i)
                        if len(seleccion) == 2:
                            game.mover(seleccion[0], seleccion[1])
                            seleccion = []
                        break

        # Dibujo de fondo y postes
        screen.fill((30, 30, 30))
        for x in PEG_X:
            pygame.draw.rect(screen, (200, 200, 200),
                             (x - PEG_WIDTH // 2, 100,
                              PEG_WIDTH, PEG_Y - 100))

        # Dibujo de discos
        for idx, pila in enumerate(game.varillas):
            for level, disco in enumerate(pila):
                w = disco * 20
                h = DISK_HEIGHT
                x = PEG_X[idx] - w // 2
                y = PEG_Y - (level + 1) * h
                pygame.draw.rect(screen,
                                 (50 + disco * 30, 100, 150),
                                 (x, y, w, h))

        # Estado del puzzle
        completed = game.esta_completo(2)
        texto = "¡Resuelto!" if completed else "Click: origen→destino"
        label = font.render(texto, True, (255, 255, 255))
        screen.blit(label, (20, 20))

        # Envío asíncrono al servidor al completar
        if completed and not enviado:
            msg = {
                "juego": "hanoi",
                "discos": discos,
                "exito": True,
                "movimientos": len(game.movimientos)
            }
            enviar_async(msg)
            enviado = True

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
