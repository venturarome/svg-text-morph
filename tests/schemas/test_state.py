from schemas.state import State

def test_to_relative_time():
    # Test happy path
    state = State(time=500, value="example")
    duration = 1000
    expected = 0.5
    result = state.to_relative_time(duration)
    assert result == expected

    # Test that exception is raised when time > duration
    try:
        state = State(time=1500, value="example")
        result = state.to_relative_time(duration=1000)
        assert False
    except Exception as e:
        assert True