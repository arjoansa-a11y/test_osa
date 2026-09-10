import os
import re

print("🔍 Buscando la carpeta en tu sistema... Por favor, espera.")

# Nombre exacto de la carpeta que queremos buscar
nombre_carpeta_objetivo = "SiPillars"
ruta_encontrada = None

# Buscar de forma automática en toda tu carpeta de usuario (/home/tu_usuario)
ruta_home = os.path.expanduser("~")

for raiz, directorios, archivos in os.walk(ruta_home):
    if nombre_carpeta_objetivo in directorios:
        ruta_encontrada = os.path.join(raiz, nombre_carpeta_objetivo)
        break

# Si no la encuentra en home, buscamos en la raíz del sistema por si acaso
if not ruta_encontrada:
    for raiz, directorios, archivos in os.walk("/"):
        # Evitar buscar en carpetas del sistema para ir más rápido
        if any(p in raiz for p in ["/proc", "/sys", "/dev", "/var/lib"]):
            continue
        if nombre_carpeta_objetivo in directorios:
            ruta_encontrada = os.path.join(raiz, nombre_carpeta_objetivo)
            break

if not ruta_encontrada:
    print(f"❌ Error crítico: No se encontró ninguna carpeta llamada '{nombre_carpeta_objetivo}' en todo el sistema.")
    print("Verifica que el nombre esté perfectamente escrito (mayúsculas, guiones, etc.).")
    exit()

print(f"📍 ¡Carpeta encontrada con éxito en: {ruta_encontrada}")

# Expresión regular para buscar 'opm_power': valor
patron = r"('opm_power'\s*:\s*)([0-9.]+)"

print("\n🔄 Iniciando la modificación de archivos...")
archivos_modificados = 0

for raiz, directorios, archivos in os.walk(ruta_home):
    for archivo_nombre in archivos:
        if archivo_nombre.endswith('.txt'):
            ruta_archivo = os.path.join(raiz, archivo_nombre)
            
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Reemplazar el valor por su versión negativa
            nuevo_contenido = re.sub(patron, r"\1-\2", contenido)
            
            # Guardar si hubo cambios
            if nuevo_contenido != contenido:
                with open(ruta_archivo, 'w', encoding='utf-8') as f:
                    f.write(nuevo_contenido)
                # Muestra en qué subcarpeta estaba el archivo modificado
                subcarpeta_actual = os.path.basename(raiz)
                print(f"✅ Modificado en subcarpeta [{subcarpeta_actual}]: {archivo_nombre}")
                archivos_modificados += 1

print(f"\n🎉 ¡Proceso completado! Se revisaron todas las subcarpetas y se modificaron {archivos_modificados} archivos.")