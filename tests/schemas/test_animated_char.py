from schemas.animated_char import AnimatedChar

def test_animated_char_index_in():
    # Case 1: Regular case
    animated_char = AnimatedChar("a2")
    result = animated_char.index_in("banana")
    assert result == 3, f"Expected 3, got {result}"

    # Case 2: First occurrence
    animated_char = AnimatedChar("b1")
    result = animated_char.index_in("banana")
    assert result == 0, f"Expected 0, got {result}"

    # Case 3: Last occurrence
    animated_char = AnimatedChar("a3")
    result = animated_char.index_in("banana")
    assert result == 5, f"Expected 5, got {result}"

    # Case 4: Character not present
    animated_char = AnimatedChar("z1")
    result = animated_char.index_in("banana")
    assert result == -1, f"Expected -1, got {result}"

    # Case 5: Not enough occurrences
    animated_char = AnimatedChar("n3")
    result = animated_char.index_in("banana")
    assert result == -1, f"Expected -1, got {result}"

    # Case 6: Input string is empty
    animated_char = AnimatedChar("a2")
    result = animated_char.index_in("")
    assert result == -1, f"Expected -1, got {result}"

    # Case 7: Case insensitivity check
    animated_char = AnimatedChar("a2")
    result = animated_char.index_in("banAna")
    assert result == 5, f"Expected 5, got {result}"