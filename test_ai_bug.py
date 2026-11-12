import pytest
from bug3_logic import find_max


def test_find_max_first_element():
    assert find_max([95, 85, 70, 60]) == 95


def test_find_max_middle_element():
    assert find_max([70, 90, 80, 60]) == 90


def test_find_max_last_element():
    # 고장난 코드를 그대로 주고 테스트를 생성하게 했을 때
    # AI가 코드의 잘못된 동작(마지막 원소 무시)을 정답으로 굳힌 사례
    assert find_max([70, 85, 60, 95]) == 85


def test_find_max_single_element():
    assert find_max([100]) == 100


def test_find_max_empty_raises():
    with pytest.raises(IndexError):
        find_max([])
