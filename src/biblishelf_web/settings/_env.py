import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_FOLDER = os.environ.get('DATA_FOLDER', BASE_DIR)
DB_PATH = os.environ.get("DB_PATH", f'{DATA_FOLDER}/db.sqlite3')
GEN_DOC = True
ENABLE_DEBUG_TOOL = True
ENABLE_GRAPPELLI = False
STATIC_ROOT = os.environ.get("DJ_STATIC_ROOT", '/data')

