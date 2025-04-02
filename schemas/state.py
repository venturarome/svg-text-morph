class State:
    """
    Holds a time (using an int to represent milliseconds)
    and the corresponding value as a string.
    """
    def __init__(self, time: float, value: str) -> None:
        self.time = time      # The absolute time for this state
        self.value = value    # The attribute value at that time

    def __repr__(self) -> str:
        return f"State(time={self.time}, value='{self.value}')"

    def to_relative_time(self, duration: int) -> float:
        if self.time > duration:
            raise "State time bigger than animation duration"
        return self.time/duration