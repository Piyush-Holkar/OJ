# compiler logic
from pathlib import Path
from django.conf import settings
from .lang_support import extension_map, executor_map
from .utils import resolve_path

CODES_DIR = Path(settings.CODES_DIR)
INPUTS_DIR = Path(settings.INPUTS_DIR)
OUTPUTS_DIR = Path(settings.OUTPUTS_DIR)


def run_code(
    lang,
    code_uuid,
    input_uuid=None,
    output_uuid=None,
    error_uuid=None,
    time_limit=5000,
    space_limit=256,
):
    extension = extension_map[lang]
    executor = executor_map.get(lang)

    code_path = resolve_path("code", code_uuid, lang)
    input_path = resolve_path("input", input_uuid)
    output_path = resolve_path("output", output_uuid)
    error_path = resolve_path("error", error_uuid)

    result = executor(
        code_path=str(code_path),
        input_path=str(input_path),
        output_path=str(output_path),
        error_path=str(error_path),
        time_limit=time_limit,
        space_limit=space_limit,
        code_file_uuid=code_uuid,
    )
    return result
