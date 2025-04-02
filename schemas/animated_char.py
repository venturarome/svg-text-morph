from schemas.attribute import Attribute


class AnimatedChar:
    def __init__(self, id: str, attributes: list[Attribute] = None) -> None:
        self.id = id            # Unique identifier for this character (e.g., "l1", "l2")
        self.char = id[:1]      # The character itself
        self.rel_pos = int(id[1:])   # The overall relative position among same characters
        # If attributes is not provided, initialize with an empty list.
        self.attributes = attributes if attributes is not None else []

    def __repr__(self) -> str:
        return f"AnimatedChar(char='{self.char}', id='{self.id}', attributes={self.attributes})"
    
    def add_attribute(self, attribute: Attribute) -> None:
        # Only add the attribute if one with the same name does not already exist.
        if not any(attr.name == attribute.name for attr in self.attributes):
            self.attributes.append(attribute)

    def id_as_ref(self) -> str:
        return '#' + self.id
    
    def attribute_by_name(self, attribute_name: str) -> Attribute:
        """Returns the attribute of the provided name"""
        for attribute in self.attributes:
            if attribute.name == attribute_name:
                return attribute
        raise ValueError(f"Attribute '{attribute_name}' not found in AnimatedChar with id '{self.id}'")

    def index_in(self, word: str) -> int:
        """
        Returns the index of self in the input string.
        Returns -1 if not found.
        """
        count = 0
        for index, c in enumerate(word):
            if c == self.char:
                count += 1
                if count == self.rel_pos:
                    return index
        return -1