import os
from pathlib import Path

CUR_DIR = os.path.realpath(os.path.dirname(__file__))
PACKAGE_DIR = os.path.dirname(CUR_DIR)
NOTES_DIR = os.path.join(Path.home(), ".prise-de-note")