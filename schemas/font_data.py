from pydantic import BaseModel
from fastapi import Query

class FontData(BaseModel):
    """
        - font-family: we should only use monospaced fonts for easiness on positioning (Courier New, Roboto Mono, Consolas, Fira Mono, ...).
          For proportional fonts, we should use libraries such as PIL (PIL.ImageFont.truetype("myFont.ttf", mySize).getsize(myChar)).
        - font-size: determines the height of the characters. For monospaced fonts, we can approximate each character's width to 0.6 x font-size.
        - font-weight: Boldness or thinness: normal (400), bold (700). Varies between 100-900.
        - font-style: normal|italic|oblique|bold|... not all fonts have all styles.
    """
    family: str
    size: int
    weight: int
    style: str

    def __str__(self) -> str:
        return f"font-family:{self.family};font-size:{self.size}px;font-weight:{self.weight};font-style:{self.style}"

    def char_height(self) -> int:
        return self.size
    
    def char_width(self) -> int:
        return int(0.6 * self.size)

def font_data_dependency(
    font_family: str = Query("Consolas, monospace"),    # TODO add enums and validators!
    font_size: int = Query(40),
    font_weight: int = Query(400),
    font_style: str = Query("normal"),
) -> FontData:
    return FontData(
        family=font_family,
        size=font_size,
        weight=font_weight,
        style=font_style,
    )
