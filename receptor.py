# receptor.py (Ejecutar en la maquina virtual Xubuntu que hace el trabajo de receptor)
import socket
import cripto_motor

# Configuración de red
IP_LOCAL = "0.0.0.0" # Escucha en todas las interfaces
PUERTO = 5000

def iniciar_receptor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP_LOCAL, PUERTO))
        s.listen()
        print(f"[*] Receptor esperando mensajes en el puerto {PUERTO}...")

        conn, addr = s.accept()
        with conn:
            print(f"[*] Conexión establecida desde: {addr}")
            
            # Recibimos el paquete completo (1 + 8 + 8 = 17 bytes)
            datos = conn.recv(1024)
            if datos:
                # Separamos los componentes del paquete
                id_func = datos[0]
                llave = datos[1:9]
                criptograma = datos[9:17]

                # --- Recuperando el mensaje original ---
                mensaje_recuperado = cripto_motor.descifrar_polimorfico(criptograma, llave, id_func)
                
                print(f"[+] ID de Función recibida: {id_func}")
                print(f"[+] Criptograma recibido: {criptograma.hex()}")
                print(f"[+] LLAVE recibida: {llave.hex()}")
                print(f"[!] MENSAJE RECUPERADO: {mensaje_recuperado.decode('utf-8')}")

if __name__ == "__main__":
    iniciar_receptor()
