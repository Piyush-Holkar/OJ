from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import UserExtension
import os
import json
from dotenv import load_dotenv
from django.http import JsonResponse
import google.generativeai as genai
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST


# Create your views here.


def homepage(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "core/homepage.html")


@login_required
def dashboard(request):
    user_ext = get_object_or_404(UserExtension, user=request.user)
    context = {
        "user_ext": user_ext,
    }
    return render(request, "core/dashboard.html", context)


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_ext = get_object_or_404(UserExtension, user=user)
    context = {
        "user": user,
        "user_ext": user_ext,
    }
    return render(request, "core/profile.html", context)


# AI prompts
PROMPT_SIMPLIFY = (
    "Break down this coding problem in simple words, like you're explaining to a beginner. "
    "Keep it short and clear:\n\n{}"
)

PROMPT_HINT = (
    "Give a very short (max 5 lines) coding hint for solving this problem. "
    "Do not reveal the full solution, only nudge the thought process:\n\n{}"
)

PROMPT_REVIEW = (
    "Here is a coding problem followed by a submitted solution. "
    "First, give a score out of 10 for the code. Then provide suggestions if any to improve code quality, readability, or logic. "
    "If the code is already good, say so clearly. Make it short without skipping important points like code quality, readability.\n\nProblem:\n{}\n\nCode:\n{}"
)


@require_POST
@csrf_protect
def AI(request):
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    try:
        body = json.loads(request.body)
        action = body.get("action")
        statement = body.get("statement", "")
        code = body.get("code", "")

        model = genai.GenerativeModel("gemini-2.0-flash")

        if action == "simplify":
            prompt = PROMPT_SIMPLIFY.format(statement)
        elif action == "hint":
            if not statement.strip():
                return JsonResponse(
                    {"error": "Empty problem statement for hint"}, status=400
                )
            prompt = PROMPT_HINT.format(statement)
        elif action == "review":
            if not code.strip():
                return JsonResponse({"error": "Empty code for review"}, status=400)
            prompt = PROMPT_REVIEW.format(statement, code)
        else:
            return JsonResponse({"error": "Invalid action"}, status=400)

        response = model.generate_content(prompt)
        return JsonResponse({"text": response.text})

    except Exception as e:
        import traceback

        print("AI View Error:", traceback.format_exc())
        return JsonResponse({"error": str(e)}, status=500)
