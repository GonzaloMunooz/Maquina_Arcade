Link:
https://github.com/GonzaloMunooz/Maquina_Arcade.git


Lo primero que debes de hacer para ejecutar la maquina sin problemas es ejecutar el servidor primero: python -m servidor.main
Desde otra terminal, en la misma carpeta raíz: python launcher.py
Seleccionas un juego y al terminarlo o abandonarlo, cada cliente envia un JSON al servidor
un ejemplo: {
  "juego": "nreinas",
  "n": 8,
  "exito": true,
  "pasos": 8
}
El servidor responde con: ok: o si hay algun error con {"status":"error","msg":"..."}
Por ultimo para ver resultados de todas las partidas registradas puedes ejecutar en terminal esto: python check_all_results.py
