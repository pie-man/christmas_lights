# Basic Imports
import time
import random
import pixel_strings_state_setters as state_setters
from pixel_strings_actors import fade_to_state_HSV_a, fade_to_state_HSV_b

NUM_LEDS = 100 # Total nuber of LEDs in the strings (including any ignored ones)

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

def zooming_blocks(pixel_count, old_state, new_state, steps=25, number_of_blocks=6, gap_ratio=1.0):
    #noblocks = 6
    if gap_ratio < 0.0:
        gap_ratio = 0.0
    section_length = int(pixel_count // number_of_blocks)
    block_length = int(section_length // (1 + gap_ratio))
    gap_length = section_length - block_length
    #print(f"section_length is {section_length}")
    #print(f"block_length is {block_length}")
    #print(f"gap_length is {gap_length}\n")
    while (gap_length / block_length) > gap_ratio:
        print(f"Calculated {gap_length / block_length}, prepare for lift off...")
        gap_length -= 1
        block_length +=1
    print(f"Final calculated {gap_length / block_length}, We are in orbit")
    #print(f"section_length is {section_length}")
    #print(f"block_length is {block_length}")
    #print(f"gap_length is {gap_length}\n")

    blocks=[]
    colours = []
    # Create a list of lists. Each lists contains a block of indecies for pixels
    # This first bit is a really overengineered way to 'space' out the left over pixels..
    # If there are more 'left over pixels than blocks - add one to the block length until there aren't
    gap_size = pixel_count - (number_of_blocks * section_length)
    print(f"Gap Size is {gap_size}")
    while gap_size >= number_of_blocks:
        print("A quick lap of the moon folks....\n")
        block_length += 1
        gap_size -= number_of_blocks
    if gap_length > 1:
        block_length += 1
        gap_length -= 1
    print(f"section_length is still {section_length}")
    print(f"gap_length is {gap_length}")
    print(f"block_length is {block_length}")

    values = list(a / (block_length - 1) for a in range(block_length))
    #print(values, "\n")
    
    for count in range(number_of_blocks):
        if count <= gap_size:
            boost = count
        else:
            boost = gap_size
        new_block = list(a + (count * section_length) + boost for a in range(block_length))
        #print(f"got a block like this : {new_block}")
        blocks.append(new_block)
        colours.append(count / number_of_blocks)


    #for steps in range(pixel_count * 3):
    for _ in range(steps):
        for point in range(block_length):
            count = 0
            for block in blocks:
                block[point] += 1
                block[point] = block[point]%pixel_count
                state[block[point]] = (colours[count],1,values[point])
                count += 1
        update_led_string(led_strip, pixel_count, indicies, state)
        time.sleep(0.1)
    print("... All Done ...")
    
def bouncing_blocks(pixel_count, old_state, new_state, steps=25, number_of_blocks=6, gap_ratio=1.0):
    #noblocks = 6
    if gap_ratio < 0.0:
        gap_ratio = 0.0
    section_length = int(pixel_count // number_of_blocks)
    block_length = int(section_length // (1 + gap_ratio))
    gap_length = section_length - block_length
    #print(f"section_length is {section_length}")
    #print(f"block_length is {block_length}")
    #print(f"gap_length is {gap_length}\n")
    while (gap_length / block_length) > gap_ratio:
        #print(f"Calculated {gap_length / block_length}, prepare for lift off...")
        gap_length -= 1
        block_length +=1
    #print(f"Final calculated {gap_length / block_length}, We are in orbit")
    #print(f"section_length is {section_length}")
    #print(f"block_length is {block_length}")
    #print(f"gap_length is {gap_length}\n")

    blocks=[]
    colours = []
    # Create a list of lists. Each lists contains a block of indecies for pixels
    # This first bit is a really overengineered way to 'space' out the left over pixels..
    # If there are more 'left over pixels than blocks - add one to the block length until there aren't
    gap_size = pixel_count - (number_of_blocks * section_length)
    #print(f"Gap Size is {gap_size}")
    while gap_size >= number_of_blocks:
        #print("A quick lap of the moon folks....\n")
        block_length += 1
        gap_size -= number_of_blocks
    if gap_length > 1:
        block_length += 1
        gap_length -= 1
    #print(f"section_length is still {section_length}")
    #print(f"gap_length is {gap_length}")
    #print(f"block_length is {block_length}")

    values = list(a / (block_length - 1) for a in range(block_length))
    #print(values, "\n")
    
    for count in range(number_of_blocks):
        if count <= gap_size:
            boost = count
        else:
            boost = gap_size
        new_block = list(a + (count * section_length) + boost for a in range(block_length))
        #print(f"got a block like this : {new_block}")
        blocks.append(new_block)
        colours.append(count / number_of_blocks)


    #for steps in range(pixel_count * 3):
    for _ in range(steps):
        for point in range(block_length):
            for count, block in enumerate(blocks):
                block[point] += 1
                block[point] = block[point]%pixel_count
                state[block[point]] = (colours[count],1,values[point])
        update_led_string(led_strip, pixel_count, indicies, state)
        time.sleep(0.1)
    print("... All Done ...")

# Start 'dark'
print("step 0")
indicies = list(range(NUM_LEDS))
state = state_setters.make_single_colour_state_tuple(NUM_LEDS, (1,1,0))
update_led_string(led_strip, NUM_LEDS, indicies, state)

# Create some colour blocks and zoom them round the string
print("step 1")
zooming_blocks(NUM_LEDS, [0,0,0,0,0], [0,0,0,0,0], steps=NUM_LEDS*3, number_of_blocks=2, gap_ratio=3)
print("step 2")
bouncing_blocks(NUM_LEDS, [0,0,0,0,0], [0,0,0,0,0], steps=NUM_LEDS*2, number_of_blocks=5, gap_ratio=1)
print("step 3")
for _ in range(50):
    print("here we go...")
    number_of_blocks = random.randint(1,11)
    gap_ratio = random.random() * 4
    zooming_blocks(NUM_LEDS, [0,0,0,0,0], [0,0,0,0,0], steps=NUM_LEDS*5, number_of_blocks=number_of_blocks, gap_ratio=gap_ratio)
    update_led_string(led_strip, NUM_LEDS, indicies, state)


