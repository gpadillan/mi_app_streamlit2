import sqlite3

def conectar_bd():
    return sqlite3.connect("database/app.db", check_same_thread=False)

def crear_tablas():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()

crear_tablas()
