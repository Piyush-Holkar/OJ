from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from accounts.models import UserExtension
from ide.utils import resolve_path
from .judge import judge_submission
from django.contrib.auth.decorators import login_required, user_passes_test
from uuid import uuid4


# Create your views here.
def problems(request):
    problems = Problem.objects.all()
    context = {"problems": problems}
    return render(request, "problems/problems_list.html", context)


def problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        user_ext = UserExtension.objects.get(user=request.user)
        code = request.POST.get("code")
        lang = request.POST.get("lang")

        code_uuid = uuid4()
        code_path = resolve_path("code", code_uuid, lang)

        with open(code_path, "w") as code_file:
            code_file.write(code)

        verdict = judge_submission(problem, lang, code_uuid)

        Submission.objects.create(
            problem=problem,
            user=user_ext,
            code_file=code_uuid,
            lang=lang,
            verdict=verdict,
        )
        return JsonResponse({"verdict": verdict})

    return render(request, "problems/problem.html", {"problem": problem})


@user_passes_test(lambda u: u.is_superuser)
def create(request):
    if request.method == "POST":
        # problem fields
        title = request.POST.get("title")
        statement = request.POST.get("statement")
        time_limit = int(request.POST.get("time_limit"))
        space_limit = int(request.POST.get("space_limit"))
        tags = request.POST.get("tags", "")
        user_ext = UserExtension.objects.get(user=request.user)
        problem = Problem.objects.create(
            title=title,
            statement=statement,
            time_limit=time_limit,
            space_limit=space_limit,
            tags=tags,
            author=user_ext,
        )
        i = 0
        while f"input_text_{i}" in request.POST:
            i_uid = uuid4()
            o_uid = uuid4()
            input_path = resolve_path("input", i_uid)
            output_path = resolve_path("output", o_uid)
            with open(input_path, "w") as i_file:
                i_file.write(request.POST[f"input_text_{i}"].strip())
            with open(output_path, "w") as o_file:
                o_file.write(request.POST[f"output_text_{i}"].strip())

            TestCase.objects.create(
                problem=problem,
                tc_number=i,
                input_file=i_uid,
                output_file=o_uid,
            )
            i = i + 1
        return redirect("problems")
    return render(request, "problems/create_problem.html")


@login_required
def submissions(request):
    user_ext = UserExtension.objects.get(user=request.user)
    subs = Submission.objects.filter(user=user_ext).order_by("-created_at")
    context = {"submissions": subs}
    return render(request, "problems/submissions.html", context)


@login_required
def submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    # read code from file
    code_path = resolve_path("code", submission.code_file, submission.lang)
    with open(code_path, "r") as f:
        code = f.read()

    context = {
        "submission": submission,
        "code": code,
    }
    return render(request, "problems/submission.html", context)
