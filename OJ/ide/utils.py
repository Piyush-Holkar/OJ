import os
from pathlib import Path
from django.conf import settings


CODES_DIR = Path(settings.CODES_DIR)
INPUTS_DIR = Path(settings.INPUTS_DIR)
OUTPUTS_DIR = Path(settings.OUTPUTS_DIR)


# code,exe,input,output,error
def resolve_path(file_type, uuid_value, lang=None):
    if not uuid_value:
        return None
    if file_type == "code":  # codes/uuid.extension
        from .lang_support import extension_map

        return CODES_DIR / f"{uuid_value}.{extension_map[lang]}"
    if file_type == "exe":  # codes/uuid
        return CODES_DIR / f"{uuid_value}"
    if file_type == "input":  # inputs/uuid.txt
        return INPUTS_DIR / f"{uuid_value}.txt"
    if file_type == "output":  # outputs/uuid_out.txt
        return OUTPUTS_DIR / f"{uuid_value}_out.txt"
    if file_type == "error":  # outputs/uuid_err.txt
        return OUTPUTS_DIR / f"{uuid_value}_err.txt"
    return None


def delete_files(paths):
    for path in paths:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                print(f"Error deleting {path}: {e}")
