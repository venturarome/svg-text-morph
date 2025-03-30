from pydantic import BaseModel
from fastapi import Query

class AnimationData(BaseModel):
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
