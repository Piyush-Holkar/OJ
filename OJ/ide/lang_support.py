# Maps language codes to file extensions
extension_map = {
    "cpp": "cpp",
    # "python": "py",
    # "java": "java",
    # "c": "c",
}

from .lang_runners import *

# Maps language codes to their executor functions
executor_map = {
    "cpp": run_cpp,
    # "python": run_python,
    # "java": run_java,
    # "c": run_c,
}
