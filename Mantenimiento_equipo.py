from pathlib import Path
from datetime import datetime
import tempfile
import platform
import shutil
import os


ARCHIVO_INFORME = Path("informe_estado_equipo.txt")


def convertir_tamano(bytes_archivo):
    """Convierte bytes a una unidad más fácil de leer."""
    unidades = ["B", "KB", "MB", "GB", "TB"]
    tamano = float(bytes_archivo)

    for unidad in unidades:
        if tamano < 1024:
            return f"{tamano:.2f} {unidad}"

        tamano /= 1024

    return f"{tamano:.2f} PB"


def analizar_temporales(carpeta):
    """
    Analiza la carpeta temporal y devuelve:
    cantidad de archivos, tamaño total, carpetas y errores.
    """
    cantidad_archivos = 0
    tamano_total = 0
    cantidad_carpetas = 0
    errores = 0

    try:
        for raiz, nombres_carpetas, nombres_archivos in os.walk(carpeta):
            cantidad_carpetas += len(nombres_carpetas)

            for nombre in nombres_archivos:
                archivo = Path(raiz) / nombre

                try:
                    if archivo.is_file():
                        cantidad_archivos += 1
                        tamano_total += archivo.stat().st_size

                except (PermissionError, OSError):
                    errores += 1

    except (PermissionError, OSError):
        errores += 1

    return (
        cantidad_archivos,
        tamano_total,
        cantidad_carpetas,
        errores
    )


def obtener_archivos_temporales(carpeta):
    """Devuelve listas de archivos y carpetas temporales."""
    archivos = []
    carpetas = []

    try:
        for raiz, nombres_carpetas, nombres_archivos in os.walk(
            carpeta,
            topdown=False
        ):
            ruta_raiz = Path(raiz)

            for nombre in nombres_archivos:
                archivo = ruta_raiz / nombre

                try:
                    if archivo.is_file():
                        archivos.append(archivo)
                except OSError:
                    pass

            for nombre in nombres_carpetas:
                subcarpeta = ruta_raiz / nombre

                try:
                    if subcarpeta.is_dir():
                        carpetas.append(subcarpeta)
                except OSError:
                    pass

    except (PermissionError, OSError):
        pass

    return archivos, carpetas


def limpiar_temporales(carpeta):
    """Elimina archivos temporales y carpetas que queden vacías."""
    archivos, carpetas = obtener_archivos_temporales(carpeta)

    eliminados = 0
    no_eliminados = 0
    espacio_liberado = 0

    for archivo in archivos:
        try:
            tamano = archivo.stat().st_size
            archivo.unlink()

            eliminados += 1
            espacio_liberado += tamano

        except (PermissionError, OSError):
            no_eliminados += 1

    carpetas_eliminadas = 0

    for carpeta in sorted(
        carpetas,
        key=lambda elemento: len(elemento.parts),
        reverse=True
    ):
        try:
            carpeta.rmdir()
            carpetas_eliminadas += 1
        except (PermissionError, OSError):
            pass

    return (
        eliminados,
        no_eliminados,
        carpetas_eliminadas,
        espacio_liberado
    )


def generar_informe():
    ahora = datetime.now()
    carpeta_temporal = Path(tempfile.gettempdir())

    # Información del disco donde está instalado Windows.
    disco = Path.home().anchor
    uso_disco = shutil.disk_usage(disco)

    archivos_temp, tamano_temp, carpetas_temp, errores = (
        analizar_temporales(carpeta_temporal)
    )

    try:
        nombre_equipo = platform.node()
    except Exception:
        nombre_equipo = "No disponible"

    try:
        usuario = os.getlogin()
    except Exception:
        usuario = "No disponible"

    contenido = []

    contenido.append("INFORME DE ESTADO Y MANTENIMIENTO DEL EQUIPO")
    contenido.append("=" * 60)
    contenido.append(f"Fecha del informe: {ahora:%Y-%m-%d %H:%M:%S}")
    contenido.append("")

    contenido.append("INFORMACIÓN DEL SISTEMA")
    contenido.append("-" * 60)
    contenido.append(f"Usuario: {usuario}")
    contenido.append(f"Nombre del equipo: {nombre_equipo}")
    contenido.append(f"Sistema operativo: {platform.system()}")
    contenido.append(f"Versión: {platform.version()}")
    contenido.append(f"Arquitectura: {platform.machine()}")
    contenido.append(
        f"Procesador: {platform.processor() or 'No disponible'}"
    )
    contenido.append(f"Núcleos disponibles: {os.cpu_count()}")
    contenido.append("")

    contenido.append("ESPACIO DEL DISCO")
    contenido.append("-" * 60)
    contenido.append(f"Unidad analizada: {disco}")
    contenido.append(
        f"Espacio total: {convertir_tamano(uso_disco.total)}"
    )
    contenido.append(
        f"Espacio utilizado: {convertir_tamano(uso_disco.used)}"
    )
    contenido.append(
        f"Espacio libre: {convertir_tamano(uso_disco.free)}"
    )
    contenido.append("")

    contenido.append("ARCHIVOS TEMPORALES")
    contenido.append("-" * 60)
    contenido.append(f"Carpeta analizada: {carpeta_temporal}")
    contenido.append(f"Archivos encontrados: {archivos_temp}")
    contenido.append(f"Carpetas encontradas: {carpetas_temp}")
    contenido.append(
        f"Espacio temporal: {convertir_tamano(tamano_temp)}"
    )
    contenido.append(f"Elementos con error: {errores}")
    contenido.append("")

    informe = "\n".join(contenido)

    with ARCHIVO_INFORME.open("w", encoding="utf-8") as archivo:
        archivo.write(informe)

    print(informe)
    print("=" * 60)
    print(f"Informe guardado en: {ARCHIVO_INFORME.resolve()}")

    return carpeta_temporal, archivos_temp, tamano_temp


def ejecutar():
    print("Generando informe del equipo...\n")

    carpeta_temporal, archivos_temp, tamano_temp = generar_informe()

    if archivos_temp == 0:
        print("\nNo se encontraron archivos temporales.")
        return

    print()
    print(
        f"Se encontraron {archivos_temp} archivos temporales "
        f"que ocupan {convertir_tamano(tamano_temp)}."
    )

    respuesta = input(
        "\n¿Quieres limpiar los archivos temporales? "
        "Escribe SI para continuar: "
    )

    if respuesta.strip().upper() != "SI":
        print("Limpieza cancelada. El informe ya fue generado.")
        return

    print("\nLimpiando archivos temporales...")

    (
        eliminados,
        no_eliminados,
        carpetas_eliminadas,
        espacio_liberado
    ) = limpiar_temporales(carpeta_temporal)

    print("\nLimpieza terminada.")
    print(f"Archivos eliminados: {eliminados}")
    print(f"Carpetas vacías eliminadas: {carpetas_eliminadas}")
    print(f"Archivos bloqueados: {no_eliminados}")
    print(f"Espacio liberado: {convertir_tamano(espacio_liberado)}")


if __name__ == "__main__":
    ejecutar()