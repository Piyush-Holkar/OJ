# Maps language codes to file extensions
extension_map = {
    "cpp": "cpp",
    "python": "py",
    # "java": "java",
    "c": "c",
}


# Maps language codes to their executor functions
from .lang_runners import run_cpp, run_python

executor_map = {
    "cpp": run_cpp,
    "python": run_python,
    # "java": run_java,
    "c": run_cpp,
}
