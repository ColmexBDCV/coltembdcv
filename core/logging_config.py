# logging_config.py
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,  # Cambia a INFO, WARNING, etc., según tus necesidades
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logging.getLogger("uvicorn").setLevel(logging.INFO)  # Configurar logs de uvicorn
