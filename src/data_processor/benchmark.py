import platform
from statistics import median
from timeit import repeat
from data_processor.processors import create_student_index, find_linear

SIZES = (1_000, 10_000, 100_000)


def generate_students(count: int) -> list[dict]:
    return [
        {"id": i, "first_name": f"Студент{i}", "last_name": f"Прізвище{i}",
         "group": f"ФЕП-{31 + i % 3}", "average_grade": float(i % 101)}
        for i in range(1, count + 1)
    ]


def run_benchmark() -> list[dict]:
    results = []
    for size in SIZES:
        students = generate_students(size)
        index = create_student_index(students)
        target = size
        assert find_linear(students, target) == index.get(target)
        linear = median(repeat(lambda: find_linear(students, target),
                               number=100, repeat=5)) / 100
        indexed = median(repeat(lambda: index.get(target),
                                number=100_000, repeat=5)) / 100_000
        build = median(repeat(lambda: create_student_index(students),
                              number=1, repeat=5))
        results.append({"records": size, "list_us": linear * 1e6,
                        "dict_us": indexed * 1e6, "build_ms": build * 1e3})
    return results


def main() -> None:
    print(f"Python {platform.python_version()} | {platform.system()} "
          f"{platform.machine()}")
    print("Медіана 5 серій; час одного пошуку останнього ID.")
    print(f"{'Записів':>10} {'list, мкс':>14} {'dict, мкс':>14} {'Індекс, мс':>14}")
    results = run_benchmark()
    for row in results:
        print(f"{row['records']:>10} {row['list_us']:>14.4f} "
              f"{row['dict_us']:>14.4f} {row['build_ms']:>14.4f}")



if __name__ == "__main__":
    main()
