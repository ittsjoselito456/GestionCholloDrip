class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'ja123@mysql'
    MYSQL_DATABASE = 'CholloDrip'
    # Leer la SECRET_KEY desde el archivo
    with open('secret_key.txt', 'r') as f:
        SECRET_KEY = f.read().strip()
