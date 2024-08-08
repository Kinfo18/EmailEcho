import traceback
from src.logger import logger

class ErrorHandler:
    @staticmethod
    def handle(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_message = f"Error in {func.__name__}: {str(e)}\n{traceback.format_exc()}"
                logger.error(error_message)
                raise
        return wrapper

error_handler = ErrorHandler()