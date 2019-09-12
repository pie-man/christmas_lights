#!/usr/bin/env python
'''Program to set and step through ligths sequences on 3 rings of WS2801
pixels on the Christmas tree at work'''

import time
from datetime import datetime, timedelta
import pixel_strings_fncs as q
import random
import argparse

# Configure the total number of pixels available:
PIXEL_COUNT = 50

# Logical to enable/disable flashing or rapidly changing sequences.
FLASHING=True

# Define the 'pixel_index' of the three sets of pixels to be used globally
TOP    = range(25, 50)
MIDDLE = range(7, 24)
BOTTOM = range(7)
ALL = [TOP, MIDDLE, BOTTOM]

# Set agloabal print level in case file is imported.
print_level = 1

def set_fade_to_rainbow(pixel_index):
    '''Set the pixels refered to by pixel_index to fade to
       a full rainbow spread around the 'colour wheel'.'''
    debug_print(1, "enetered set_fade_to_rainbow")
    state = q.make_rainbow_state_rgb(pixel_index)
    actor = (q.fade_to_state_rgb, pixel_index, state, False)
    return actor

def set_rainbows_fade(collections):
    '''Set all the groups of pixels in each collection to fade to
       a full rainbow spread around the 'colour wheel'.'''
    debug_print(1, "enetered set_rainbows_fade")
    actors = []
    for collection in collections:
        actors.append(set_fade_to_rainbow(collection))
    return (actors)

def set_fade_to_R_G_or_B(pixel_index):
    '''Set the pixels refered to by pixel_index to fade to
    one of red, green or blue selected randomly'''
    debug_print(1, "enetered set_fade_to_R_G_or_B")
    colours = [(200, 0, 0), (0, 200, 0), (0, 0, 200)]
    state = q.make_single_colour_state(pixel_index,
            colours[random.randint(0,len(colours)-1)])
    actor = (q.fade_to_state_rgb, pixel_index, state, False)
    return (actor)

def set_R_G_or_B_blocks(collections):
    '''Set all the groups of pixels in each collection to fade to
    one of red, green or blue selected randomly'''
    debug_print(1, "enetered set_R_G_or_B_blocks")
    actors = []
    for collection in collections:
        actors.append(set_fade_to_R_G_or_B(collection))
    return (actors)

def set_fade_to_rand_colour(pixel_index):
    '''Set the pixels refered to by pixel_index to fade to
    a random colour'''
    debug_print(1, "enetered set_fade_to_rand_colour ")
    state = q.make_single_colour_state(pixel_index, q.get_random_colour_rgb())
    actor = (q.fade_to_state_rgb, pixel_index, state, False)
    return (actor)

def set_blocks_to_fade_to_rand_colours(collections):
    '''Set all the groups of pixels in each collection to fade to
       a randomly selected colour.
       Selecting separate colours for each block'''
    debug_print(1, "enetered set_blocks_to_fade_to_rand_colours")
    actors = []
    for collection in collections:
        actors.append(set_fade_to_rand_colour(collection))
    return (actors)

def set_fade_to_colour_array(pixel_index):
    '''Set the pixels refered to by pixel_index to fade to
    a predefined set of clours'''
    debug_print(1, "enetered set_fade_to_colour_array ")
    state = q.make_multi_colour_state_rgb(pixel_index, None)
    actor = (q.fade_to_state_rgb, pixel_index, state, False)
    return (actor)

def set_blocks_to_fade_to_colour_arrays(collections):
    '''Set all the groups of pixels in each collection to fade to
       a predefined set of clours.
       Selecting separate colours for each block'''
    debug_print(1, "enetered set_blocks_to_fade_to_colour_arrays")
    actors = []
    for collection in collections:
        actors.append(set_fade_to_colour_array(collection))
    return (actors)

def set_fade_to_black(pixel_index):
    '''Set the pixels refered to by pixel_index to fade
    out completely'''
    debug_print(1, "enetered set_fade_to_black ")
    dummy = "not required"
    actor = (q.fade_to_black, pixel_index, dummy, False)
    return (actor)

def set_blocks_to_fade_black(collections):
    '''Set all the groups of pixels in each collection to fade to
    out completely'''
    debug_print(1, "enetered set_blocks_to_fade_black(): ")
    actors = []
    for collection in collections:
        actors.append(set_fade_to_black(collection))
    return (actors)

def set_fade_to_dim(pixel_index):
    '''Set the pixels refered to by pixel_index to fade
    to almost black'''
    debug_print(1, "enetered set_fade_to_dim ")
    actor    = (q.fade_to_color_rgb, pixel_index, (1,1,1), False)
    return (actor)

def set_blocks_to_fade_to_dim(collections):
    '''Set all the groups of pixels in each collection to fade to
    to almost black'''
    debug_print(1, "enetered set_blocks_to_fade_to_dim():")
    actors = []
    for collection in collections:
        actors.append(set_fade_to_dim(collection))
    return (actors)

def set_to_cycling_rainbow(pixel_index):
    '''Set the pixels refered to by pixel_index to immediately display
    a rainbow pattern and gently cycle it around the block of pixels.'''
    debug_print(1, "enetered set_to_cycling_rainbow ")
    # laps is the number of times the sequence cylces round fully
    laps = random.choice([2,4,6,8])
    direction = random.choice([True, False])
    actor    = (q.rainbow_cycle, pixel_index, (256, 256, laps), direction)
    return (actor)

def set_cycling_rainbow_blocks(collections):
    '''Set all the groups of pixels in each collection to display a rainbow
       pattern and gently cycle it around the group'''
    debug_print(1, "enetered set_cycling_rainbow_blocks(): ")
    actors = []
    for collection in collections:
        actors.append(set_to_cycling_rainbow(collection))
    return (actors)

def set_rainbow_pattern_successive(pixel_index):
    '''Set the pixels refered to by pixel_index to display
    a rainbow pattern by successively illuminating sections of the
    group.'''
    debug_print(1, "enetered set_rainbow_pattern_successive ")
    state = q.make_rainbow_state_rgb(pixel_index)
    actor = (q.light_up_successive_rgb, pixel_index, state, False)
    return (actor)

def set_random_colour_successive(pixel_index):
    '''Set an pixel_index to display a set colour by successively
    illuminating sections of the ring.'''
    debug_print(1, "enetered set_random_colour_successive")
    colour = q.get_random_colour_rgb()
    state = q.make_single_colour_state(pixel_index, colour)
    direction = random.choice([True, False])
    actor = (q.light_up_successive_rgb, pixel_index, state, direction)
    return (actor)

def set_go_out_successive(pixel_index):
    '''Set the pixels refered to by pixel_index to go out
    by successively de-illuminating sections of the block.'''
    debug_print(1, "enetered set_go_out_successive")
    colour = (0, 0, 0)
    state = q.make_single_colour_state(pixel_index, colour)
    direction = random.choice([True, False])
    actor = (q.light_up_successive_rgb, pixel_index, state, direction)
    return (actor)

def set_rotate_state(pixel_index):
    '''Set the pixels refered to by pixel_index to  shift
    round one pixel at a time'''
    debug_print(1, "enetered set_rotate_state")
    colour = (0, 0, 0)
    state = q.make_multi_colour_state_rgb(pixel_index, None)
    direction = random.choice([True, False])
    actor = (q.rotate_state, pixel_index, 1, direction)
    return (actor)

def set_colour_chase():
    '''assign a colour to every Nth pixel (where N=no. of colours provided)
    and then step all the pixels one direction or the othert'''

def set_successive_rainbow_blocks(collections):
    '''Set all the groups of pixels in each collection to display
    a rainbow pattern by successively illuminating sections of the
    groups.'''
    debug_print(1, "enetered set_successive_rainbow_blocks(): ")
    actors = []
    for collection in collections:
        actors.append(set_rainbow_pattern_successive(collection))
    return (actors)

def set_successive_random_colour_blocks(collections):
    '''Set all the groups of pixels in each collection to display
    a randomly selected colour by successively illuminating sections
    of the groups.'''
    debug_print(1, "enetered set_successive_random_colour_blocks(): ")
    actors = []
    for collection in collections:
        actors.append(set_random_colour_successive(collection))
    return (actors)

def set_go_out_successive_blocks(collections):
    '''Set all the groups of pixels in each collection to display
    a rainbow pattern by successively illuminating sections of the
    groups.'''
    debug_print(1, "enetered set_go_out_successive_blocks(): ")
    actors = []
    for collection in collections:
        actors.append(set_go_out_successive(collection))
    return (actors)

def set_rotate_block_states(collections):
    '''Set all the groups of pixels in each collection to shift
    round one pixel at a time'''
    debug_print(1, "enetered set_rotate_block_states(): ")
    actors = []
    for collection in collections:
        actors.append(set_rotate_state(collection))
    return (actors)

def set_right_random_wibblefest(collections):
    '''Randomly select and assign a function for each collection of pixels'''
    debug_print(1, "enetered set_right_random_wibblefest(): ")
    actors = []
    list_of_functions = [
            set_fade_to_rainbow,
            set_fade_to_R_G_or_B,
            set_to_cycling_rainbow,
            set_fade_to_rand_colour,
            set_to_cycling_rainbow,
            set_rainbow_pattern_successive,
            set_random_colour_successive,
            set_go_out_successive,
            ]
    for collection in collections:
        selection  = random.choice(list_of_functions)
        actors.append(selection(collection))
    return (actors)

def debug_print(threshold, text):
    '''Check print level and print messages if threshold is met or exceeded.
    Thus warning/debug messages with a higher threshold can be silenced for
    more routine running and re-enabled if there's debugging to be done.'''
    if print_level >= threshold:
        print(text)

def handle_cmd_args():
    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('--start', dest='starttime', 
                        default=datetime.strftime(datetime.now(), "%H:%M"))
    parser.add_argument('--end', dest='endtime', 
                        default=datetime.strftime(datetime.now()+
                            timedelta(hours=4), "%H:%M"))
    parser.add_argument("-v", "--verbosity", action="count", default=0,
                        help="increase output verbosity")
    args = parser.parse_args()
    print ("my args are...{0:}".format(args))
    print ("my starttime is...{0:s}".format(args.starttime))
    print ("my endtime is...{0:s}".format(args.endtime))
    return args

if __name__ == '__main__':

    pixels = q.initialise_pixels(PIXEL_COUNT)
    function_list = [
            set_blocks_to_fade_to_rand_colours,
            set_R_G_or_B_blocks,
            set_rainbows_fade,
            set_cycling_rainbow_blocks,
            set_blocks_to_fade_to_dim,
            set_blocks_to_fade_to_rand_colours,
            set_blocks_to_fade_to_dim,
            set_blocks_to_fade_to_rand_colours,
            set_blocks_to_fade_to_dim,
            set_blocks_to_fade_to_colour_arrays,
            set_rotate_block_states,
            set_blocks_to_fade_to_dim,
            set_successive_rainbow_blocks,
            set_go_out_successive_blocks,
            set_right_random_wibblefest,
            set_right_random_wibblefest,
            set_right_random_wibblefest,
            set_right_random_wibblefest,
            set_right_random_wibblefest,
            set_right_random_wibblefest,
            set_successive_random_colour_blocks,
            set_right_random_wibblefest,
            set_blocks_to_fade_to_dim,
            set_right_random_wibblefest,
            set_blocks_to_fade_to_dim,
            set_right_random_wibblefest,
            set_blocks_to_fade_to_dim,
            set_rainbows_fade,
            set_cycling_rainbow_blocks,
            set_blocks_to_fade_to_dim,
            ]

    args = handle_cmd_args()

    # some abysmal time mangling to turn "%H:%M" formatted time into a time today
    # Please let there be a better way to do this....
    starttime = datetime.strptime(args.starttime, "%H:%M")
    endtime = datetime.strptime(args.endtime, "%H:%M")
    todays_year = datetime.now().year
    todays_month = datetime.now().month
    todays_day = datetime.now().day
    starttime = starttime.replace(todays_year, todays_month, todays_day)
    endtime = endtime.replace(todays_year, todays_month, todays_day)
    if endtime < starttime:
        endtime = endtime + timedelta(days=1)

    print_level=args.verbosity

    #Wait to start ?
    while starttime >= datetime.now():
        debug_print(1, "having a nap... at {0}".format(datetime.now()))
        time.sleep(300)
    count=len(function_list)-1
    #for function in function_list:
    while endtime > datetime.now():
        count=count+1
        if count >= len(function_list):
            count=0
        function = function_list[count]
        actors = function(ALL)
        stepcount = 180
        cluster = q.bundle(pixels, wait=0.2, steps=stepcount)
        for actor in actors:
            cluster.add_function(actor[0], actor[1],
                                 attribute=actor[2],
                                 reverse=actor[3])
        cluster.run_bundle()

    # Shut it all down quietly...
    debug_print(1, "closing down... at {0}".format(datetime.now()))
    actors = set_blocks_to_fade_black(ALL)
    stepcount = 120
    cluster = q.bundle(pixels, wait=0.5, steps=stepcount)
    for actor in actors:
        cluster.add_function(actor[0], actor[1],
                             attribute=actor[2], reverse=actor[3])
    cluster.run_bundle()
