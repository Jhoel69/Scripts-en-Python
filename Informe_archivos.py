from pathlib import Path
from collections import Counter
from datetime import datetime
import csv


# Cambia esta ruta por la carpeta que deseas analizar.
# Ejemplos:
#
# CARPETA = Path(r"C:\Users\jhoel.munoz\Documents")
# CARPETA = Path(r"C:\Users\jhoel.munoz\Downloads")
# CARPETA = Path(r"C:\Users\jhoel.munoz\Desktop")

CARPETA = Path(r"C:\Users\jhoel.munoz\Downloads")

ARCHIVO_CSV = Path("informe_archivos.csv")
ARCHIVO_RESUMEN = Path("resumen_archivos.txt")


def convertir_tamano(bytes_archivo):
    """Convierte bytes a una unidad más fácil de leer."""
    unidades = ["B", "KB", "MB", "GB", "TB"]
    tamano = float(bytes_archivo)

    for unidad in unidades:
        if tamano < 1024:
            return f"{tamano:.2f} {unidad}"

        tamano /= 1024

    return f"{tamano:.2f} PB"


def obtener_extension(archivo):
    """Obtiene la extensión del archivo o indica que no tiene."""
    extension = archivo.suffix.lower()

    if extension:
        return extension
    else:
        return "[sin extension]"


def generar_informe():
    if not CARPETA.exists():
        print(f"La carpeta no existe: {CARPETA}")
        return

    if not CARPETA.is_dir():
        print(f"La ruta no es una carpeta: {CARPETA}")
        return

    print(f"Analizando carpeta:\n{CARPETA}\n")
    print("El proceso puede tardar dependiendo de la cantidad de archivos...")

    archivos = []
    extensiones = Counter()
    tamano_total = 0
    errores = 0

    for elemento in CARPETA.rglob("*"):
        try:
            if elemento.is_file():
                informacion = elemento.stat()
                tamano = informacion.st_size
                fecha_modificacion = datetime.fromtimestamp(
                    informacion.st_mtime
                )

                registro = {
                    "nombre": elemento.name,
                    "extension": obtener_extension(elemento),
                    "tamano_bytes": tamano,
                    "tamano_legible": convertir_tamano(tamano),
                    "fecha_modificacion": fecha_modificacion.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "ruta": str(elemento)
                }

                archivos.append(registro)
                extensiones[registro["extension"]] += 1
                tamano_total += tamano

        except (PermissionError, OSError) as error:
            errores += 1
            print(f"No se pudo analizar: {elemento}")
            print(f"Motivo: {error}")

    # Crear el archivo CSV con los detalles.
    with ARCHIVO_CSV.open(
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as archivo_csv:
        columnas = [
            "nombre",
            "extension",
            "tamano_bytes",
            "tamano_legible",
            "fecha_modificacion",
            "ruta"
        ]

        escritor = csv.DictWriter(
            archivo_csv,
            fieldnames=columnas
        )

        escritor.writeheader()
        escritor.writerows(archivos)

    # Ordenar extensiones de mayor a menor cantidad.
    extensiones_ordenadas = extensiones.most_common()

    # Crear el archivo de resumen.
    with ARCHIVO_RESUMEN.open("w", encoding="utf-8") as archivo_resumen:
        archivo_resumen.write("INFORME DE ARCHIVOS\n")
        archivo_resumen.write("=" * 50 + "\n\n")

        archivo_resumen.write(f"Carpeta analizada:\n{CARPETA}\n\n")
        archivo_resumen.write(f"Cantidad de archivos: {len(archivos)}\n")
        archivo_resumen.write(
            f"Espacio total ocupado: {convertir_tamano(tamano_total)}\n"
        )
        archivo_resumen.write(f"Elementos con error: {errores}\n\n")

        archivo_resumen.write("ARCHIVOS POR EXTENSION\n")
        archivo_resumen.write("-" * 50 + "\n")

        for extension, cantidad in extensiones_ordenadas:
            archivo_resumen.write(
                f"{extension}: {cantidad} archivo(s)\n"
            )

        archivo_resumen.write("\nARCHIVOS MÁS GRANDES\n")
        archivo_resumen.write("-" * 50 + "\n")

        archivos_mas_grandes = sorted(
            archivos,
            key=lambda archivo: archivo["tamano_bytes"],
            reverse=True
        )[:10]

        for numero, archivo in enumerate(archivos_mas_grandes, start=1):
            archivo_resumen.write(
                f"{numero}. {archivo['nombre']} - "
                f"{archivo['tamano_legible']}\n"
            )
            archivo_resumen.write(
                f"   {archivo['ruta']}\n"
            )

    print("\nInforme terminado.")
    print(f"Archivos analizados: {len(archivos)}")
    print(f"Espacio total: {convertir_tamano(tamano_total)}")
    print(f"Informe detallado: {ARCHIVO_CSV.resolve()}")
    print(f"Resumen: {ARCHIVO_RESUMEN.resolve()}")


if __name__ == "__main__":
    generar_informe()