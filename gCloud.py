from google.cloud import storage
import os

def subir_archivos_a_gcs(bucket_nombre, carpeta_local, carpeta_remota):
    # Obtener la ruta completa a la carpeta local y al archivo de credenciales
    ruta_completa_carpeta_local = os.path.join(os.path.dirname(__file__), carpeta_local)
    ruta_credenciales = os.path.join(os.path.dirname(__file__), "local-sprite-405801-59e629ee469b.json")

    # Autenticación con las credenciales de Google Cloud
    client = storage.Client.from_service_account_json(ruta_credenciales)

    # Seleccionar el bucket en el que deseas almacenar los archivos
    bucket = client.get_bucket(bucket_nombre)

    try:
        # Obtener la lista de archivos en la carpeta local
        archivos_locales = os.listdir(ruta_completa_carpeta_local)

        for archivo_local in archivos_locales:
            # Construir la ruta completa al archivo local
            ruta_completa_local = os.path.join(ruta_completa_carpeta_local, archivo_local)

            # Construir la ruta remota en Google Cloud Storage
            archivo_remoto = os.path.join(carpeta_remota, archivo_local).replace(os.path.sep, "/")

            # Subir el archivo local al bucket con un nombre remoto específico
            blob = bucket.blob(archivo_remoto)
            blob.upload_from_filename(ruta_completa_local)

            print("\n")
            print(f"Archivo {ruta_completa_local} subido exitosamente a {bucket_nombre}/{archivo_remoto}")

    except Exception as e:
        print(f"Error: {str(e)}")

# Ejemplo de uso
bucket_nombre = "entrega-final-sql"
carpeta_local = "subir"
carpeta_remota = "Entrega"

subir_archivos_a_gcs(bucket_nombre, carpeta_local, carpeta_remota)
