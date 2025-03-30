from pydantic import BaseModel
from fastapi import Query

class Words(BaseModel):
    """
    Wrapper of list[str] that adds functionality to curate the input data.
    """
    data: list[str]

    def dedupe_consecutive(self) -> None:
        """
        Removes consecutive and identical occurrences to only keep one of them.
        For example:
        ["a", "a", "b", "b", "a"] → ["a", "b", "a"]
        """
        if not self.data:
            return

        deduped = [self.data[0]]
        for item in self.data[1:]:
            if item != deduped[-1]:
                deduped.append(item)
        self.data = deduped

    def simplify_repeating(self) -> None:
        """
        If the **entire** list is composed of **only** a repeating segment,
        replace it with that segment. Otherwise, leave the original list as it was.
        For example:
        ["a", "b", "a", "c", "a", "b", "a", "c"] → ["a", "b", "a", "c"]
        ["a", "b", "a", "b", "a", "b"] → ["a", "b"]
        ["a", "a", "b"] → ["a", "a", "b"] (unchanged)
        """
        n = len(self.data)

        if n <= 1:
            return 

        # Try possible pattern lengths from 1 up to half of the list length.
        for d in range(1, n // 2 + 1):
            if n % d == 0:  # A repeating unit must be a divisor of the total length.
                pattern = self.data[:d]
                if pattern * (n // d) == self.data:
                    self.data = pattern  # Found a repeating pattern; replace.
        return  # No repeating pattern found; keep original list.

def words_dependency(
    words: str = Query(...),
) -> Words:
    words = Words(
        data = words.split(','),
    )
    words.dedupe_consecutive()
    words.simplify_repeating()
    return words
