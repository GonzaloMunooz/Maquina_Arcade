import socket
import json
import threading

class ClienteRed:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port

    def enviar(self, mensaje):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        data = json.dumps(mensaje).encode()
        sock.send(data)
        respuesta = sock.recv(4096)
        sock.close()
        return json.loads(respuesta.decode())

def enviar_async(mensaje, host='127.0.0.1', port=5000):
    """
    Envía el mensaje al servidor en un hilo daemon para no bloquear la UI.
    """
    def _work():
        cliente = ClienteRed(host, port)
        try:
            resp = cliente.enviar(mensaje)
            print("Servidor:", resp.get("status"))
        except Exception as e:
            print("Error al enviar:", e)
    threading.Thread(target=_work, daemon=True).start()
