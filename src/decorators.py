import logging
from functools import wraps


logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)


def report_decorator(file_path):
    """
    Декоратор для функций-отчетов, записывает в файл результат, который возвращает функция, формирующая отчет.
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(file_path, "w") as file:
                file.write(result)
            return result

        return inner

    return wrapper


def log_function_call(func):
    """
    Декоратор для логирования
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Вызов функции: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Функция: {func.__name__} выполнена успешно.")
            return result
        except Exception as e:
            logger.error(f"Ошибка в функции: {func.__name__}. Ошибка: {str(e)}")
            raise

    return wrapper
