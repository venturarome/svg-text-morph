from fastapi import Response
from schemas import AnimationData, FontData, Words
from schemas.animated_char import AnimatedChar
from schemas.attribute import Attribute
from schemas.state import State
import svgwrite

class ConfigureSvg():
    def __init__(self, words: Words, font: FontData, animation: AnimationData):
        self.words = words
        self.font = font
        self.animation = animation

    

    def generate(self) -> str:
        # Create Transitions (one for each consecutive pair)
        transitions = []

        # Loop over each word, and treat the next word (with wrap-around) as the target.
        num_words = len(self.words.data)
        elapsed_time = 0
        for i in range(num_words):
            current_word = self.words.data[i]
            next_word = self.words.data[(i + 1) % num_words]  # Wrap around for the last word

            # Get the numbered characters for both words.
            current_chars = number_chars(current_word)
            next_chars = number_chars(next_word)
            
            transition_config = {
                "current_word": current_word,
                "next_word": next_word,
                "show_chars": current_chars,
                "translate_chars": inner_join(current_chars, next_chars),
                "fade_out_chars": left_join(current_chars, next_chars),
                "fade_in_chars": right_join(current_chars, next_chars),
                "start_times": {
                    "hold": (t_hold := elapsed_time),
                    "fade_out": (t_fade_out := t_hold + self.animation.show_time),
                    "translate": (t_translate := t_fade_out + self.animation.fade_time),
                    "fade_in": (t_fade_in := t_translate + self.animation.translation_time),
                    #"total": T_show + T_translate + 2 * T_fade,
                }
            }
            transitions.append(transition_config)
            elapsed_time = t_fade_in + self.animation.fade_time

        # Create a set with all the char_ids (the char + a number)
        # Note: we could have embedded this in the transitions calculation, but this is cleaner.
        
        char_ids = set()
        for word in self.words.data:
            word_char_ids = number_chars(word)
            char_ids |= word_char_ids

        # Iterate over each char and create an animated_char_list
        animated_char_list = []
        for char_id in char_ids:
            attribute_opacity = Attribute("opacity")
            attribute_x = Attribute("x")

            for transition in transitions:
                # Steps that a char can follow in a transition:
                #   - only appears in 1sr word  ==> show + fade_out   
                #   - appears in both words     ==> show + translate
                #   - only appears in 2nd word  ==> fade_in
                #   - don't appear in any word  ==> <none>

                if char_id in transition["show_chars"]:
                    t_show_start = transition["start_times"]["hold"]
                    t_show_end = t_show_start + self.animation.show_time
                    attribute_opacity.add_state(State(t_show_start, "1"))
                    attribute_opacity.add_state(State(t_show_end, "1"))

                    pos_start = self.font.char_width() * nth_occurrence_index(transition["current_word"], char_id[:1], int(char_id[1:]))
                    attribute_x.add_state(State(t_show_start, pos_start))
                    attribute_x.add_state(State(t_show_end, pos_start))
                    
                    if char_id in transition["fade_out_chars"]:
                        t_fade_out_start = transition["start_times"]["fade_out"]
                        t_fade_out_end = t_fade_out_start + self.animation.fade_time
                        attribute_opacity.add_state(State(t_fade_out_start, "1"))
                        attribute_opacity.add_state(State(t_fade_out_end, "0"))

                        attribute_x.add_state(State(t_fade_out_start, pos_start))
                        attribute_x.add_state(State(t_fade_out_end, pos_start))

                    else:   # char_id in transition["translate_chars"]
                        t_translate_start = transition["start_times"]["translate"]
                        t_translate_end = t_translate_start + self.animation.translation_time
                        pos_start = self.font.char_width() * nth_occurrence_index(transition["current_word"], char_id[:1], int(char_id[1:]))
                        pos_end = self.font.char_width() * nth_occurrence_index(transition["next_word"], char_id[:1], int(char_id[1:]))
                        attribute_x.add_state(State(t_translate_start, pos_start))
                        attribute_x.add_state(State(t_translate_end, pos_end))

                else:
                    t_show_start = transition["start_times"]["hold"]
                    t_show_end = t_show_start + self.animation.show_time
                    attribute_opacity.add_state(State(t_show_start, "0"))
                    attribute_opacity.add_state(State(t_show_end, "0"))

                    if char_id in transition["fade_in_chars"]:
                        t_fade_in_start =  transition["start_times"]["fade_in"]
                        t_fade_in_end =  t_fade_in_start + self.animation.fade_time
                        attribute_opacity.add_state(State(t_fade_in_start, "0"))
                        attribute_opacity.add_state(State(t_fade_in_end, "1"))

                        pos_start = self.font.char_width() * nth_occurrence_index(transition["next_word"], char_id[:1], int(char_id[1:]))
                        attribute_x.add_state(State(t_fade_in_start, pos_start))
                        attribute_x.add_state(State(t_fade_in_end, pos_start))

            animated_char_list.append(AnimatedChar(char_id[:1], char_id, [attribute_opacity, attribute_x]))


        # Create the SVG object:
        # Esto es todo lo que irá dentro de SvgConfig
        box_height = self.font.char_height()
        box_width = self.font.char_width() * self.words.max_len()
        # dwg = svgwrite.Drawing('animation.svg', size=(f"{box_height}px", f"{10 * box_width}px"))
        # dwg = svgwrite.Drawing('animation.svg' width = str(box_width), height=str(box_height))
        dwg = svgwrite.Drawing('animation.svg')
        dwg.attribs['viewBox'] = f"0 0 {box_width} {box_height}"
        dwg.attribs['width'] = str(box_width)
        dwg.attribs['height'] = str(box_height)

        # Add text element with individual tspans
        text = dwg.text('', style = str(self.font), y = "0", dominant_baseline='hanging')
        for animated_char in animated_char_list:
            initial_x_pos = nth_occurrence_index(self.words.data[0], animated_char.char, int(animated_char.id[1:]))
            if initial_x_pos != -1:
                text.add(dwg.tspan(animated_char.char, id=animated_char.id, x=str(self.font.char_width() * initial_x_pos)))
            else:
                text.add(dwg.tspan(animated_char.char, id=animated_char.id))
        dwg.add(text)

        for animated_char in animated_char_list:
            for attribute in animated_char.attributes:
                dwg.add(dwg.animate(
                    href = animated_char.id_as_ref(),
                    attributeName = attribute.name,
                    values = attribute.format_values(),
                    keyTimes = attribute.format_key_times(elapsed_time),    # TODO check that initial (0) and final (1) are always added.
                    dur = f"{elapsed_time}ms",
                    repeatCount = "indefinite"
                ))

        return dwg.tostring()


def number_chars(word: str) -> set[str]:
    """
    Given a word, returns a list of its characters, each postfixed with a count indicating
    its occurrence order.
    
    Example:
    "banana" → ["b1", "a1", "n1", "a2", "n2", "a3"]
    """
    counts = {}
    result = set()
    for char in word:
        counts[char] = counts.get(char, 0) + 1
        result.add(f"{char}{counts[char]}")
    return result

def inner_join(l1: list[str], l2: list[str]) -> list[str]:
    """
    Returns a list containing the common elements to both lists
    """
    return [elem for elem in l1 if elem in l2]


def left_join(l1: list[str], l2: list[str]) -> list[str]:
    """
    Returns a list containing the elements found in left list but not in right list
    """
    return [elem for elem in l1 if elem not in l2]

def right_join(l1: list[str], l2: list[str]) -> list[str]:
    """
    Returns a list containing the elements found in right list but not in left list
    """
    return [elem for elem in l2 if elem not in l1]

def nth_occurrence_index(s: str, char: str, n: int) -> int:
    """
    Returns the index of the n-th occurrence of 'char' in 's'.
    Returns -1 if 'char' doesn't occur n times.
    """
    count = 0
    for index, c in enumerate(s):
        if c == char:
            count += 1
            if count == n:
                return index
    return -1

def have_common_char(s1: str, s2: str) -> bool:
    set1 = set(c for c in s1 if not c.isspace())
    set2 = set(c for c in s2 if not c.isspace())
    return not set1.isdisjoint(set2)