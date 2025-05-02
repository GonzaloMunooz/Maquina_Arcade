import sys
import threading
import pygame
# Aumentar límite de recursión para el backtracking
sys.setrecursionlimit(10000)

from caballo.juego import CaballoTour
from comunicacion.cliente import enviar_async  # Envío asíncrono

# Configuración
CELL = 60
MARGIN = 20
FPS = 30
VISITED_COLOR = (50, 200, 50)
KNIGHT_COLOR = (50, 50, 200)
PATH_COLOR = (200, 200, 50)

def main(n=8, inicio=(0, 0)):
    pygame.init()
    tour = CaballoTour(n, inicio)
    size = n * CELL + 2 * MARGIN
    screen = pygame.display.set_mode((size, size))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    enviado = False       # Para enviar el resultado solo una vez
    solving = False       # Para saber si ya lanzamos el hilo

    def solve():
        nonlocal solving
        try:
            tour.buscar_tour()
        except Exception as e:
            print("Error interno en buscar_tour():", repr(e))
        finally:
            solving = False

    running = True
    while running:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

            # Al pulsar ESPACIO lanzamos la resolución en hilo si aún no lo hemos hecho
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE and not solving:
                solving = True
                threading.Thread(target=solve, daemon=True).start()

            # Click paso a paso manual
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and not solving:
                x, y = ev.pos
                c = (x - MARGIN) // CELL
                r = (y - MARGIN) // CELL
                origen = tour.movimientos[-1] if tour.movimientos else inicio
                if (r, c) in tour.movimientos_legales(origen):
                    tour.movimientos.append((r, c))
                    tour.visitadas.add((r, c))

        # Dibujo del tablero
        screen.fill((30, 30, 30))
        for i in range(n + 1):
            pygame.draw.line(screen, (200, 200, 200),
                             (MARGIN, MARGIN + i * CELL),
                             (MARGIN + n * CELL, MARGIN + i * CELL))
            pygame.draw.line(screen, (200, 200, 200),
                             (MARGIN + i * CELL, MARGIN),
                             (MARGIN + i * CELL, MARGIN + n * CELL))

        # Dibujo del camino
        for idx, pos in enumerate(tour.movimientos):
            r, c = pos
            rect = pygame.Rect(MARGIN + c * CELL,
                               MARGIN + r * CELL,
                               CELL, CELL)
            pygame.draw.rect(screen, VISITED_COLOR, rect)
            if idx > 0:
                pr, pc = tour.movimientos[idx - 1]
                start = (MARGIN + pc * CELL + CELL // 2,
                         MARGIN + pr * CELL + CELL // 2)
                end = (MARGIN + c * CELL + CELL // 2,
                       MARGIN + r * CELL + CELL // 2)
                pygame.draw.line(screen, PATH_COLOR, start, end, 3)

        # Dibujo del caballo
        if tour.movimientos:
            r, c = tour.movimientos[-1]
        else:
            r, c = inicio
        pygame.draw.circle(screen, KNIGHT_COLOR,
                           (MARGIN + c * CELL + CELL // 2,
                            MARGIN + r * CELL + CELL // 2),
                           CELL // 3)

        # Texto de estado
        completed = len(tour.movimientos) == n * n
        if solving and not completed:
            status = "Resolviendo..."
        else:
            status = "¡Completado!" if completed else "Espacio: auto / Click: paso"

        label = font.render(status, True, (255, 255, 255))
        screen.blit(label, (MARGIN, size - MARGIN - 25))

        # Envío asíncrono al servidor al completar
        if completed and not enviado:
            msg = {
                "juego": "caballo",
                "inicio": list(inicio),
                "exito": True,
                "movimientos": len(tour.movimientos)
            }
            enviar_async(msg)
            enviado = True

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
