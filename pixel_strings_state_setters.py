'''
Some routines to set a 'state'. A state being a list of colours.
Potentially colours can be a tuple for red, blue and green (in various orders)
or a tuple for Hue, Saturarion and Value
or a 'hex' value (and possibly other scalar values to store the colour)

It may be that the 'state' should also the indecies of the pixels being set, but
this may get complicated as previously 'actors' which animate lights accept
'states' and apply them to subsections of the string. So somewhere along the
line an 'offset' needs to be used to allow mapping betweeen a 'local' index and
the global one.
'''

from pixel_strings_helper_fncs import RED_RGB, YELLOW_RGB, GREEN_RGB, BLUE_RGB,\
                       MAGENTA_RGB, ORANGE_RGB

def make_single_colour_state_tuple(count, colour_tuple):
    '''Takes a count and a tuple defining an RGB or HSV colour.
    Returns a list, of length count, of the colour tuples''' 
    colour_state = []
    for i in range(count):
        colour_state.append(colour_tuple)
    return colour_state

def make_multi_colour_state_tuple(count, colour_tuple_list=None):
    '''Takes a count and a list of RGB/HSV colour tuples.
    Returns a list, of length count, of colour tuples formed
    by cycling through the list of colour tuples provided.'''
    colour_state = []
    if colour_tuple_list is None:
        colour_tuple_list = [RED_RGB, YELLOW_RGB, GREEN_RGB, BLUE_RGB,
                       MAGENTA_RGB, ORANGE_RGB]
    num_colours=len(colour_tuple_list)
    colour_index=0
    for i in range(count):
        colour_state.append(colour_tuple_list[colour_index])
        colour_index += 1
        if colour_index >= num_colours:
            colour_index = 0
    return colour_state

def make_rainbow_state_HSV(count, arc_start=0, arc_length=360,
                           saturation=1.0, value=1.0):
    '''
       Creates a list of 'count' HSV colour tuples spread evenly along an 'arc'
       of length 'arc_length' degrees (could be 720 for 2 full rainbows)
       starting from point 'arc_start'.
       saturation and value default to 1 and are just passed through and used in
       the returned tuples. Set value to a lower decimal, e.g. 0.75, to reduce
       the brightness of the string.
    '''
    rainbow_state = []
    arc_increments = arc_length / count
    for pixel in range(count):
        hue = ((pixel * arc_increments) + arc_start) % 360
        rainbow_state.append((hue, saturation, value))
    return rainbow_state

# : This block could be methods in a 'state' object
# : which also stores the current 'state' as the plasma lights don't wheras the
# : Adafruit library for WS2801 s did.
#: def get_state(pixels, index):
#:     active_pixels = len(index)
#:     current_state = []
#:     for i in range(active_pixels):
#:         current_state.append(pixels.get_pixel(index[i]))
#:     return current_state
#: 
#: def get_state_rgb(pixels, index):
#:     active_pixels = len(index)
#:     current_state = []
#:     for i in range(active_pixels):
#:         current_state.append(pixels.get_pixel_rgb(index[i]))
#:     return current_state
#: 
#: def set_state_rgb(pixels, index, rgb_state):
#:     active_pixels = len(index)
#:     if active_pixels != len(rgb_state):
#:         print("Error in set_state_rgb : Length of states not consistent")
#:     for i in range(active_pixels):
#:         red_val, green_val, blue_val = rgb_state[i]
#:         pixels.set_pixel(index[i],
#:                 Adafruit_WS2801.RGB_to_color( red_val, green_val, blue_val ))
#: 
#: def set_state(pixels, index, state):
#:     active_pixels = len(index)
#:     if active_pixels != len(state):
#:         print("Error in set_state : Length of states not consistent")
#:     for i in range(active_pixels):
#:         pixels.set_pixel(index[i],state[i])
#=-

