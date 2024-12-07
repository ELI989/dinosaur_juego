import sqlite3

def mostrar_resultados():
    """Muestra todos los resultados guardados en la base de datos."""
    # Establece conexión con la base de datos correcta
    connection = sqlite3.connect("juego_dino.db")
    cursor = connection.cursor()
    
    # Ejecuta la consulta para obtener todos los resultados
    cursor.execute('SELECT * FROM resultados')
    resultados = cursor.fetchall()
    
    # Imprime cada resultado
    for resultado in resultados:
        print(f'ID: {resultado[0]}, Fecha y Hora: {resultado[1]}, Tiempo Perdido: {resultado[2]} segundos')
    
    # Cierra la conexión
    connection.close()

# Cerrar la conexión principal
def close_connection():
    conn.close()  # noqa: F821

# Llama a la función para mostrar resultados después de que finaliza el juego
if __name__ == "__main__":
    mostrar_resultados()
