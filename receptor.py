# receptor.py (Ejecutar en la maquina virtual Xubuntu que hace el trabajo de receptor)
import socket        # Librería para gestionar las conexiones de red
import cripto_motor  # Importamos nuestro motor para las funciones de descifrado

# Configuración de red
IP_LOCAL = "0.0.0.0" # Escucha en todas las interfaces de red disponibles en la MV
PUERTO = 5000         # Puerto configurado para recibir los paquetes del emisor

def iniciar_receptor():
    # Creamos el socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Vinculamos el socket a la IP y puerto especificados
        s.bind((IP_LOCAL, PUERTO))
        # El servidor se pone en modo escucha para detectar intentos de conexión
        s.listen()
        print(f"[*] Receptor esperando mensajes en el puerto {PUERTO}...")
        print("[*] Presiona Ctrl+C para detener el servidor.")

        # --- BUCLE INFINITO PARA MEJORAR COMPROBACIONES DE CONEXIÓN ---
        # Este bucle permite recibir múltiples mensajes (PROYECTO, PROYECTO1, etc.)
        # sin que el programa se cierre después del primer intercambio.
        while True:
            # Aceptamos una nueva conexión entrante
            conn, addr = s.accept()
            with conn:
                # Recibimos el paquete de datos (ID + Llave + Criptograma = 17 bytes)
                datos = conn.recv(1024)
                if datos:
                    # Segmentamos el paquete recibido según el protocolo de 64 bits
                    id_func = datos[0]       # Primer byte: ID de la función polimórfica
                    llave = datos[1:9]       # Siguientes 8 bytes: Llave de 64 bits
                    criptograma = datos[9:17] # Últimos 8 bytes: El mensaje cifrado

                    # --- PROCESO DE DESCIFRADO ---
                    # Usamos el motor para recuperar el texto original usando la polimorfia
                    mensaje_recuperado = cripto_motor.descifrar_polimorfico(criptograma, llave, id_func)
                    
                    # Imprimimos los resultados en la terminal para validación
                    print("\n" + "="*40)
                    print(f"[*] Conexión establecida desde: {addr}")
                    print(f"[+] ID de Función recibida: {id_func}")
                    print(f"[+] Criptograma recibido: {criptograma.hex()}")
                    print(f"[+] LLAVE recibida: {llave.hex()}")
                    # Decodificamos de bytes a texto para mostrar el mensaje recuperado
                    print(f"[!] MENSAJE RECUPERADO: {mensaje_recuperado.decode('utf-8')}")
                    print("="*40)
                    print("[*] Esperando siguiente mensaje...")

if __name__ == "__main__":
    # Iniciamos el servicio del receptor
    iniciar_receptor()
