import pytest
import pixel_strings_state_setters
from pixel_strings_state_setters import make_single_colour_state_tuple, \
     make_multi_colour_state_tuple

@pytest.mark.parametrize("count,colour,result",[
(4, pixel_strings_state_setters.RED_RGB,
    [pixel_strings_state_setters.RED_RGB] * 4),
(5, (270, 1.0, 0.75),
    [(270, 1.0, 0.75)] * 5),
(6, pixel_strings_state_setters.YELLOW_HSV,
    [pixel_strings_state_setters.YELLOW_HSV] * 6),
])
def test_make_single_colour_state_tuple(count, colour, result):
    '''Given a count and a tuple which defines a colour, receive a list of that
    tuple that is count items long''' 
    got = make_single_colour_state_tuple(count, colour)
    assert got == result
 
@pytest.mark.parametrize("count,colour_list,result",[
(4, None,
    [pixel_strings_state_setters.RED_RGB,
     pixel_strings_state_setters.YELLOW_RGB,
     pixel_strings_state_setters.GREEN_RGB,
     pixel_strings_state_setters.BLUE_RGB]),
(12, None,
    [pixel_strings_state_setters.RED_RGB,
     pixel_strings_state_setters.YELLOW_RGB,
     pixel_strings_state_setters.GREEN_RGB,
     pixel_strings_state_setters.BLUE_RGB,
     pixel_strings_state_setters.PURPLE_RGB,
     pixel_strings_state_setters.ORANGE_RGB] * 2),
(6, [(270, 1.0, 0.75), pixel_strings_state_setters.BLUE_RGB,
     pixel_strings_state_setters.GREEN_RGB],
    [(270, 1.0, 0.75), pixel_strings_state_setters.BLUE_RGB,
     pixel_strings_state_setters.GREEN_RGB] * 2),
(6, [pixel_strings_state_setters.YELLOW_HSV],
    [pixel_strings_state_setters.YELLOW_HSV] * 6),
])
def test_make_multi_colour_state_tuple(count, colour_list, result):
    '''Given a count and a list of tuples which define colours,
    receive a list of that tuple that is count items long and cycles through
    the provided list of colours, or a default list of 6''' 
    got = make_multi_colour_state_tuple(count, colour_list)
    assert got == result
 
