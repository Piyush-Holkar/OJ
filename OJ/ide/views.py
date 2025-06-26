from django.shortcuts import render
from .compiler import run_code
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

        context = run_code(
            lang=lang,
            code_uuid=uid,
            input_uuid=uid if input_data.strip() else None,
            output_uuid=uid,
            error_uuid=uid,
        )

        try:
            with open(output_path, "r") as f:
                context["output"] = f.read()
        except FileNotFoundError:
            context["output"] = "(No output)"

        try:
            with open(error_path, "r") as f:
                context["error"] = f.read()
        except FileNotFoundError:
            context["error"] = "(No error)"

        additional_cleanup = context.pop("cleanup_paths", [])
        delete_files(
            [code_path, input_path, output_path, error_path, *additional_cleanup]
        )

        return render(request, "ide/ide.html", {"context": context})

    return render(request, "ide/ide.html")
