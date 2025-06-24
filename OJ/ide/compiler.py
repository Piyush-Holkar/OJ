# compiler logic
from pathlib import Path
from django.conf import settings
import uuid
from .lang_support import extension_map, executor_map

CODES_DIR = Path(settings.CODES_DIR)
INPUTS_DIR = Path(settings.INPUTS_DIR)
OUTPUTS_DIR = Path(settings.OUTPUTS_DIR)


def run_code(
    lang, code, input_str="", save_temps=True, time_limit=5000, space_limit=256
):
    file_info = setup_file_paths(lang)
    executor = executor_map.get(lang)
    result = executor(file_info, code, input_str, save_temps, time_limit, space_limit)

    return result


def setup_file_paths(lang):
    file_uuid = uuid.uuid4().hex
    extension = extension_map.get(lang)

    code_file_name = f"{file_uuid}.{extension}"
    input_file_name = f"{file_uuid}.txt"
    output_file_name = f"{file_uuid}_out.txt"
    error_file_name = f"{file_uuid}_err.txt"

    code_file_path = CODES_DIR / code_file_name
    input_file_path = INPUTS_DIR / input_file_name
    output_file_path = OUTPUTS_DIR / output_file_name
    error_file_path = OUTPUTS_DIR / error_file_name

    return {
        "uuid": file_uuid,
        "code_file_name": code_file_name,
        "input_file_name": input_file_name,
        "output_file_name": output_file_name,
        "error_file_name": error_file_name,
        "code_file_path": str(code_file_path),
        "input_file_path": str(input_file_path),
        "output_file_path": str(output_file_path),
        "error_file_path": str(error_file_path),
    }
