# check_db.py
from servidor.modelos import Session, ResultadoNReinas

def main():
    session = Session()
    resultados = session.query(ResultadoNReinas).all()
    if not resultados:
        print("→ No hay registros en la tabla nreinas.")
    else:
        for r in resultados:
            print(f"ID={r.id}, N={r.n}, Éxito={r.exito}, Pasos={r.pasos}, Fecha={r.timestamp}")
    session.close()

if __name__ == '__main__':
    main()
