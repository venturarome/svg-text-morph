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
                }
            }
            print(transition_config)
            transitions.append(transition_config)
            elapsed_time = t_fade_in + self.animation.fade_time

        # Create a set with all the "animated chars"
        # Note: we could have embedded this in the transitions calculation, but this is cleaner.
        animated_chars: list[AnimatedChar] = []
        for word in self.words.data:
            for char_id in number_chars(word):
                if all(existing_char.id != char_id for existing_char in animated_chars):
                    animated_chars.append(AnimatedChar(char_id))

        # Fill each animated char with animations
        for animated_char in animated_chars:
            attribute_opacity = Attribute("opacity")
            attribute_x = Attribute("x")

            for transition in transitions:
                # Steps that a char can follow in a transition:
                #   - only appears in 1sr word  ==> show + fade_out   
                #   - appears in both words     ==> show + translate
                #   - only appears in 2nd word  ==> fade_in
                #   - don't appear in any word  ==> <none>

                # 1. SHOW:
                t_show_start = transition["start_times"]["hold"]
                t_show_end = t_show_start + self.animation.show_time
                # Opacity
                opacity_value = "1" if animated_char.id in transition["show_chars"] else "0"
                attribute_opacity.add_state(State(t_show_start, opacity_value))
                attribute_opacity.add_state(State(t_show_end, opacity_value))
                # Position
                pos_start = max(self.font.char_width() * animated_char.index_in(transition["current_word"]), 0)
                attribute_x.add_state(State(t_show_start, pos_start))
                attribute_x.add_state(State(t_show_end, pos_start))

                # 2. FADE-OUT:
                t_fade_out_start = transition["start_times"]["fade_out"]
                t_fade_out_end = t_fade_out_start + self.animation.fade_time
                # Opacity
                if animated_char.id in transition["fade_out_chars"]:
                    attribute_opacity.add_state(State(t_fade_out_start, "1"))
                    attribute_opacity.add_state(State(t_fade_out_end, "0"))
                # Position
                attribute_x.add_state(State(t_fade_out_start, pos_start))
                attribute_x.add_state(State(t_fade_out_end, pos_start))

                # 3. TRANSLATE:
                # Opacity -> none
                # Position
                if animated_char.id in transition["translate_chars"]:
                    t_translate_start = transition["start_times"]["translate"]
                    t_translate_end = t_translate_start + self.animation.translation_time
                    pos_end = max(self.font.char_width() * animated_char.index_in(transition["next_word"]), 0)
                    attribute_x.add_state(State(t_translate_start, pos_start))
                    attribute_x.add_state(State(t_translate_end, pos_end))

                # 4. FADE-IN:
                t_fade_in_start =  transition["start_times"]["fade_in"]
                t_fade_in_end =  t_fade_in_start + self.animation.fade_time
                # Opacity
                if animated_char.id in transition["fade_in_chars"]:
                    attribute_opacity.add_state(State(t_fade_in_start, "0"))
                    attribute_opacity.add_state(State(t_fade_in_end, "1"))
                elif animated_char.id in transition["translate_chars"]:
                    attribute_opacity.add_state(State(t_fade_in_end, "1"))
                else: # fade_out or none
                    attribute_opacity.add_state(State(t_fade_in_end, "0"))
                # Position
                pos_start = max(self.font.char_width() * animated_char.index_in(transition["next_word"]), 0)
                if animated_char.id in transition["fade_in_chars"]:
                    attribute_x.add_state(State(t_fade_in_start, pos_start))
                attribute_x.add_state(State(t_fade_in_end, pos_start))

            animated_char.add_attribute(attribute_opacity)
            animated_char.add_attribute(attribute_x)


        # Create the SVG object:
        box_height = self.font.char_height()
        box_width = self.font.char_width() * self.words.max_len()
        
        dwg = svgwrite.Drawing('animation.svg')
        dwg.attribs['viewBox'] = f"0 0 {box_width+100} {box_height+100}"
        dwg.attribs['width'] = str(box_width+100)
        dwg.attribs['height'] = str(box_height+100)

        # Add text element with individual tspans
        text = dwg.text('', style = str(self.font), dominant_baseline='hanging')
        for animated_char in animated_chars:
            text.add(dwg.tspan(animated_char.char, id=animated_char.id))
        dwg.add(text)

        for animated_char in animated_chars:
            for attribute in animated_char.attributes:
                dwg.add(dwg.animate(
                    href = animated_char.id_as_ref(),
                    attributeName = attribute.name,
                    values = attribute.format_values(),
                    keyTimes = attribute.format_key_times(elapsed_time),
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
    return left_join(l2, l1)