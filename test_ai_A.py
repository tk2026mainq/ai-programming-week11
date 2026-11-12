import pytest
from load_scores import load_scores


def test_valid_and_duplicate_names(tmp_path):
    p = tmp_path / "valid.csv"
    p.write_text('name,score\n김하나,88\n"최,네번",77\n김하나,91\n\n', encoding="utf-8")
    kept, skipped = load_scores(str(p))
    assert kept == [("김하나", 88), ("최,네번", 77), ("김하나", 91)]
    assert skipped == []


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_scores("non_existent_file.csv")


def test_header_only(tmp_path):
    p = tmp_path / "empty.csv"
    p.write_text("name,score\n", encoding="utf-8")
    assert load_scores(str(p)) == ([], [])


@pytest.mark.parametrize("score,expected_kept", [
    (0, 1),
    (100, 1),
    (-1, 0),
    (101, 0),
])
def test_score_boundaries(tmp_path, score, expected_kept):
    p = tmp_path / "bound.csv"
    p.write_text(f"name,score\n테스터,{score}\n", encoding="utf-8")
    kept, skipped = load_scores(str(p))
    assert len(kept) == expected_kept
    assert len(skipped) == (1 - expected_kept)


def test_invalid_rows_reasons(tmp_path):
    p = tmp_path / "invalid.csv"
    p.write_text(
        "name,score\n"
        "장미르,72,비고\n"
        ",90\n"
        "박세찬,\n"
        "한겨울,결석\n"
        "이두리,105\n",
        encoding="utf-8",
    )
    kept, skipped = load_scores(str(p))
    assert kept == []
    reasons = [r[2] for r in skipped]
    assert reasons == [
        "열 개수가 2가 아님",
        "이름이 비어 있음",
        "점수가 비어 있음",
        "점수가 정수가 아님",
        "점수가 0~100 밖",
    ]
