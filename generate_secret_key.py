import os

# Ruta del archivo donde se guardará la SECRET_KEY
secret_key_file = 'secret_key.txt'

# Verificar si el archivo ya existe
if not os.path.exists(secret_key_file):
    # Generar una nueva SECRET_KEY
    secret_key = os.urandom(24).hex()
    # Guardar la SECRET_KEY en el archivo
    with open(secret_key_file, 'w') as f:
        f.write(secret_key)
    print(f"SECRET_KEY generada y guardada en {secret_key_file}")
else:
    print(f"El archivo {secret_key_file} ya existe. No se generó una nueva SECRET_KEY.")
