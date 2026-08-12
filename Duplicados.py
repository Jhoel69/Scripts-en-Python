from pathlib import Path
import hashlib
from collections import defaultdict

# Cambia esta ruta por la carpeta que quieres analizar.
# Ejemplo:
# CARPETA = Path(r"C:\Users\jhoel.munoz\Downloads")

CARPETA = Path(r"C:\Users\jhoel.munoz\Downloads")

def calcular_hash(archivo, bloques=1024 * 1024):
    """
    Calcula una huella digital del contenido del archivo.
    Lee el archivo por bloques para no consumir demasiada memoria.
    """
    sha256 = hashlib.sha256()

    try:
        with archivo.open("rb") as datos:
            while bloque := datos.read(bloques):
                sha256.update(bloque)

        return sha256.hexdigest()

    except (PermissionError, OSError) as error:
        print(f"No se pudo leer: {archivo}")
        print(f"Motivo: {error}")
        return None


def buscar_duplicados(carpeta):
    if not carpeta.exists():
        print(f"La carpeta no existe: {carpeta}")
        return

    if not carpeta.is_dir():
        print(f"La ruta no es una carpeta: {carpeta}")
        return

    print(f"Analizando carpeta:\n{carpeta}\n")
    print("Buscando archivos...")

    archivos_por_tamano = defaultdict(list)

    # Busca archivos dentro de la carpeta y todas sus subcarpetas.
    for archivo in carpeta.rglob("*"):
        try:
            if archivo.is_file():
                tamano = archivo.stat().st_size
                archivos_por_tamano[tamano].append(archivo)
        except (PermissionError, OSError):
            print(f"No se pudo acceder a: {archivo}")

    # Solo pueden ser duplicados los archivos con el mismo tamaño.
    posibles_duplicados = [
        archivos
        for archivos in archivos_por_tamano.values()
        if len(archivos) > 1
    ]

    if not posibles_duplicados:
        print("No se encontraron posibles archivos duplicados.")
        return

    archivos_por_hash = defaultdict(list)

    print("Comparando el contenido de los archivos...\n")

    for grupo in posibles_duplicados:
        for archivo in grupo:
            huella = calcular_hash(archivo)

            if huella is not None:
                archivos_por_hash[huella].append(archivo)

    grupos_duplicados = [
        archivos
        for archivos in archivos_por_hash.values()
        if len(archivos) > 1
    ]

    if not grupos_duplicados:
        print("No se encontraron archivos duplicados.")
        return

    espacio_repetido = 0

    print("=" * 70)
    print("ARCHIVOS DUPLICADOS ENCONTRADOS")
    print("=" * 70)

    for numero, grupo in enumerate(grupos_duplicados, start=1):
        tamano = grupo[0].stat().st_size
        espacio_repetido += tamano * (len(grupo) - 1)

        print(f"\nGrupo {numero} - {len(grupo)} copias")
        print(f"Tamaño de cada archivo: {tamano:,} bytes")

        for archivo in grupo:
            print(f"  - {archivo}")

    print("\n" + "=" * 70)
    print(f"Grupos duplicados: {len(grupos_duplicados)}")
    print(f"Espacio repetido aproximado: {espacio_repetido:,} bytes")
    print("=" * 70)

    print("\nNo se eliminó ningún archivo.")


if __name__ == "__main__":
    buscar_duplicados(CARPETA)