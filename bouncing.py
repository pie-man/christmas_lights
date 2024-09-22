# Basic Imports
import time
import random

import pixel_strings_state_setters as state_setters
from pixel_strings_actors import fade_to_state_HSV_a, fade_to_state_HSV_b

 NUM_LEDS = 50 # Total nuber of LEDs in the strings (including any ignored ones)

TIMES_TO_REPEAT = 60

state = [(0, 1.0, 0.0) * NUM_LEDS]

# The onboard LED - probably don't need it...
from machine import Pin
pico_led = Pin('LED', Pin.OUT)

# set up the WS2812 / NeoPixel¿ LEDs
import plasma
from plasma import plasma_stick
led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_RGB)

# start updating the LED strip
led_strip.start()

def update_led_string(led_strip, strip_length, indicies, state,
                      colour_type='HSV', clean=False):
    ''' Match the colour settings in 'state' to the indices provided and apply
    them to the led_strip. If clean IS set, turn all other LEDs in the
    strip off'''
    if len(indicies) != len(state):
        raise Exception(f"State {len(state)} and indices {len(indicies)} not of same length")
    if clean:
        # First assign all LEDs to be 'off'
        if colour_type.upper() == "RGB":
            colour_tuple = (0, 0, 0)
        else:
            colour_tuple = (0, 1.0, 0.0)
        updated_state = [colour_tuple for i in range(strip_length)]
        # Then update the one's reffered to by indicie
        for count, index in enumerate(indicies):
            updated_state[index] = state[count]
            #print(f"Patching index {index} to {state[count]}")
        indicies = list(range(strip_length))
        state = updated_state
    #print(f"tackled 'clean' it was {clean}")
    #time.sleep(3)
    if colour_type.upper() == "RGB":
        setter = led_strip.set_rgb
    else:
        setter = led_strip.set_hsv
    for index, colour in zip(indicies, state):
        setter(index, colour[0], colour[1], colour[2])
    return

def add_next_pixel(max_length,indecies,new_pixel):
    indecies.append(new_pixel)
    #print(f"length of block is {len(indecies)}, max_length = {max_length}")
    while len(indecies) > max_length:
        #print("adjusting block to max_length")
        indecies = indecies[1:]
        #print(f"  new length of block is {len(indecies)}, max_length = {max_length}")

    return indecies

def bouncing_blocks(pixel_count, indecies, colour, steps=25, length_of_block=6, first_pixel_global_index=0, last_pixel_global_index=99):
    #set up the indecies for this strip
    if length_of_block < pixel_count:
        length_of_block += 1
    
    start_point = random.randint(1,pixel_count) -1
    direction = random.randint(0,1)
    
    block_indecies = []
    block_values = [(colour, 1, (a / (length_of_block -1))) for a in range(length_of_block)]
    print(f"block length = {length_of_block}")
    #print(f"block_values = {block_values}")
    
    new_point = indecies[start_point]
    next_index = start_point
    
    print("Setting off :")
    print(f"    start_point = {start_point}")
    print(f"    start_index = {indecies[start_point]}")
    print(f"    direction   = {direction}")
    print(f"    colour      = {colour}")
    #print(f"    start_point = {start_point})
    
    for _ in range(steps):
        block_indecies = add_next_pixel(length_of_block, block_indecies, indecies[next_index])
        if next_index == pixel_count - 1:
            direction = 0
        elif next_index == 0:
            direction = 1
        if direction == 1:
            next_index += 1
        else :
            next_index -= 1
        
        #print(f"block_indecies are : {block_indecies}")
        #print(f"length of block indecies are : {len(block_indecies)}")
        # iterate over the block_indecies backwards
        for index, pixel_index in enumerate(block_indecies):
            #print(f"index = {index} , pixel_index = {pixel_index} , setting to value {block_values[index]}")
            #update the pixel with indecie, with the corresponding 'value'
            state[pixel_index] = block_values[index]
            
        #update _all_ the pixels
        update_led_string(led_strip, pixel_count, range(NUM_LEDS), state)
        time.sleep(0.1)
    print("... All Done ...")

# Start 'dark'
print("step 0")
indicies = list(range(NUM_LEDS))
state = state_setters.make_single_colour_state_tuple(NUM_LEDS, (1,1,0))
update_led_string(led_strip, NUM_LEDS, indicies, state)

# Create some colour blocks and zoom them round the string
print("step 1")
for _ in range(TIMES_TO_REPEAT):
    indicies = list(range(NUM_LEDS))
    state = state_setters.make_single_colour_state_tuple(NUM_LEDS, (1,1,0))
    update_led_string(led_strip, NUM_LEDS, indicies, state)

    colour = random.random()
    pixel_count = random.randint(1,70) + 30
    shift = random.randint(0,99)
    indicies = [a%NUM_LEDS for a in range(shift,shift+pixel_count)]
    print(f"Block in use goes from {indicies[0]} to {indicies[-1]} ans is {pixel_count} LEDs long")
    bouncing_blocks(pixel_count, indicies, colour, steps=6*pixel_count, length_of_block=random.randint(10,20), first_pixel_global_index=indicies[0], last_pixel_global_index=indicies[-1])
    time.sleep(2)
