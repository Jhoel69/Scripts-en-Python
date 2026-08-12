from pathlib import Path


# Cambia esta ruta por la carpeta que quieres utilizar.
# Ejemplo:
# CARPETA = Path(r"C:\Users\tu_usuario\Downloads")

CARPETA = Path.home() / "Downloads" #aqui inserta la ruta de la carpeta recuerda colocar r al inicio

# Prefijo que tendrán los archivos.
PREFIJO = "archivo"

# Comenzar la numeración desde este número.
NUMERO_INICIAL = 1


def obtener_nombre_disponible(prefijo, numero, extension):
    """
    Crea un nombre con formato:
    prefijo_001.extension
    """
    return f"{prefijo}_{numero:03d}{extension}"


def renombrar_archivos():
    if not CARPETA.exists():
        print(f"La carpeta no existe: {CARPETA}")
        return

    if not CARPETA.is_dir():
        print(f"La ruta no es una carpeta: {CARPETA}")
        return

    archivos = sorted(
        [
            elemento for elemento in CARPETA.iterdir()
            if elemento.is_file()
        ],
        key=lambda archivo: archivo.name.lower()
    )

    if not archivos:
        print("No se encontraron archivos en la carpeta.")
        return

    cambios = []
    numero = NUMERO_INICIAL

    for archivo in archivos:
        nuevo_nombre = obtener_nombre_disponible(
            PREFIJO,
            numero,
            archivo.suffix
        )

        nuevo_archivo = CARPETA / nuevo_nombre

        cambios.append((archivo, nuevo_archivo))
        numero += 1

    # Evitar sobrescribir archivos existentes.
    destinos = {destino for _, destino in cambios}

    for _, destino in cambios:
        if destino.exists() and destino not in {
            origen for origen, _ in cambios
        }:
            print(f"El archivo ya existe: {destino.name}")
            print("No se realizó ningún cambio.")
            return

    print("\nVISTA PREVIA DE LOS CAMBIOS")
    print("=" * 60)

    for origen, destino in cambios:
        print(f"{origen.name}  ->  {destino.name}")

    print("=" * 60)
    respuesta = input(
        "\n¿Quieres aplicar estos cambios? Escribe SI para continuar: "
    )

    if respuesta.strip().upper() != "SI":
        print("Operación cancelada. No se cambió ningún archivo.")
        return

    renombrados = 0

    for origen, destino in cambios:
        try:
            origen.rename(destino)
            renombrados += 1
        except OSError as error:
            print(f"No se pudo renombrar {origen.name}: {error}")

    print(f"\nProceso terminado. Archivos renombrados: {renombrados}")


if __name__ == "__main__":
    renombrar_archivos()