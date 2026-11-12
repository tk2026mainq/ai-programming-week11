import pytest
from load_scores import load_scores


def test_spec_normal_and_homonyms(tmp_path):
    p = tmp_path / "scores.csv"
    p.write_text("name,score\n김하나,85\n김하나,95\n이두리,70\n", encoding="utf-8")
    kept, skipped = load_scores(str(p))
    assert kept == [("김하나", 85), ("김하나", 95), ("이두리", 70)]
    assert skipped == []


def test_spec_missing_file():
    with pytest.raises(FileNotFoundError):
        load_scores("missing.csv")


def test_spec_empty_header_only(tmp_path):
    p = tmp_path / "empty.csv"
    p.write_text("name,score\n", encoding="utf-8")
    kept, skipped = load_scores(str(p))
    assert kept == []
    assert skipped == []


@pytest.mark.parametrize("score,is_valid", [
    (-1, False),
    (0, True),
    (100, True),
    (101, False),
])
def test_spec_boundary_values(tmp_path, score, is_valid):
    p = tmp_path / "boundary.csv"
    p.write_text(f"name,score\n학생,{score}\n", encoding="utf-8")
    kept, skipped = load_scores(str(p))
    if is_valid:
        assert kept == [("학생", score)]
        assert skipped == []
    else:
        assert kept == []
        assert len(skipped) == 1
        assert skipped[0][0] == 2


def test_spec_skipped_records_and_blank_lines(tmp_path):
    p = tmp_path / "mixed.csv"
    p.write_text("name,score\n\n,80\n홍길동,\n이순신,결석\n강감찬,90,추가열\n", encoding="utf-8")
    kept, skipped = load_scores(str(p))
    assert kept == []
    assert [item[0] for item in skipped] == [3, 4, 5, 6]
