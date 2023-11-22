from google.cloud import storage
import os

def listar_archivos_en_gcs(bucket_nombre, carpeta_remota):
    nombres = []
    # Obtener la ruta completa al archivo de credenciales (en la misma carpeta que el script)
    ruta_credenciales = os.path.join(os.path.dirname(__file__), "local-sprite-405801-59e629ee469b.json")

    # Autenticación con las credenciales de Google Cloud
    client = storage.Client.from_service_account_json(ruta_credenciales)

    # Seleccionar el bucket en el que deseas listar los archivos
    bucket = client.get_bucket(bucket_nombre)

    try:
        # Listar los archivos en la carpeta remota
        blobs = bucket.list_blobs(prefix=carpeta_remota)

        # Imprimir los nombres de los archivos
        print(f"Nombres de archivos en {bucket_nombre}/{carpeta_remota}:")
        for blob in blobs:
            nombres.append(blob.name)

    except Exception as e:
        print(f"Error: {str(e)}")

    return nombres

def descargar_archivos_desde_gcs(bucket_nombre, archivos_remotos, carpeta_local):
    # Obtener la ruta completa a la carpeta local
    ruta_completa_carpeta_local = os.path.join(os.path.dirname(__file__), carpeta_local)

    # Autenticación con las credenciales de Google Cloud
    client = storage.Client.from_service_account_json(os.path.join(os.path.dirname(__file__), "local-sprite-405801-59e629ee469b.json"))

    # Seleccionar el bucket en el que se encuentran los archivos
    bucket = client.get_bucket(bucket_nombre)

    try:
        # Verificar si la carpeta local existe, si no, crearla
        if not os.path.exists(ruta_completa_carpeta_local):
            os.makedirs(ruta_completa_carpeta_local)

        for archivo_remoto in archivos_remotos:
            # Construir la ruta local para descargar el archivo
            ruta_local = os.path.join(ruta_completa_carpeta_local, os.path.basename(archivo_remoto))

            # Obtener el blob (archivo) desde el bucket
            blob = bucket.blob(archivo_remoto)

            # Descargar el archivo a la ruta local especificada
            blob.download_to_filename(ruta_local)

            print("\n")
            print(f"Archivo {archivo_remoto} descargado exitosamente a {ruta_local}")

        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

# Ejemplo de uso
bucket_nombre = "entrega-final-sql"
carpeta_remota = "Entrega"

# Listar archivos en Google Cloud Storage
archivos_para_descargar = listar_archivos_en_gcs(bucket_nombre, carpeta_remota)

# Eliminar el primer elemento de la lista
try:
    archivos_para_descargar.pop(0)
except IndexError:
    print("La lista está vacía o no hay elementos para eliminar.")

# Descargar archivos desde Google Cloud Storage
descargar_exitoso = descargar_archivos_desde_gcs(bucket_nombre, archivos_para_descargar, "descargas")

if descargar_exitoso:
    print("Descarga completa: Archivos descargados exitosamente.")
else:
    print("Error al descargar archivos.")
