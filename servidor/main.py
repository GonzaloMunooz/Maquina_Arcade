# servidor/main.py
from comunicaciones import ServidorRed
from modelos import init_db, ResultadoNReinas, ResultadoCaballo, ResultadoHanoi

def main():
    init_db()  # Crea tablas si no existen
    server = ServidorRed(host='0.0.0.0', port=5000)
    server.start()

if __name__ == '__main__':
    main()