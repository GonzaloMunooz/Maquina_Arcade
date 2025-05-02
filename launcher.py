import sys
import os
import subprocess

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print('Máquina Arcade')
    print('1) N-Reinas')
    print("2) Knight's Tour")
    print('3) Torres de Hanoi')
    choice = input('Selecciona un juego: ')

    rutas = {
        '1': 'nreinas.ui',
        '2': 'caballo.ui',
        '3': 'hanoi.ui',
    }

    if choice in rutas:
        module = rutas[choice]
        # Ejecuta el módulo como paquete para resolver imports correctamente
        subprocess.run(
            [sys.executable, '-m', module],
            cwd=base_dir
        )
    else:
        print('Opción no válida.')

if __name__ == '__main__':
    main()
