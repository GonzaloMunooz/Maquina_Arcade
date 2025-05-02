import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Ruta al directorio de este archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Base de datos dentro de servidor/arcade.db
DB_PATH = os.path.join(BASE_DIR, 'arcade.db')

Base = declarative_base()

class ResultadoBase(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    juego = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class ResultadoNReinas(ResultadoBase):
    __tablename__ = 'nreinas'
    n = Column(Integer)
    exito = Column(Boolean)
    pasos = Column(Integer)

class ResultadoCaballo(ResultadoBase):
    __tablename__ = 'caballo'
    inicio = Column(String)
    exito = Column(Boolean)
    movimientos = Column(Integer)

class ResultadoHanoi(ResultadoBase):
    __tablename__ = 'hanoi'
    discos = Column(Integer)
    exito = Column(Boolean)
    movimientos = Column(Integer)

# Motor y sesión apuntando al archivo en servidor/arcade.db
engine = create_engine(f'sqlite:///{DB_PATH}')
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

def guardar_resultado(mensaje):
    session = Session()
    juego = mensaje.get('juego')
    if juego == 'nreinas':
        res = ResultadoNReinas(
            juego=juego,
            n=mensaje.get('n'),
            exito=mensaje.get('exito'),
            pasos=mensaje.get('pasos')
        )
    elif juego == 'caballo':
        res = ResultadoCaballo(
            juego=juego,
            inicio=str(mensaje.get('inicio')),
            exito=mensaje.get('exito'),
            movimientos=mensaje.get('movimientos')
        )
    elif juego == 'hanoi':
        res = ResultadoHanoi(
            juego=juego,
            discos=mensaje.get('discos'),
            exito=mensaje.get('exito'),
            movimientos=mensaje.get('movimientos')
        )
    else:
        session.close()
        return
    session.add(res)
    session.commit()
    session.close()
