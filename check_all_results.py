# check_all_results.py
from servidor.modelos import Session, ResultadoNReinas, ResultadoCaballo, ResultadoHanoi

def main():
    session = Session()

    print("=== N-Reinas ===")
    for r in session.query(ResultadoNReinas).all():
        print(f"ID={r.id}, N={r.n}, Éxito={r.exito}, Pasos={r.pasos}, Fecha={r.timestamp}")

    print("\n=== Knight’s Tour ===")
    for r in session.query(ResultadoCaballo).all():
        print(f"ID={r.id}, Inicio={r.inicio}, Éxito={r.exito}, Movimientos={r.movimientos}, Fecha={r.timestamp}")

    print("\n=== Torres de Hanói ===")
    for r in session.query(ResultadoHanoi).all():
        print(f"ID={r.id}, Discos={r.discos}, Éxito={r.exito}, Movimientos={r.movimientos}, Fecha={r.timestamp}")

    session.close()

if __name__ == '__main__':
    main()
