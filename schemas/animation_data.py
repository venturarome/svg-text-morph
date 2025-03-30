from pydantic import BaseModel
from fastapi import Query

class AnimationData(BaseModel):
    """
        - font-family: we should only use monospaced fonts for easiness on positioning (Courier New, Roboto Mono, Consolas, Fira Mono, ...).
          For proportional fonts, we should use libraries such as PIL (PIL.ImageFont.truetype("myFont.ttf", mySize).getsize(myChar)).
        - font-size: determines the height of the characters. For monospaced fonts, we can approximate each character's width to 0.6 x font-size.
        - font-weight: Boldness or thinness: normal (400), bold (700). Varies between 100-900.
        - font-style: normal|italic|oblique|bold|... not all fonts have all styles.
    """
    show_time: int
    fade_time: int
    translation_time: int

    def word_animation_time(self) -> int:
        return self.show_time + 2 * self.fade_time + self.translation_time

def animation_data_dependency(
    show_time: int = Query(1000),
    fade_time: int = Query(1000),
    translation_time: int = Query(1000),
) -> AnimationData:
    return AnimationData(
        show_time=show_time,
        fade_time=fade_time,
        translation_time=translation_time,
    )
