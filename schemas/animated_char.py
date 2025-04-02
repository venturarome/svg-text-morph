from schemas.attribute import Attribute


class AnimatedChar:
    def __init__(self, char: str, id: str, attributes: list[Attribute] = None) -> None:
        self.char = char      # The character itself
        self.id = id          # Unique identifier for this character (e.g., "l1", "l2")
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