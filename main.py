#!/usr/bin/env python
# Here from previous version. May want to connect to t'internet, so left for now
#import WIFI_CONFIG
#from network_manager import NetworkManager
#import uasyncio
#import urequests
import time
import pixel_strings_state_setters as state_setters

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

def update_led_string(led_strip, strip_length, indicies, state, clean=False):
    ''' Match the colour settings in 'state' to the indices provided and applpy
    them to the led_strip. If clean IS set, turn all other LEDs in the
    strip off'''
    if len(indicies) != len(state):
        raise exception("State and indices not of same length")
    if clean:
        # First assign all LEDs to be 'off'
        updated_state = [(0,0,0) for i in range(strip_length)]
        # Then update the one's reffered to by indicie
        for count, index in enumerate(indicies):
            updated_state[index] = state[count]
            print(f"Patching index {index} to {state[count]}")
        indicies = list(range(strip_length))
        state = updated_state
    print(f"tackled 'clean' it was {clean}")
    time.sleep(3)
    for index, colour in zip(indicies, state):
        print(f"Setting index {index} to {colour[red_pos]}, {colour[grn_pos]},"
                         + f" {colour[blu_pos]}")
        led_strip.set_rgb(index, colour[red_pos], colour[grn_pos],
                          colour[blu_pos])
    return

print("step 1")
indicies = list(range(NUM_LEDS))
state = state_setters.make_multi_colour_state_tuple(NUM_LEDS)     
update_led_string(led_strip, NUM_LEDS, indicies, state)
time.sleep(10)

print("step 2")
for index in range(2,len(state),6):
    print (f"updating index {index} to white")
    state[index] = (200, 200, 200) # hopefully set all the green LEDS to white
update_led_string(led_strip, NUM_LEDS, indicies, state) # Sholud see something happen here
time.sleep(10)

print("step 3")
indicies = [x for x in indicies if ((x + 4) % 6) != 0]
# hopefully removes every 6th indicie, from the third
                   # WHich is equally hopefully, all the white ones...
state = [state[x] for x in indicies]
print(f"state has {len(state)} entries and indicies has {len(indicies)}")
print(f"last entry in indicies is {indicies[-1]}")
# remove the colour values to match
update_led_string(led_strip, NUM_LEDS, indicies, state) # Sholud actually fail
# to see a difference here as we're updating without 'clean'
time.sleep(10)

print("step 4")
state = [state[count] for count, x in enumerate(indicies) if ((x+1)%6) != 0]
indicies = [x for x in indicies if ((x + 1) % 6) != 0]
# hopefully removes every 5th indicie, from the fifth
                   # WHich is equally hopefully, all the orange ones...

# remove the colour values to match
print(f"state has {len(state)} entries and indicies has {len(indicies)}")
print(f"last entry in indicies is {indicies[-1]}")
update_led_string(led_strip, NUM_LEDS, indicies, state, clean=True)
time.sleep(10)


#print("step 5")
#indicies = list(range(NUM_LEDS))
#state = state_setters.make_multi_colour_state_tuple(NUM_LEDS)     
#update_led_string(led_strip, NUM_LEDS, indicies, state)
#time.sleep(10)


