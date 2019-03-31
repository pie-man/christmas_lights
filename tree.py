#!/usr/bin/env python
# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
import time
from datetime import datetime
import pixel_strings_fncs as q
from random import randint

# Configure the count of pixels:
PIXEL_COUNT = 50

# Logical to enable/disable flashing or rapidly changing sequences.
FLASHING=True

# Define the 'index' of the three rings of pixels to be ued globally
TOP    = range(25, 50)
MIDDLE = range(7, 24)
BOTTOM = range(7)

print_level=1
threshold=1

def set_rainbow_ring_fade(index):
    '''Set the lights  refered to by index to
       a full rainbow spread'''
    debug_print("enetered set_rainbow_ring_fade")
    state = q.make_rainbow_state_rgb(index)
    actor = (q.fade_to_state_rgb, index, state, False)
    return actor

def set_rainbows():
    '''Set the three rings of the tree to display a static
       loop of rainbow colours'''

    debug_print("enetered set_rainbows(): ")
    top_actor    = set_rainbow_ring_fade(TOP)
    middle_actor = set_rainbow_ring_fade(MIDDLE)
    bottom_actor = set_rainbow_ring_fade(BOTTOM)
    return (top_actor, middle_actor, bottom_actor)

def set_r_g_or_b_ring(index):
    '''Randomly set an index to one of red, green or blue'''
    debug_print("enetered set_r_g_or_b_ring")
    colours = [(200, 0, 0), (0, 200, 0), (0, 0, 200)]
    state = q.make_colour_state(index, colours[randint(0,len(colours)-1)])
    actor = (q.fade_to_state_rgb, index, state, False)
    return (actor)

def set_r_g_and_b_rings():
    '''Set the three rings of the tree to display static
       rings of red, green or blue'''
    debug_print("enetered set_r_g_and_b_rings")
    top_actor    = set_r_g_or_b_ring(TOP)
    middle_actor = set_r_g_or_b_ring(MIDDLE)
    bottom_actor = set_r_g_or_b_ring(BOTTOM)
    return (top_actor, middle_actor, bottom_actor)

def set_random_colour_ring(index):
    '''Set an index to a random colour'''
    debug_print("enetered set_random_colour_ring ")
    state = q.make_colour_state(index, q.get_random_colour_rgb())
    actor = (q.fade_to_state_rgb, index, state, False)
    return (actor)

def set_random_rings():
    '''Set the three rings of the tree to display static
       rings of random colours'''
    debug_print("enetered set_random_rings")
    top_actor    = set_random_colour_ring(TOP)
    middle_actor = set_random_colour_ring(MIDDLE)
    bottom_actor = set_random_colour_ring(BOTTOM)
    return (top_actor, middle_actor, bottom_actor)

def set_ring_to_black(index):
    '''Set an index to the go black'''
    debug_print("enetered set_ring_to_black ")
    dummy = "not required"
    actor = (q.fade_to_black, index, dummy, False)
    return (actor)

def set_to_black():
    '''fade all three rings to black'''
    debug_print("enetered set_to_black(): ")
    top_actor    = set_ring_to_black(TOP)
    middle_actor = set_ring_to_black(MIDDLE)
    bottom_actor = set_ring_to_black(BOTTOM)
    return (top_actor, middle_actor, bottom_actor)

def set_ring_to_dim(index):
    '''Set an index to the go almost black'''
    debug_print("enetered set_ring_to_dim ")
    actor    = (q.fade_to_color_rgb, index, (1,1,1), False)
    return (actor)

def set_to_dim():
    '''fade all three rings to black'''
    debug_print("enetered set_to_dim():")
    top_actor    = set_ring_to_dim(TOP)
    middle_actor = set_ring_to_dim(MIDDLE)
    bottom_actor = set_ring_to_dim(BOTTOM)
    return (top_actor, middle_actor, bottom_actor)

def set_ring_to_cycling_rainbow(index):
    '''Set an index to display a rainbow
       pattern and gently cycle it around the ring.
       Please only run this AFTER a set_rainbow_ring function'''
    debug_print("enetered set_ring_to_cycling_rainbow ")
    actor    = (q.rainbow_cycle, index, (256, 256, 2), False)
    return (actor)

def cycling_rainbows():
    '''Set the three rings of the tree to display a rainbow
       pattern and gently cycle it around the ring.
       Please only run this AFTER set_to_rainbows'''
    debug_print("enetered cycling_rainbows(): ")
    top_actor    = (q.rainbow_cycle, TOP   , (256, 256, 2), False)
    middle_actor = (q.rainbow_cycle, MIDDLE, (256, 256, 4), True)
    bottom_actor = (q.rainbow_cycle, BOTTOM, (256, 256, 6), False)
    return (top_actor, middle_actor, bottom_actor)

def set_rainbow_ring_successive(index):
    '''Set an index to display a rainbow pattern by successively
    illuminating sections of the ring.'''
    debug_print("enetered set_rainbow_ring_successive ")
    state = q.make_rainbow_state_rgb(index)
    actor = (q.light_up_successive_rgb, index, state, False)
    return (actor)

def set_successive_rainbows():
    '''Set the three rings of the tree to display a rainbow
    pattern by successively illuminating sections of the rings.'''
    debug_print("enetered cycling_rainbows(): ")
    top_actor    = set_rainbow_ring_successive(TOP)
    middle_actor = set_rainbow_ring_successive(MIDDLE)
    bottom_actor = set_rainbow_ring_successive(BOTTOM)
    return (top_actor, middle_actor, bottom_actor)

def set_right_random_wibblefest():
    '''Selects 3 funtions randomly and assigns one to each ring'''
    debug_print("enetered set_right_random_wibblefest(): ")
    list_of_functions = [
            set_rainbow_ring_fade,
            set_r_g_or_b_ring,
            set_ring_to_cycling_rainbow,
            set_random_colour_ring,
            set_ring_to_cycling_rainbow,
            set_rainbow_ring_successive,
            ]
    selection = randint(0, len(list_of_functions)-1 )
    top_actor    = list_of_functions[selection](TOP)
    selection = randint(0, len(list_of_functions)-1 )
    middle_actor = list_of_functions[selection](MIDDLE)
    selection = randint(0, len(list_of_functions)-1 )
    bottom_actor = list_of_functions[selection](BOTTOM)
    return (top_actor, middle_actor, bottom_actor)

def debug_print(text):
    '''Check print level and print messages if threshold metdef '''
    if print_level >= threshold:
        print(text)

if __name__ == '__main__':
    pixels = q.initialise_pixels(PIXEL_COUNT)
    function_list = [
            set_random_rings,
            set_r_g_and_b_rings,
            set_rainbows,
            cycling_rainbows,
            set_to_dim,
            set_random_rings,
            set_to_dim,
            set_random_rings,
            set_to_dim,
            set_successive_rainbows,
            set_right_random_wibblefest,
            set_right_random_wibblefest,
            set_right_random_wibblefest,
            set_rainbows,
            cycling_rainbows,
            set_to_dim,
            ]

    count=len(function_list)-1
    #for function in function_list:
    while datetime.now().hour > 16:
        count=count+1
        if count >= len(function_list):
            count=0
        function = function_list[count]
        (top_actor, middle_actor, bottom_actor) = function()
        stepcount = 180
        cluster = q.bundle(pixels, wait=0.2, steps=stepcount)
        cluster.add_function(top_actor[0], top_actor[1], attribute=top_actor[2],
                             reverse=top_actor[3])
        cluster.add_function(middle_actor[0], middle_actor[1],
                             attribute=middle_actor[2],
                             reverse=middle_actor[3])
        cluster.add_function(bottom_actor[0], bottom_actor[1],
                             attribute=bottom_actor[2],
                             reverse=bottom_actor[3])
        #print("Running a function... at {0}".format(datetime.now()))
        cluster.run_bundle()

    # Shut it all down quietly...
    #print("closing down... at {0}".format(datetime.now()))
    (top_actor, middle_actor, bottom_actor) = set_to_black()
    stepcount = 120
    cluster = q.bundle(pixels, wait=0.5, steps=stepcount)
    cluster.add_function(top_actor[0], top_actor[1],
                         attribute=top_actor[2], reverse=top_actor[3])
    cluster.add_function(middle_actor[0], middle_actor[1],
                         attribute=middle_actor[2], reverse=middle_actor[3])
    cluster.add_function(bottom_actor[0], bottom_actor[1],
                         attribute=bottom_actor[2], reverse=bottom_actor[3])
    cluster.run_bundle()
