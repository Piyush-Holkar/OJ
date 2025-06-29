from .models import *
from ide.compiler import run_code
from ide.utils import resolve_path, delete_files


def judge_submission(problem, lang, code_uuid):
    verdict = "Success"
    cleanup_paths = []

    output_path = resolve_path("output", code_uuid)
    error_path = resolve_path("error", code_uuid)
    cleanup_paths.extend([output_path, error_path])

    testcases = TestCase.objects.filter(problem=problem).order_by("tc_number")

    for tc in testcases:
        result = run_code(
            lang=lang,
            code_uuid=code_uuid,
            input_uuid=tc.input_file,
            output_uuid=code_uuid,
            error_uuid=code_uuid,
            time_limit=problem.time_limit,
            space_limit=problem.space_limit,
        )

        if "cleanup_paths" in result:
            cleanup_paths.extend(result["cleanup_paths"])

        if result["verdict"] != "Success":
            delete_files(cleanup_paths)
            return f'{result["verdict"]} at TC{tc.tc_number}'

        if not compare_outputs(code_uuid, tc.output_file):
            delete_files(cleanup_paths)
            return f"Wrong Answer at TC{tc.tc_number}"

    delete_files(cleanup_paths)
    return verdict


def compare_outputs(user_output_uuid, expected_output_uuid):
    user_output_path = resolve_path("output", user_output_uuid)
    expected_output_path = resolve_path("output", expected_output_uuid)
    with open(user_output_path, "r") as uo, open(expected_output_path, "r") as eo:
        user_lines = [line.rstrip() for line in uo]
        expected_lines = [line.rstrip() for line in eo]
    return user_lines == expected_lines
