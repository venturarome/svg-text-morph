from services.configure_svg import nth_occurrence_index

def test_nth_occurrence_index():
    # Case 1: Regular case
    result = nth_occurrence_index("banana", "a", 2)
    assert result == 3, f"Expected 3, got {result}"

    # Case 2: First occurrence
    result = nth_occurrence_index("banana", "b", 1)
    assert result == 0, f"Expected 0, got {result}"

    # Case 3: Last occurrence
    result = nth_occurrence_index("banana", "a", 3)
    assert result == 5, f"Expected 5, got {result}"

    # Case 4: Character not present
    result = nth_occurrence_index("banana", "z", 1)
    assert result == -1, f"Expected -1, got {result}"

    # Case 5: Not enough occurrences
    result = nth_occurrence_index("banana", "n", 3)
    assert result == -1, f"Expected -1, got {result}"

    # Case 6: Input string is empty
    result = nth_occurrence_index("", "a", 1)
    assert result == -1, f"Expected -1, got {result}"

    # Case 7: Asking for 0-th occurrence (invalid input)
    result = nth_occurrence_index("banana", "a", 0)
    assert result == -1, f"Expected -1, got {result}"

    # Case 8: Case insensitivity check
    result = nth_occurrence_index("BanAna", "a", 2)
    assert result == 5, f"Expected 5, got {result}"  # 'a' at index 3

    print("All tests passed.")