from collections.abc import Callable
from data_processor.decorators import measure_time


@measure_time
def calculate_average(students: list[dict]) -> float | None:
    if not students:
        return None
    return sum(s["average_grade"] for s in students) / len(students)


def find_best_student(students: list[dict]) -> dict | None:
    return max(students, key=lambda s: s["average_grade"], default=None)


def calculate_average_values(*values: float) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def create_record(**fields) -> dict:
    return dict(fields)


def create_grade_filter(threshold: float) -> Callable[[dict], bool]:
    def predicate(student: dict) -> bool:
        return student["average_grade"] > threshold

    return predicate
