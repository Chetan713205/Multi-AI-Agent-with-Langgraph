import subprocess
import threading
import time
from dotenv import load_dotenv
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

load_dotenv()

def run_backend():
    try:
        logger.info("..... Starting backend Service .....")
        subprocess.run(["uvicorn", "app.backend.api:app", "--host", "127.0.0.1", "--port", "9999"], check=True)
    except Exception as e:
        logger.error(f"Failed to start backend service: {e}")
        raise CustomException("Failed to start backend service") from e
    
def run_frontend():
    try:
        logger.info("..... Starting frontend Service .....")
        subprocess.run(["streamlit", "run", "app/frontend/ui.py"], check=True)
    except Exception as e:
        logger.error(f"Failed to start frontend service: {e}")
        raise CustomException("Failed to start frontend service") from e
    
if __name__ == "__main__":
    backend_thread = threading.Thread(target=run_backend)
    frontend_thread = threading.Thread(target=run_frontend)

    backend_thread.start()
    time.sleep(1)  # Give frontend some time to start
    frontend_thread.start()

    backend_thread.join()
    frontend_thread.join()