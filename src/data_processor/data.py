STUDENT_FIELDS = ("id", "first_name", "last_name", "group", "average_grade")


def get_students() -> list[dict]:
    rows = [
        (1, "Марія", "Дорош", "ФЕП-32", 86.5),
        (2, "Данило", "Левицький", "ФЕП-31", 95.0),
        (3, "Соломія", "Климчук", "ФЕП-32", 91.5),
        (4, "Остап", "Мазур", "ФЕП-31", 78.0),
        (5, "Олена", "Романюк", "ФЕП-33", 85.0),
        (6, "Тарас", "Дорош", "ФЕП-33", 72.0),
    ]
    return [dict(zip(STUDENT_FIELDS, row)) for row in rows]
