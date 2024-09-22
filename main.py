# Basic Imports
import time
import random
import pixel_strings_state_setters as state_setters
from pixel_strings_actors import fade_to_state_HSV_a, fade_to_state_HSV_b, \
                                 bouncing_blocks, zooming_blocks

NUM_LEDS = 50 # Total nuber of LEDs in the strings (including any ignored ones)

from pixel_strings_ext_libs import plasma_stick_WS2812, update_led_string
led_strip = plasma_stick_WS2812(NUM_LEDS)


# Start 'dark'
print("step 0")
indicies = list(range(NUM_LEDS))
state = state_setters.make_single_colour_state_tuple(NUM_LEDS, (1,1,0))
update_led_string(led_strip, NUM_LEDS, indicies, state)

# Create some colour blocks and zoom them round the string
print("step 1 : Zooming Blocks")
number_of_steps = NUM_LEDS*3
zinger = zooming_blocks(NUM_LEDS, state, state, steps=number_of_steps, number_of_blocks=2, gap_ratio=3)
for step_count, state in enumerate(zinger) :
    update_led_string(led_strip, NUM_LEDS, indicies, state)
#     print(f"done yeild no. {step_count}")
    time.sleep(0.1)

print("step 2")
number_of_steps = NUM_LEDS*2
actor = bouncing_blocks(NUM_LEDS, state, state, steps=number_of_steps, number_of_blocks=5, gap_ratio=1)
for state in actor :
    update_led_string(led_strip, NUM_LEDS, indicies, state)
    time.sleep(0.1)

print("step 3")
while True :
    print("here we go... again...")
    number_of_blocks = random.randint(1,11)
    gap_ratio = random.random() * 4
    number_of_steps = NUM_LEDS * random.randint(2,6)
    print(f"number of blocks is {number_of_blocks}")
    print(f"gap ratio is        {gap_ratio}")
    print(f"number of steps  is {number_of_steps}")
    if random.randint(0,1) :
        actor = zooming_blocks(NUM_LEDS, state, state, steps=number_of_steps, number_of_blocks=number_of_blocks, gap_ratio=gap_ratio)
    else :
        actor = bouncing_blocks(NUM_LEDS, state, state, steps=number_of_steps, number_of_blocks=number_of_blocks, gap_ratio=gap_ratio)
    for state in actor :
        update_led_string(led_strip, NUM_LEDS, indicies, state)
        time.sleep(0.1)
    time.sleep(10)


