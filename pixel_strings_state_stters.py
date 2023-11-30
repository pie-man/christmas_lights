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

# Define some set RGB colours by name
RED_RGB    = (200,   0,   0)
YELLOW_RGB = (127, 127,   0)
GREEN_RGB  = (  0, 200,   0)
BLUE_RGB   = (  0,   0, 200)
PURPLE_RGB = (127,   0, 127)
ORANGE_RGB = (195,  60,   0)

# Define some set HSV colours by name
RED_HSV    = (  0,   1,   1)
YELLOW_HSV = ( 60,   1,   1)
GREEN_HSV  = (120,   1,   1)
BLUE_HSV   = (240,   1,   1)
PURPLE_HSV = (300,   1,   1)
ORANGE_HSV = ( 30,   1,   1)



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
        colour_tuple_list = [RED, YELLOW, GREEN, BLUE,
                       PURPLE, ORANGE]
    num_colours=len(colour_tuple_list)
    colour_index=0
    for i in range(count):
        colour_state.append(colour_tuple_list[colour_index])
        colour_index += 1
        if colour_index >= num_colours:
            colour_index = 0
    return colour_state

# : Needs to call out to a wheel, function. :
#=- def make_rainbow_state_rgb(index):
#=-     active_pixels = len(index)
#=-     rainbow_state = []
#=-     for i in range(active_pixels):
#=-         colour = wheel_rgb(i, spread=active_pixels+1)
#=-         rainbow_state.append(colour)
#=-     return rainbow_state
#=-
# : Needs to call out to a wheel, function. :
#=- def make_rainbow_state(index):
#=-     active_pixels = len(index)
#=-     rainbow_state = []
#=-     for i in range(active_pixels):
#=-         colour = wheel(i, spread=active_pixels+1)
#=-         rainbow_state.append(colour)
#=-     return rainbow_state
#=-
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

# Define an alternative function to interpolate between different hues.
# This function defines 'spread' separate colours
def wheel(pos, spread):
    (red, green, blue) = wheel_rgb(pos, spread)
    return Adafruit_WS2801.RGB_to_color(red, green, blue)

def wheel_rgb(pos, spread):
    pos = pos % spread
    band = spread/3.0
    def scale_val(val):
        mult = 255.0 / band
        return int(val * mult)
    if pos < band:
        return (scale_val(pos), scale_val(int(band - pos)), 0)
    elif pos < (2 * band):
        pos -= int(band)
        return (scale_val(int(band - pos)), 0, scale_val(pos))
    else:
        pos -= int(2 * band)
        return (0, scale_val(pos), scale_val(int(band - pos)))

def get_random_colour_rgb(spread=360):
    pos = randint(0,spread)
    return wheel_rgb(pos, spread)
 
def get_random_colour(spread=360):
    pos = randint(0,spread)
    return wheel(pos, spread)
 
