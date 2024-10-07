from pathlib import Path
from flask import current_app
import os

def get_download_data_path():
    """
    Retorna la ruta completa para descargar datos, basada en la configuración actual.
    """
    return Path(current_app.root_path) / (current_app.config.get("DOWNLOAD_DATA_PATH"))
