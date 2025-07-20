# seed from json 
import os
import django
import json
from uuid import uuid4

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OJ.settings")
django.setup()

from problems.models import Problem, TestCase
from accounts.models import UserExtension
from ide.utils import resolve_path

ADMIN_USERNAME = "admin"
JSON_FILE = os.path.join("fixtures", "problems.json")

try:
    admin_user_ext = UserExtension.objects.get(user__username=ADMIN_USERNAME)
except UserExtension.DoesNotExist:
    print(f"Admin user '{ADMIN_USERNAME}' not found.")
    exit(1)

try:
    with open(JSON_FILE, "r") as f:
        problems_data = json.load(f)
except Exception as e:
    print(f"Failed to load JSON file: {e}")
    exit(1)

for pdata in problems_data:
    print(f"→ Adding: {pdata['title']}")

    problem = Problem.objects.create(
        title=pdata["title"],
        statement=pdata["statement"],
        time_limit=pdata["time_limit"],
        space_limit=pdata["space_limit"],
        tags=pdata.get("tags", ""),
        author=admin_user_ext,
    )

    for i, tc in enumerate(pdata["testcases"]):
        i_uid = uuid4()
        o_uid = uuid4()

        input_path = resolve_path("input", i_uid)
        output_path = resolve_path("output", o_uid)

        with open(input_path, "w") as infile:
            infile.write(tc["input"].strip())

        with open(output_path, "w") as outfile:
            outfile.write(tc["output"].strip())

        TestCase.objects.create(
            problem=problem, tc_number=i, input_file=i_uid, output_file=o_uid
        )

print("All problems seeded successfully.")
