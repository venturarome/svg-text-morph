from schemas.state import State


class Attribute:
    """
    Contains the name of an attribute (like “opacity” or “x”) and a list of its states.
    """
    def __init__(self, name: str, states: list[State] = None) -> None:
        self.name = name      # The name of the attribute (e.g., "opacity", "x", etc.)
        self.states = states if states is not None else []

    def __repr__(self) -> str:
        return f"Attribute(name='{self.name}', states={self.states})"
    
    def add_state(self, state: State) -> None:
        for existing_state in self.states:
            if existing_state.time == state.time and existing_state.value == state.value:
                return  # Duplicated state, do nothing
        self.states.append(state)
        
        # Sort the states by time after each insertion.
        self.states.sort(key=lambda s: s.time)

    def format_values(self) -> str:
        #TODO implement self.simplify() to remove redundant states
        return ";".join(str(state.value) for state in self.states)

    def format_key_times(self, duration: int) -> str:
        return ";".join(str(state.to_relative_time(duration)) for state in self.states)

# TODO extend into 2 classes: AttributeX and AttributeOpacity.