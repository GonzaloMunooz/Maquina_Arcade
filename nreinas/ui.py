import sys
import pygame
from nreinas.juego import TableroReinas
from comunicacion.cliente import enviar_async  # Envío asíncrono de resultados

# Configuración
CELL_SIZE = 60
MARGIN = 20
FPS = 30
QUEEN_COLOR = (200, 50, 50)

def main(n=8):
    pygame.init()
    board = TableroReinas(n)
    size = n * CELL_SIZE + 2 * MARGIN
    screen = pygame.display.set_mode((size, size))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    
    enviado = False  # Para enviar solo una vez

    running = True
    while running:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                x, y = ev.pos
                col = (x - MARGIN) // CELL_SIZE
                row = (y - MARGIN) // CELL_SIZE
                if 0 <= row < n and 0 <= col < n:
                    board.colocar_reina(row, col)

        # Dibujar tablero
        screen.fill((30, 30, 30))
        for r in range(n):
            for c in range(n):
                rect = pygame.Rect(
                    MARGIN + c*CELL_SIZE,
                    MARGIN + r*CELL_SIZE,
                    CELL_SIZE, CELL_SIZE
                )
                color = (240,240,240) if (r+c)%2 == 0 else (200,200,200)
                pygame.draw.rect(screen, color, rect)

        # Dibujar reinas
        for reina in board.reinas:
            cx = MARGIN + reina.col*CELL_SIZE + CELL_SIZE//2
            cy = MARGIN + reina.fila*CELL_SIZE + CELL_SIZE//2
            pygame.draw.circle(screen, QUEEN_COLOR, (cx, cy), CELL_SIZE//3)

        # Estado
        text = "¡Resuelto!" if board.esta_completo() else "Coloca reinas..."
        label = font.render(text, True, (255,255,255))
        screen.blit(label, (MARGIN, size - MARGIN - 30))

        # Envío asíncrono al servidor al completar
        if board.esta_completo() and not enviado:
            msg = {
                "juego": "nreinas",
                "n": n,
                "exito": True,
                "pasos": len(board.reinas)
            }
            enviar_async(msg)
            enviado = True

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
