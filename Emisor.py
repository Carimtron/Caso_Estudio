# emisor.py (Ejecutar en la maquina virtual Ubuntu que es la emisor)
import socket        # Librería para establecer conexiones de red TCP/IP
import cripto_motor  # Importamos nuestra lógica de cifrado polimórfico de 64 bits
import secrets       # Generador de números aleatorios seguro para criptografía
import random        # Librería para seleccionar elementos aleatorios de una lista

# Configuración de red
IP_RECEPTOR = "192.168.1.114" # Dirección IP de la máquina virtual Xubuntu
PUERTO = 5000                 # Puerto de escucha del receptor

def iniciar_emisor():
    # Creamos el socket utilizando IPv4 (AF_INET) y protocolo TCP (SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Intentamos la conexión con el receptor
            s.connect((IP_RECEPTOR, PUERTO))
            print(f"[*] Conectado al receptor en {IP_RECEPTOR}")

            # --- Implementación de todos los tipos de intercambio ---
            # Definimos una lista con los diferentes tipos de mensajes requeridos
            tipos_mensajes = ["PROYECTO", "PROYECTO1", "PROYECTO2", "PROYECTO3"]
            
            # Seleccionamos un mensaje al azar de la lista anterior
            mensaje_texto = random.choice(tipos_mensajes) 
            
            # Convertimos el texto a formato de bytes (UTF-8) para el procesamiento
            mensaje_bytes = mensaje_texto.encode('utf-8')

            # --- Generación de llave y selección polimórfica ---
            # Generamos una llave única de 64 bits (8 bytes) para este envío específico
            llave = cripto_motor.generar_llave_64()
            
            # Elegimos al azar una de las 4 funciones polimórficas (0 a 3)
            id_func = secrets.randbelow(4) 
            
            # Aplicamos el cifrado polimórfico a través de nuestro motor
            criptograma = cripto_motor.cifrar_polimorfico(mensaje_bytes, llave, id_func)

            # Mostramos en consola los detalles del paquete antes de enviarlo
            print(f"[+] Mensaje Original Seleccionado: {mensaje_texto}")
            print(f"[+] Función Polimórfica utilizada: ID {id_func}")
            print(f"[+] Criptograma generado (hex): {criptograma.hex()}")

            # Estructuramos el paquete final: ID (1 byte) + Llave (8 bytes) + Criptograma (8 bytes)
            paquete = bytes([id_func]) + llave + criptograma
            
            # Enviamos el paquete completo de 17 bytes a través de la red
            s.sendall(paquete)
            print("[*] Paquete enviado con éxito.")

        except Exception as e:
            # Captura y muestra errores de conexión o ejecución
            print(f"[!] Error: {e}")

if __name__ == "__main__":
    # Punto de entrada principal para ejecutar el script
    iniciar_emisor()
