from django.http import JsonResponse
from django.shortcuts import render
from .compiler import run_code
from .lang_support import extension_map
from .utils import resolve_path, delete_files
import uuid


def ide(request):
    if request.method == "POST":
        lang = request.POST.get("language")
        code = request.POST.get("code")
        input_data = request.POST.get("input")

        uid = uuid.uuid4().hex  # shared UUID for all files

        code_path = resolve_path("code", uid, lang)
        input_path = resolve_path("input", uid)
        output_path = resolve_path("output", uid)
        error_path = resolve_path("error", uid)

        with open(code_path, "w") as f:
            f.write(code)

        if input_data.strip():
            with open(input_path, "w") as f:
                f.write(input_data)

        result = run_code(
            lang=lang,
            code_uuid=uid,
            input_uuid=uid if input_data.strip() else None,
            output_uuid=uid,
            error_uuid=uid,
        )

        try:
            with open(output_path, "r") as f:
                result["output"] = f.read()
        except FileNotFoundError:
            result["output"] = "(No output)"

        try:
            with open(error_path, "r") as f:
                # result["error"] = f.read()
                result["error"] = result["verdict"]

        except FileNotFoundError:
            result["error"] = "(No error)"

        additional_cleanup = result.pop("cleanup_paths", [])
        delete_files(
            [code_path, input_path, output_path, error_path, *additional_cleanup]
        )

        return JsonResponse(result)
    context = {"languages": list(extension_map.keys())}
    return render(request, "ide/ide.html", context)
