from django.shortcuts import render, redirect, get_object_or_404

from .models import Problem, Submission, TestCase
from accounts.models import UserExtension


# Create your views here.
def create(request):
    if request.method == "POST":
        # problem fields
        title = request.POST.get("title")
        statement = request.POST.get("statement")
        time_limit = request.POST.get("time_limit")
        space_limit = request.POST.get("space_limit")
        tags = request.POST.get("tags")
        input_text = request.POST.get("input_text")
        output_text = request.POST.get("output_text")
        user_ext = UserExtension.objects.get(user=request.user)
        problem = Problem.objects.create(
            title=title,
            statement=statement,
            time_limit=time_limit,
            space_limit=space_limit,
            tags=tags,
            author=user_ext,
        )
        TestCase.objects.create(
            problem=problem,
            tc_number=1,
            input_text=input_text,
            output_text=output_text,
        )
        return redirect("problems")
    return render(request, "problems/create_problem.html")


def problems(request):
    problems = Problem.objects.all()
    context = {"problems": problems}
    return render(request, "problems/problems_list.html", context)


def problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)

    if request.method == "POST":
        user_ext = UserExtension.objects.get(user=request.user)
        code = request.POST.get("code")
        lang = request.POST.get("lang")

        submission = Submission.objects.create(
            problem=problem,
            user=user_ext,
            code=code,
            lang=lang,
            verdict="Pending",
        )
        submission.save()
        return redirect("submissions")

    context = {
        "problem": problem,
    }
    return render(request, "problems/problem.html", context)


def submissions(request):
    user_ext = UserExtension.objects.get(user=request.user)
    subs = Submission.objects.filter(user=user_ext).order_by("-created_at")
    context = {"submissions": subs}
    return render(request, "problems/submissions.html", context)


def submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    context = {"submission": submission}
    return render(request, "problems/submission.html", context)
