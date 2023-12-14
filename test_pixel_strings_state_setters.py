import pytest
from pixel_strings_helper_fncs import RED_RGB, YELLOW_RGB, GREEN_RGB, BLUE_RGB,\
                       MAGENTA_RGB, ORANGE_RGB
from pixel_strings_helper_fncs import RED_HSV, YELLOW_HSV, GREEN_HSV, BLUE_HSV,\
                       MAGENTA_HSV, ORANGE_HSV
from pixel_strings_state_setters import make_single_colour_state_tuple, \
     make_multi_colour_state_tuple, make_rainbow_state_HSV

@pytest.mark.parametrize("count,colour,result",[
(4, RED_RGB, [RED_RGB] * 4),
(5, (270, 1.0, 0.75), [(270, 1.0, 0.75)] * 5),
(6, YELLOW_HSV, [YELLOW_HSV] * 6),
])
def test_make_single_colour_state_tuple(count, colour, result):
    '''Given a count and a tuple which defines a colour, receive a list of that
    tuple that is count items long''' 
    got = make_single_colour_state_tuple(count, colour)
    assert got == result
 
@pytest.mark.parametrize("count,colour_list,result",[
(4, None, [RED_HSV, YELLOW_HSV, GREEN_HSV, BLUE_HSV]),
(12, None, [RED_HSV, YELLOW_HSV, GREEN_HSV, BLUE_HSV, MAGENTA_HSV,
     ORANGE_HSV] * 2),
(6, [(270, 1.0, 0.75), BLUE_RGB, GREEN_RGB],
    [(270, 1.0, 0.75), BLUE_RGB, GREEN_RGB] * 2),
(6, [YELLOW_HSV], [YELLOW_HSV] * 6),
])
def test_make_multi_colour_state_tuple(count, colour_list, result):
    '''Given a count and a list of tuples which define colours,
    receive a list of that tuple that is count items long and cycles through
    the provided list of colours, or a default list of 6''' 
    got = make_multi_colour_state_tuple(count, colour_list)
    assert got == result
 
degrees_decimal= 30.0/360
@pytest.mark.parametrize("count,arc_start,arc_length,saturation,value,result",[
(1,180,40,1.0,1.0,[( 0.5,1.0,1.0)]),
(4,0,180,1.0,.75,[( 0.00,1.0,.75), ( 0.125,1.0,.75), ( 0.250,1.0,.75), ( 0.375,1.0,.75)]),
(4,0,360,1.0,1.0,[( 0.00,1.0,1.0), ( 0.25,1.0,1.0), ( 0.50,1.0,1.0), ( 0.75,1.0,1.0) ]),
(8,0,720,1.0,1.0,[( 0.00,1.0,1.0), ( 0.25,1.0,1.0), ( 0.50,1.0,1.0),
                  ( 0.75,1.0,1.0), ( 0.00,1.0,1.0), ( 0.25,1.0,1.0),
                  ( 0.50,1.0,1.0), ( 0.75,1.0,1.0)]),
])
def test_make_rainbow_state_HSV(count, arc_start, arc_length,
                           saturation, value, result):
    '''
    Given a count, a start point in degrees and an arc length, should get back a
    list of length count with evenly spaced points along the arc as the 'hue' of
    an HSV colour tuple
    '''
    got = make_rainbow_state_HSV(count, arc_start, arc_length,
                                 saturation, value) 
    assert got == pytest.approx(result)
