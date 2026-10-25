import argparse
from data_processor.data import get_students
from data_processor.analytics import (
    calculate_average, calculate_average_values, create_record,
    create_grade_filter, find_best_student,
)
from data_processor.processors import (
    get_unique_groups, create_student_index, filter_items, sort_items,
    group_students, count_students_by_group,
)


def print_students(title: str, students: list[dict]) -> None:
    print(f"\n{title}")
    print(f"{'ID':<4} {'Прізвище та ім’я':<25} {'Група':<10} Бал")
    print("-" * 50)
    for student in students:
        name = f"{student['last_name']} {student['first_name']}"
        print(f"{student['id']:<4} {name:<25} "
              f"{student['group']:<10} {student['average_grade']:.2f}")
    if not students:
        print("Записів немає.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Аналіз обліку студентів")
    parser.add_argument("--threshold", type=float, default=85.0)
    parser.add_argument("--student-id", type=int, default=3)
    args = parser.parse_args()
    if not 0 <= args.threshold <= 100:
        parser.error("Пороговий бал має бути від 0 до 100.")

    students = get_students()
    print_students("Усі студенти", students)
    print("\nУнікальні групи:", ", ".join(sorted(get_unique_groups(students))))
    average = calculate_average(students)
    print("Середній бал:", f"{average:.2f}" if average is not None else "немає даних")
    best = find_best_student(students)
    print_students("Найкращий студент", [best] if best else [])
    selected = filter_items(students, create_grade_filter(args.threshold))
    print_students(f"Бал вище {args.threshold:g}", selected)
    ranking = sort_items(students, key=lambda s: s["average_grade"], reverse=True)
    print_students("Рейтинг студентів", ranking)
    for group, members in group_students(students).items():
        print_students(f"Група {group}", members)
    print("\nКількість студентів у групах:")
    for group, count in count_students_by_group(students).items():
        print(f"{group}: {count}")
    index = create_student_index(students)
    found = index.get(args.student_id)
    print_students(f"Пошук ID {args.student_id}", [found] if found else [])
    grades = tuple(s["average_grade"] for s in students)
    print("\nСередній бал через *args:", calculate_average_values(*grades))
    summary = create_record(count=len(students), average=average,
                            groups=len(get_unique_groups(students)))
    print("Підсумок через **kwargs:", summary)


if __name__ == "__main__":
    main()
