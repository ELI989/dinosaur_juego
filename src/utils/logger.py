import logging

# Configurar el logger
logger = logging.getLogger('dino_logger')
logger.setLevel(logging.INFO)  # Nivel de logging: INFO

# Crear un manejador para el archivo de logging
file_handler = logging.FileHandler('dino_game.log')
file_handler.setLevel(logging.INFO)

# Crear un manejador para la consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Crear un formato de logging y agregarlo a los manejadores
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Agregar los manejadores al logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info('Logger configurado correctamente.')
