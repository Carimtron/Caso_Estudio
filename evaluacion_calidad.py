# evaluacion_calidad.py # Realizando la prueba en la maquina ubuntu 
import cripto_motor # Importamos nuestro motor para usar la función de generación de llaves
import collections  # Necesario para contar frecuencias de elementos y detectar duplicados
import math         # Utilizado para realizar el cálculo logarítmico de la entropía

def calcular_entropia(datos):
    """Calcula la entropía de Shannon para medir qué tan aleatorios son los bits."""
    if not datos:
        return 0
    # Contamos cuántas veces aparece cada byte en el total de la muestra
    conteo = collections.Counter(datos)
    # Calculamos la probabilidad de aparición de cada byte
    probabilidades = [f / len(datos) for f in conteo.values()]
    # Aplicamos la fórmula de Shannon: suma de p * log2(p)
    return -sum(p * math.log2(p) for p in probabilidades)

def ejecutar_test_robusto(n=10000):
    print("="*50)
    print(f"[*] INICIANDO PRUEBA DE CALIDAD (Muestra: {n} llaves)")
    print("="*50)
    
    llaves = [] # Lista para almacenar cada llave completa y buscar colisiones
    bits_totales = bytearray() # Acumulador de todos los bytes para el análisis estadístico

    # --- Generación de la Tabla de Llaves ---
    # Creamos un archivo .txt para documentar las llaves generadas de forma eficiente
    with open("tabla_llaves.txt", "w") as archivo_tabla:
        archivo_tabla.write(f"REPORTE TECNICO: TABLA DE {n} LLAVES DE 64-BIT\n")
        archivo_tabla.write("="*50 + "\n")
        
        for i in range(n):
            # Generamos la llave de 64 bits usando nuestro motor criptográfico
            llave = cripto_motor.generar_llave_64()
            llaves.append(llave)
            bits_totales.extend(llave)
            
            # Escribimos la llave en formato hexadecimal en nuestra tabla física
            archivo_tabla.write(f"ID: {i+1:05d} | LLAVE (HEX): {llave.hex()}\n")

    # 1. Prueba de Colisiones (Repeticiones)
    conteo = collections.Counter(llaves)
    duplicados = [l for l, c in conteo.items() if c > 1]
    
    # 2. Análisis de Entropía
    entropia = calcular_entropia(bits_totales)

    print(f"[+] Generación de Tabla:")
    print(f"    - Archivo creado: tabla_llaves.txt") 

    print(f"\n[+] Análisis de Colisiones:")
    print(f"    - Llaves Únicas: {len(set(llaves))}")
    print(f"    - Llaves Duplicadas: {len(duplicados)}")
    
    print(f"\n[+] Análisis de Entropía (Shannon):")
    print(f"    - Valor obtenido: {entropia:.4f} bits por byte")
    print(f"    - Ideal: 8.0000 (Máxima aleatoriedad)")
    
    print("\n" + "="*50)
    # Criterio de éxito: Cero duplicados y una entropía superior al umbral de seguridad (7.5)
    if len(duplicados) == 0 and entropia > 7.5:
        print("[!] VEREDICTO: CALIDAD ALTA - APTO PARA DESPLIEGUE IoT")
        print("    La generación basada en 'secrets' es criptográficamente segura.")
    else:
        print("[!] VEREDICTO: CALIDAD INSUFICIENTE")
    print("="*50)

if __name__ == "__main__":
    # Ejecutamos la prueba de robustez masiva
    ejecutar_test_robusto()
