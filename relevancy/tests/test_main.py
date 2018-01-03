from relevancy.main import calculate_relevancy
import logging

logging.basicConfig(level=logging.INFO)


def test_calculate_relevancy_empty_value():
    assert calculate_relevancy([1, 3, 4], [])[0] == 0
    assert calculate_relevancy([], [1, 3, 4])[0] == 0


def test_calculate_relevancy():
    assert calculate_relevancy([1, 3, 4], [1, 3, 4])[0] == 1.0


def test_calculate_relevancy_with_difference():
    relevancy1 = calculate_relevancy([1, 3, 4], [1, 4, 3])
    assert relevancy1[0] < 1.0


def test_calculate_relevancy_with_shuffle():
    relevancy1 = calculate_relevancy([1, 3, 4], [1, 4, 3])
    assert relevancy1[0] < 1.0


def test_calculate_relevancy_ignore_omission():
    relevancy1 = calculate_relevancy([1, 3, 4], [1, 4, 3])
    relevancy2 = calculate_relevancy([1, 3, 4], [1, 9, 3])
    assert relevancy1[0] < 1.0
    assert relevancy2[0] < relevancy1[0]
