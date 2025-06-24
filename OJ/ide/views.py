from django.shortcuts import render
from .compiler import run_code


def ide(request):
    if request.method == "POST":
        code = request.POST.get("code")
        lang = request.POST.get("language")
        input_data = request.POST.get("input")
        context = run_code(lang, code, input_data, save_temps=False)
        return render(request, "ide/ide.html", {"context": context})

    return render(request, "ide/ide.html")
