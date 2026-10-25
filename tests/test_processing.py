import pytest
from data_processor.data import get_students
from data_processor.analytics import (
    calculate_average, calculate_average_values, create_record,
    create_grade_filter, find_best_student,
)
from data_processor.processors import (
    get_unique_groups, create_student_index, find_linear, filter_items,
    sort_items, group_students, count_students_by_group,
)


def test_summary():
    students = get_students()
    assert calculate_average(students) == pytest.approx(508 / 6)
    assert find_best_student(students)['id'] == 2
    assert get_unique_groups(students) == {'ФЕП-31', 'ФЕП-32', 'ФЕП-33'}
    assert dict(count_students_by_group(students)) == {
        'ФЕП-31': 2, 'ФЕП-32': 2, 'ФЕП-33': 2}
    assert len(group_students(students)['ФЕП-32']) == 2


def test_strict_threshold_and_independent_closures():
    students = get_students()
    above85, above95 = create_grade_filter(85), create_grade_filter(95)
    assert [s['id'] for s in filter_items(students, above85)] == [1, 2, 3]
    assert filter_items(students, above95) == []
    assert not above85(students[4])


def test_index_search_and_duplicate_surnames():
    students = get_students()
    index = create_student_index(students)
    assert index[1]['last_name'] == index[6]['last_name']
    assert index.get(3) == find_linear(students, 3)
    assert index.get(999) is None
    assert find_linear(students, 999) is None
    with pytest.raises(ValueError):
        create_student_index(students + [students[0]])


def test_sort_preserves_input():
    students = get_students()
    original_ids = [s['id'] for s in students]
    ranking = sort_items(students, lambda s: s['average_grade'], reverse=True)
    assert [s['id'] for s in ranking] == [2, 3, 1, 5, 4, 6]
    assert [s['id'] for s in students] == original_ids
    names = sort_items(students, lambda s: s['last_name'])
    assert names[0]['last_name'] == 'Дорош'


def test_empty_collections():
    assert calculate_average([]) is None
    assert find_best_student([]) is None
    assert calculate_average_values() is None
    assert get_unique_groups([]) == set()
    assert group_students([]) == {}
    assert create_student_index([]) == {}
    assert filter_items([], create_grade_filter(85)) == []
    assert find_linear([], 1) is None


def test_args_kwargs_and_decorator(capsys):
    assert calculate_average_values(0, 100) == 50
    assert create_record(count=6, group='ФЕП-32') == {'count': 6, 'group': 'ФЕП-32'}
    assert calculate_average.__name__ == 'calculate_average'
    assert calculate_average([{'average_grade': 0}]) == 0
    assert 'Час calculate_average:' in capsys.readouterr().out


def test_fresh_input():
    students = get_students()
    students[0]['average_grade'] = 0
    assert get_students()[0]['average_grade'] == 86.5
