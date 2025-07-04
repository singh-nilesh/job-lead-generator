# contains Python runtime events (Exception, etc)
import sys
from src.logger import logging  

def error_message_detail(error, error_detail=None):
    try:
        if error_detail is None:
            error_detail = sys  # Fallback to sys if None is passed
        
        _, _, exc_tb = error_detail.exc_info()
        
        
        if exc_tb is not None:
            file_name = exc_tb.tb_frame.f_code.co_filename
            message = (
                f"\nError occurred in file: {file_name}, "
                f"at line: {exc_tb.tb_lineno}, \nerror: {str(error)}"
            )
        else:
            message = f"\nError occurred: {str(error)} (No traceback info available)"
        return message
    except Exception as e:
        return f"\nFailed to get error details: {str(e)} (Original error: {str(error)})"

# Custom Exception to be used for Logger
class CustomException(Exception):
    def __init__(self, error, error_details=None):
        super().__init__(str(error))
        self.error_message = error_message_detail(error, error_details)

    def __str__(self):
        return self.error_message

# Example test block
if __name__ == "__main__":    
    try:
        a = 1/0
    except Exception as e:
        logging.info("Divide by Zero")
        raise CustomException(e)  # Can now be called without passing sys
