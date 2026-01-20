import os
import sys

def resource_path(relative_path):
    """
    Mengembalikan path resource (icon, gambar, dll)
    Support Python biasa & PyInstaller (.exe)
    """
    try:
        # Mode PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Mode Python biasa
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
