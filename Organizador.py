from pathlib import Path
import shutil

# Cambia esta ruta por la carpeta que quieres organizar.
# Ejemplo en Windows:
# CARPETA = Path(r"C:\Users\TuNombre\Downloads")
#
# Ejemplo en macOS o Linux:
# CARPETA = Path("/home/tu_usuario/Descargas")

CARPETA = Path(r"C:\Users\jhoel.munoz\Downloads")


CATEGORIAS = {
    "Imagenes": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp",
        ".webp", ".svg", ".tiff"
    ],
    "Documentos": [
        ".doc", ".docx", ".txt", ".odt", ".rtf"
    ],
    "PDF": [
        ".pdf"
    ],
    "Hojas_de_calculo": [
        ".xls", ".xlsx", ".csv", ".ods"
    ],
    "Presentaciones": [
        ".ppt", ".pptx", ".odp"
    ],
    "Videos": [
        ".mp4", ".avi", ".mkv", ".mov", ".wmv"
    ],
    "Audio": [
        ".mp3", ".wav", ".flac", ".aac", ".ogg"
    ],
    "Comprimidos": [
        ".zip", ".rar", ".7z", ".tar", ".gz"
    ],
    "Programas": [
        ".exe", ".msi", ".apk", ".dmg", ".deb"
    ]
}


def obtener_categoria(extension):
    """Devuelve la categoría correspondiente a una extensión."""
    extension = extension.lower()

    for categoria, extensiones in CATEGORIAS.items():
        if extension in extensiones:
            return categoria

    return "Otros"


def obtener_nombre_disponible(destino):
    """
    Evita sobrescribir un archivo si ya existe otro con el mismo nombre.
    Ejemplo:
    informe.pdf
    informe_1.pdf
    informe_2.pdf
    """
    if not destino.exists():
        return destino

    contador = 1

    while True:
        nuevo_nombre = (
            f"{destino.stem}_{contador}{destino.suffix}"
        )
        nuevo_destino = destino.parent / nuevo_nombre

        if not nuevo_destino.exists():
            return nuevo_destino

        contador += 1


def organizar_carpeta():
    if not CARPETA.exists():
        print(f"La carpeta no existe: {CARPETA}")
        return

    archivos = [
        elemento for elemento in CARPETA.iterdir()
        if elemento.is_file()
    ]

    if not archivos:
        print("No se encontraron archivos para organizar.")
        return

    movidos = 0

    for archivo in archivos:
        categoria = obtener_categoria(archivo.suffix)
        carpeta_destino = CARPETA / categoria

        carpeta_destino.mkdir(exist_ok=True)

        destino = carpeta_destino / archivo.name
        destino = obtener_nombre_disponible(destino)

        shutil.move(str(archivo), str(destino))

        print(f"Movido: {archivo.name} -> {categoria}/{destino.name}")
        movidos += 1

    print()
    print(f"Proceso terminado. Archivos movidos: {movidos}")


if __name__ == "__main__":
    organizar_carpeta()