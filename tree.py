#!/usr/bin/env python
# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
import time
from datetime import datetime
import pixel_strings_fncs as q
from random import randint

# Configure the count of pixels:
PIXEL_COUNT = 46

# Define the 'index' of the three rings of pixels to be ued globally
TOP    = range(37, 46)
MIDDLE = range(22, 33)
BOTTOM = range(18)

def set_rainbows():
    '''Set the three rings of the tree to display a static
       loop of rainbow colours'''

    top_state = q.make_rainbow_state_rgb(TOP)
    middle_state = q.make_rainbow_state_rgb(MIDDLE)
    bottom_state = q.make_rainbow_state_rgb(BOTTOM)
    top_actor    = (q.fade_to_state_rgb, TOP, top_state, False)
    middle_actor = (q.fade_to_state_rgb, MIDDLE, middle_state, True)
    bottom_actor = (q.fade_to_state_rgb, BOTTOM, bottom_state, False)
    #return (top_state, middle_state, bottom_state)
    return (top_actor, middle_actor, bottom_actor)

def set_r_g_and_b_rings():
    '''Set the three rings of the tree to display static
       rings of red, green or blue'''
    colours = [(200, 0, 0), (0, 200, 0), (0, 0, 200)]
    top_state = q.make_colour_state(TOP, colours[randint(0,2)])
    middle_state = q.make_colour_state(MIDDLE, colours[randint(0,2)])
    bottom_state = q.make_colour_state(BOTTOM, colours[randint(0,2)])
    top_actor    = (q.fade_to_state_rgb, TOP, top_state, False)
    middle_actor = (q.fade_to_state_rgb, MIDDLE, middle_state, False)
    bottom_actor = (q.fade_to_state_rgb, BOTTOM, bottom_state, False)
    #return (top_state, middle_state, bottom_state)
    return (top_actor, middle_actor, bottom_actor)

def set_random_rings():
    '''Set the three rings of the tree to display static
       rings of random colours'''
    top_state = q.make_colour_state(TOP, q.get_random_colour_rgb())
    middle_state = q.make_colour_state(MIDDLE, q.get_random_colour_rgb())
    bottom_state = q.make_colour_state(BOTTOM, q.get_random_colour_rgb())
    top_actor    = (q.fade_to_state_rgb, TOP, top_state, False)
    middle_actor = (q.fade_to_state_rgb, MIDDLE, middle_state, False)
    bottom_actor = (q.fade_to_state_rgb, BOTTOM, bottom_state, False)
    #return (top_state, middle_state, bottom_state)
    return (top_actor, middle_actor, bottom_actor)

def set_to_black():
    '''fade all three rings to black'''
    dummy = "not required"
    top_actor    = (q.fade_to_black, TOP, dummy, False)
    middle_actor = (q.fade_to_black, MIDDLE, dummy, False)
    bottom_actor = (q.fade_to_black, BOTTOM, dummy, False)
    #return (top_state, middle_state, bottom_state)
    return (top_actor, middle_actor, bottom_actor)

def cycling_rainbows():
    '''Set the three rings of the tree to display a rainbow
       pattern and gently cycle it around the ring.
       Please only run this AFTER set_to_rainbows'''
    top_actor    = (q.rainbow_cycle_II, TOP   , (256, 256, 2), False)
    middle_actor = (q.rainbow_cycle_II, MIDDLE, (256, 256, 4), True)
    bottom_actor = (q.rainbow_cycle_II, BOTTOM, (256, 256, 6), False)
    return (top_actor, middle_actor, bottom_actor)

if __name__ == '__main__':
    pixels = q.initialise_pixels(PIXEL_COUNT)
    function_list = [
            set_random_rings,
            set_r_g_and_b_rings,
            set_rainbows,
            cycling_rainbows,
            set_to_black,
            set_random_rings,
            set_to_black,
            set_random_rings,
            set_to_black,
            ]

    count=len(function_list)-1
    #for function in function_list:
    while datetime.now().hour < 18:
        count=count+1
        if count >= len(function_list):
            count=0
        function = function_list[count]
        (top_actor, middle_actor, bottom_actor) = function()
        stepcount = 360
        cluster = q.bundle(pixels, wait=0.5, steps=stepcount)
        cluster.add_function(top_actor[0], top_actor[1], attribute=top_actor[2],
                             reverse=top_actor[3])
        cluster.add_function(middle_actor[0], middle_actor[1], attribute=middle_actor[2],
                             reverse=middle_actor[3])
        cluster.add_function(bottom_actor[0], bottom_actor[1], attribute=bottom_actor[2],
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
