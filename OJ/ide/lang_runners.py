import time
from subprocess import TimeoutExpired
import subprocess
from pathlib import Path
from django.conf import settings
from .utils import resolve_path


CODES_DIR = Path(settings.CODES_DIR)
INPUTS_DIR = Path(settings.INPUTS_DIR)
OUTPUTS_DIR = Path(settings.OUTPUTS_DIR)


def run_cpp(
    code_path,
    input_path=None,
    output_path=None,
    error_path=None,
    time_limit=5000,
    space_limit=256,
    code_file_uuid=None,
):
    verdict = ""
    execution_time = 0
    exe_file_path = resolve_path("exe", code_file_uuid)

    # compile only if exe file doesn't exist (to avoid re-compilation)
    if not exe_file_path.exists():
        compiler_result = subprocess.run(
            ["g++", code_path, "-o", str(exe_file_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if compiler_result.returncode != 0:
            if error_path:
                with open(error_path, "w") as err_file:
                    err_file.write(compiler_result.stderr.decode())

            return {
                "verdict": f"Compilation Error (exit code {compiler_result.returncode})",
                "time_used": 0,
                "memory_used": 0,
            }

    # Execute compiled binary
    stdin_file = (
        open(input_path, "r") if input_path and Path(input_path).exists() else None
    )

    try:
        with open(output_path, "w") as out_file, open(error_path, "w") as err_file:
            start_time = time.time()
            exe_result = subprocess.run(
                [str(exe_file_path)],
                stdin=stdin_file,
                stdout=out_file,
                stderr=err_file,
                timeout=time_limit / 1000,
            )
            execution_time = time.time() - start_time

        if exe_result.returncode == 0:
            verdict = "Success"
        else:
            verdict = "Runtime Error"

    except TimeoutExpired:
        execution_time = time.time() - start_time
        verdict = "TLE"
        if error_path:
            with open(error_path, "a") as err_file:
                err_file.write("\nTime Limit Exceeded")

    finally:
        if stdin_file:
            stdin_file.close()

    return {
        "verdict": verdict,
        "time_used": round(execution_time, 3),
        "memory_used": "coming soon...",
        "cleanup_paths": [str(exe_file_path)],
    }
