#!/usr/bin/env python
# Here from previous version. May want to connect to t'internet, so left for now
#import WIFI_CONFIG
#from network_manager import NetworkManager
#import uasyncio
#import urequests
import time
import pixel_strings_state_setters as state_setters
from pixel_strings_actors import fade_to_state_HSV_a, fade_to_state_HSV_b

'''
Code intended to be run on boot which controlls the individually programmable
LED lights on a Christmas tree.
'''

NUM_LEDS = 50 # Total nuber of LEDs in the strings (including any ignored ones)

## This may want to become a 'class' for the pico W,
## possibly to be considered always paired to the WS2812 LEDs
## __init__(no_of_LEDs, type_of_LED): etc...
## Then the same code could be re-used in differing projects and a new class
## instnace for each physical setup made.

# The onboard LED
from machine import Pin
pico_led = Pin('LED', Pin.OUT)

# set up the WS2812 / NeoPixel¿ LEDs
import plasma
from plasma import plasma_stick
led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_RGB)

# When calling library routines to set r,g,b values, not all kit uses
# them in rgb order...
red_pos = 0
grn_pos = 1
blu_pos = 2

# start updating the LED strip
led_strip.start()

def update_led_string(led_strip, strip_length, indicies, state,
                      colour_type='HSV', clean=False):
    ''' Match the colour settings in 'state' to the indices provided and apply
    them to the led_strip. If clean IS set, turn all other LEDs in the
    strip off'''
    if len(indicies) != len(state):
        raise Exception("State and indices not of same length")
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
        #print(f"Setting index {index} to {colour[red_pos]}, {colour[grn_pos]},"
                         #+ f" {colour[blu_pos]}")
        setter(index, colour[0], colour[1], colour[2])
    return

# Start 'dark'
print("step 0")
indicies = list(range(NUM_LEDS))
state = state_setters.make_single_colour_state_tuple(NUM_LEDS, (1,1,0))
update_led_string(led_strip, NUM_LEDS, indicies, state)

# Fade in a nice set of repeating colours
print("step 1a")
old_state = state
new_state = state_setters.make_multi_colour_state_tuple(NUM_LEDS)     
transition = fade_to_state_HSV_a(NUM_LEDS, old_state, new_state, steps=20)
for state in transition:
    update_led_string(led_strip, NUM_LEDS, indicies, state)
    time.sleep(0.1)

time.sleep(10)

# Fade to black
print("step 2a")
old_state = state
new_state = state_setters.make_single_colour_state_tuple(NUM_LEDS, (1,1,0))
transition = fade_to_state_HSV_a(NUM_LEDS, old_state, new_state, steps=20)
for state in transition:
    update_led_string(led_strip, NUM_LEDS, indicies, state)
    time.sleep(0.1)

# Fade in a nice set of repeating colours
print("step 1b")
old_state = state
new_state = state_setters.make_multi_colour_state_tuple(NUM_LEDS)     
transition = fade_to_state_HSV_b(NUM_LEDS, old_state, new_state, steps=20)
for state in transition:
    update_led_string(led_strip, NUM_LEDS, indicies, state)
    time.sleep(0.1)

time.sleep(10)

# Fade to black
print("step 2b")
old_state = state
new_state = state_setters.make_single_colour_state_tuple(NUM_LEDS, (1,1,0))
transition = fade_to_state_HSV_b(NUM_LEDS, old_state, new_state, steps=20)
for state in transition:
    update_led_string(led_strip, NUM_LEDS, indicies, state)
    time.sleep(0.1)

#=- for _ in range(NUM_LEDS):
#=- #for _ in range(len(state1) + len(state2) + len(state3) + len(state4) + NUM_LEDS):
#=-     update_led_string(led_strip, NUM_LEDS, indicies, state[:NUM_LEDS])
#=-     time.sleep(.5)
#=-     state = state[1:] + [state[0]]
#=-     inner_count +=1
#=-     if inner_count % 15 == 0:
#=-         print(f"Inner count is {inner_count} : outer count is {outer_count}, state is {len(state)} long")
#=-     if inner_count % (2* len(state)) == 0:
#=-         print("Transitioning")
#=-         outer_count +=1
#=-         outer_count = outer_count % len(states)
#=-         inner_count = 0
#=-         for i in range(len(states[outer_count])):
#=-             state = state[1:]
#=-             state.append(states[outer_count][i])
#=-             update_led_string(led_strip, NUM_LEDS, indicies, state[:NUM_LEDS])
#=-             if i%10 ==0:
#=-                 print(f"step {i}")
#=-             time.sleep(.5)


print("step 3")
old_state = state
new_state = state_setters.make_rainbow_state_HSV(NUM_LEDS, arc_length=360,
                                                 value=0.75)     
transition = fade_to_state_HSV_a(NUM_LEDS, old_state, new_state, steps=20)
for state in transition:
    update_led_string(led_strip, NUM_LEDS, indicies, state, colour_type='HSV')
    time.sleep(0.1)

time.sleep(5)

print("step 4")
for _ in range(NUM_LEDS * 2):
    old_state = state
    new_state = state[1:] + [state[0]]
    transition = fade_to_state_HSV_a(NUM_LEDS, old_state, new_state, steps=10)
    for state in transition:
        update_led_string(led_strip, NUM_LEDS, indicies, state[:NUM_LEDS], colour_type='HSV')
        time.sleep(0.05)

print("step 5")
for _ in range(NUM_LEDS * 2):
    old_state = state
    new_state = [state[-1]] + state[0:-1]
    transition = fade_to_state_HSV_a(NUM_LEDS, old_state, new_state, steps=10)
    for state in transition:
        update_led_string(led_strip, NUM_LEDS, indicies, state[:NUM_LEDS], colour_type='HSV')
        time.sleep(0.05)


# Fade to black
print("step 6")
old_state = state
new_state = state_setters.make_single_colour_state_tuple(NUM_LEDS, (1,1,0))
transition = fade_to_state_HSV_a(NUM_LEDS, old_state, new_state, steps=20)
for state in transition:
    update_led_string(led_strip, NUM_LEDS, indicies, state)
    time.sleep(0.1)

print("step 7")
old_state = state
new_state = state_setters.make_rainbow_state_HSV(NUM_LEDS, arc_length=360,
                                                 value=0.75)     
transition = fade_to_state_HSV_b(NUM_LEDS, old_state, new_state, steps=20)
for state in transition:
    update_led_string(led_strip, NUM_LEDS, indicies, state, colour_type='HSV')
    time.sleep(0.1)

time.sleep(5)

print("step 8")
for _ in range(NUM_LEDS * 2):
    old_state = state
    new_state = state[1:] + [state[0]]
    transition = fade_to_state_HSV_b(NUM_LEDS, old_state, new_state, steps=10)
    for state in transition:
        update_led_string(led_strip, NUM_LEDS, indicies, state[:NUM_LEDS], colour_type='HSV')
        time.sleep(0.05)

print("step 9")
for _ in range(NUM_LEDS * 2):
    old_state = state
    new_state = [state[-1]] + state[0:-1]
    transition = fade_to_state_HSV_b(NUM_LEDS, old_state, new_state, steps=10)
    for state in transition:
        update_led_string(led_strip, NUM_LEDS, indicies, state[:NUM_LEDS], colour_type='HSV')
        time.sleep(0.05)


# Fade to black
print("step 10")
old_state = state
new_state = state_setters.make_single_colour_state_tuple(NUM_LEDS, (1,1,0))
transition = fade_to_state_HSV_b(NUM_LEDS, old_state, new_state, steps=20)
for state in transition:
    update_led_string(led_strip, NUM_LEDS, indicies, state)
    time.sleep(0.1)

