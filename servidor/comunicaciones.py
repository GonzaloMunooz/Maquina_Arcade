import socket
import threading
import json
from modelos import guardar_resultado

class ServidorRed:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(5)

    def start(self):
        print(f"Servidor escuchando en {self.host}:{self.port}")
        while True:
            client, addr = self.sock.accept()
            threading.Thread(target=self.handle_client, args=(client, addr), daemon=True).start()

    def handle_client(self, client_sock, addr):
        try:
            data = client_sock.recv(4096)
            raw = data.decode().strip()
            print("DEBUG: recibido del cliente:", raw)
            # Intentamos parsear JSON
            mensaje = json.loads(raw)
        except json.JSONDecodeError as e:
            print("Error al decodificar JSON del cliente:", e)
            client_sock.send(b'{"status":"error","msg":"invalid JSON"}')
            client_sock.close()
            return
        except Exception as e:
            print("Error genérico recibiendo datos:", e)
            client_sock.close()
            return

        try:
            guardar_resultado(mensaje)
            # Enviamos siempre JSON con dobles comillas
            client_sock.send(b'{"status":"ok"}')
            print("DEBUG: enviada respuesta al cliente: {\"status\":\"ok\"}")
        except Exception as e:
            print("Error guardando en la base de datos:", e)
            client_sock.send(b'{"status":"error","msg":"save failed"}')
        finally:
            client_sock.close()
