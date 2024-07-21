import logging

def setup_logger(log_file, log_level=logging.INFO):
    # Создание объекта логгера
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # Создание обработчика для записи в файл
    file_handler = logging.FileHandler(log_file)

    # Создание формата для записи логов
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Добавление обработчика к логгеру
    logger.addHandler(file_handler)

    return logger


# logger = setup_logger('./eevee8/logs.txt')

def write_log(logger=setup_logger('./eevee8/logs.txt'), message=''):
    logger.info(message)