import time
import os
from subprocess import TimeoutExpired
import subprocess
from pathlib import Path
from django.conf import settings

CODES_DIR = Path(settings.CODES_DIR)
INPUTS_DIR = Path(settings.INPUTS_DIR)
OUTPUTS_DIR = Path(settings.OUTPUTS_DIR)

# def any <lang> runner with following signature:

# def run_<lang>(file_info, code, input_str, save_temps, time_limit, space_limit):


#     return {
#         "output": "Hello",
#         "error": "",
#         "verdict": "Success",
#         "time_used": 0.42,
#         "memory_used": 12.5,
#     }
# Use this after lang_support.py mapping is done


# to run cpp files using gcc
def run_cpp(file_info, code, input_str, save_temps, time_limit, space_limit):
    verdict = ""
    execution_time = 0
    write_file(file_info["code_file_path"], code)
    exe_file_path = CODES_DIR / file_info["uuid"]
    compiler_result = subprocess.run(
        ["g++", file_info["code_file_path"], "-o", str(exe_file_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=time_limit,
    )
    if compiler_result.returncode != 0:
        verdict = f"Compilation Error (exit code {compiler_result.returncode})"
        if not save_temps:
            cleanup_files(file_info["code_file_path"])
        return {
            "output": "error",
            "error": compiler_result.stderr.decode(),
            "verdict": verdict,
            "time_used": 0,
            "memory_used": 0,
        }
    write_file(file_info["input_file_path"], input_str)

    with open(file_info["output_file_path"], "w") as output_file, open(
        file_info["error_file_path"], "w"
    ) as error_file:
        stdin_file = None
        try:
            if input_str.strip():
                stdin_file = open(file_info["input_file_path"], "r")
            execution_time = time.time()
            exe_result = subprocess.run(
                [str(exe_file_path)],
                stdin=stdin_file,
                stdout=output_file,
                stderr=error_file,
                timeout=time_limit / 1000,
            )
            execution_time = time.time() - execution_time
        except TimeoutExpired:
            execution_time = time.time() - execution_time
            exe_result = None
            verdict = "TLE"
            error_file.write("Time Limit Exceeded")

        finally:
            if stdin_file:
                stdin_file.close()

    output = read_file(file_info["output_file_path"])
    error = read_file(file_info["error_file_path"])
    if verdict == "" and exe_result.returncode == 0:
        verdict = "Success"
    else:
        verdict = "Runtime error"
    if not save_temps:
        cleanup_files(
            file_info["code_file_path"],
            file_info["input_file_path"],
            file_info["output_file_path"],
            file_info["error_file_path"],
            str(exe_file_path),
        )

    return {
        "output": output,
        "error": error,
        "verdict": verdict,
        "time_used": str(round(execution_time, 3)) + "seconds",
        "memory_used": "coming soon...",
    }


def cleanup_files(*paths):
    for path in paths:
        try:
            os.remove(path)
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"Error deleting file {path}: {e}")


def write_file(path, data):
    if data.strip():
        with open(path, "w") as input_file:
            input_file.write(data)


def read_file(path):
    try:
        with open(path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return ""
