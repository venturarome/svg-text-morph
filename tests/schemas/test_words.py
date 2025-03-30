from schemas import Words

def test_dedupe_consecutive():
    # Repeated 2 times
    words = Words(data=["a", "a", "b", "a"])
    words.dedupe_consecutive()
    assert words.data == ["a", "b", "a"]

    # Repeated 3 times
    words = Words(data=["a", "b", "b", "b", "c", "a"])
    words.dedupe_consecutive()
    assert words.data == ["a", "b", "c", "a"]

    # Repeated 4 times
    words = Words(data=["x", "x", "x", "x"])
    words.dedupe_consecutive()
    assert words.data == ["x"]

    # No repetition
    words = Words(data=["a", "b", "c"])
    words.dedupe_consecutive()
    assert words.data == ["a", "b", "c"]

    # Empty data
    words = Words(data=[])
    words.dedupe_consecutive()
    assert words.data == []

def test_words_simplify_repeating():
    # Pattern not repeated
    words0 = Words(data = ["a", "b", "c"])
    words0.simplify_repeating()
    expected0 = ["a", "b", "c"]
    assert words0.data == expected0

    # Pattern repeated 2 times
    words1 = Words(data = ["a", "b", "a", "c", "a", "b", "a", "c"])
    words1.simplify_repeating()
    expected1 = ["a", "b", "a", "c"]
    assert words1.data == expected1

    # Pattern repeated 3 times
    words2 = Words(data = ["a", "b", "a", "b", "a", "b"])
    words2.simplify_repeating()
    expected2 = ["a", "b"]
    assert words2.data == expected2

    # Pattern repeated, but not over the whole list
    words3 = Words(data = ["a", "a", "b"])
    words3.simplify_repeating()
    expected3 = ["a", "a", "b"]
    assert words3.data == expected3