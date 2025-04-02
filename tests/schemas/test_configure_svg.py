from services.configure_svg import inner_join, left_join, right_join

def test_inner_join():
    # Normal case
    assert inner_join(["a1", "b1", "c1"], ["b1", "c1", "d1"]) == ["b1", "c1"]

    # First empty
    assert inner_join([], ["a1"]) == []

    # Second empty
    assert inner_join(["a1"], []) == []

    # Both empty
    assert inner_join([], []) == []

    # Different order
    assert inner_join(["a1", "a2"], ["a2", "a1"]) == ["a1", "a2"]

def test_left_join():
    # Normal case
    assert left_join(["a1", "b1", "c1"], ["b1", "d1"]) == ["a1", "c1"]

    # First empty
    assert left_join([], ["a1"]) == []

    # Second empty
    assert left_join(["a1"], []) == ["a1"]

    # Both empty
    assert left_join([], []) == []
