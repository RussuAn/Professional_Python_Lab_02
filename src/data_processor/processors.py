from collections import Counter, defaultdict
from collections.abc import Callable


def get_unique_groups(students: list[dict]) -> set[str]:
    return {student["group"] for student in students}


def create_student_index(students: list[dict]) -> dict[int, dict]:
    index = {student["id"]: student for student in students}
    if len(index) != len(students):
        raise ValueError("ID студентів мають бути унікальними.")
    return index


def find_linear(students: list[dict], student_id: int) -> dict | None:
    for student in students:
        if student["id"] == student_id:
            return student
    return None


def filter_items(items: list[dict], predicate: Callable) -> list[dict]:
    return [item for item in items if predicate(item)]


def sort_items(items: list[dict], key: Callable,
               reverse: bool = False) -> list[dict]:
    return sorted(items, key=key, reverse=reverse)


def group_students(students: list[dict]) -> dict[str, list[dict]]:
    grouped = defaultdict(list)
    for student in students:
        grouped[student["group"]].append(student)
    return dict(grouped)


def count_students_by_group(students: list[dict]) -> Counter:
    return Counter(student["group"] for student in students)
