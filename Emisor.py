# emisor.py (Ejecutar en en la maquina virtual Ubuntu que es la emisor)
import socket
import cripto_motor # Importamos nuestra lógica cripto_motor
import secrets

# Configuración de red
IP_RECEPTOR = "192.168.1.114" # Tu IP de Xubuntu
PUERTO = 5000

def iniciar_emisor():
    # Creamos el socket para comunicación de red
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((IP_RECEPTOR, PUERTO))
            print(f"[*] Conectado al receptor en {IP_RECEPTOR}")

            # --- Probando tipos de mensajes (Ejemplo: Proyecto) ---
            mensaje_texto = "PROYECTO" # Exactamente 8 caracteres = 64 bits
            mensaje_bytes = mensaje_texto.encode('utf-8')

            # --- Generación de llave y selección polimórfica ---
            llave = cripto_motor.generar_llave_64()
            id_func = secrets.randbelow(4) # Elige una función de la 0 a la 3 al azar
            
            # Ciframos usando el motor polimórfico
            criptograma = cripto_motor.cifrar_polimorfico(mensaje_bytes, llave, id_func)

            print(f"[+] Mensaje Original: {mensaje_texto}")
            print(f"[+] Función Polimórfica usada: ID {id_func}")
            print(f"[+] Criptograma enviado (hex): {criptograma.hex()}")

            # Enviamos el paquete completo: ID_FUNCION (1 byte) + LLAVE (8 bytes) + CRIPTOGRAMA (8 bytes)
            paquete = bytes([id_func]) + llave + criptograma
            s.sendall(paquete)
            print("[*] Paquete enviado con éxito.")

        except Exception as e:
            print(f"[!] Error: {e}")

if __name__ == "__main__":
    iniciar_emisor()
