import pytest
from load_scores import load_scores


def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5
    assert len(skipped) == 5


def test_빈_줄은_건너뛴다(tmp_path):
    csv_file = tmp_path / "blank.csv"
    csv_file.write_text("name,score\n김하나,88\n\n이두리,92\n", encoding="utf-8")
    kept, skipped = load_scores(str(csv_file))
    assert kept == [("김하나", 88), ("이두리", 92)]
    assert skipped == []


def test_이름에_쉼표가_있어도_읽는다():
    kept, _ = load_scores("scores.csv")
    assert ("최,네번", 77) in kept


def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")


def test_헤더만_있으면_빈_결과():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []


@pytest.mark.parametrize("점수, 유효한가", [
    (-1, False),
    (0, True),
    (1, True),
    (99, True),
    (100, True),
    (101, False),
])
def test_점수_경계값(tmp_path, 점수, 유효한가):
    csv_file = tmp_path / "boundary.csv"
    csv_file.write_text(f"name,score\n홍길동,{점수}\n", encoding="utf-8")
    kept, skipped = load_scores(str(csv_file))
    assert (len(kept) == 1) == 유효한가
    assert (len(skipped) == 0) == 유효한가


def test_이름이_비어_있으면_건너뛴다(tmp_path):
    csv_file = tmp_path / "no_name.csv"
    csv_file.write_text("name,score\n,90\n박세찬,\n", encoding="utf-8")
    kept, skipped = load_scores(str(csv_file))
    assert kept == []
    assert len(skipped) == 2
