import time
import random
from machine import Pin # type: ignore
import plasma # type: ignore

import pixel_strings_helper_fncs as fncs
import pixel_strings_state_setters as states
import pixel_strings_actors as actors

NUM_LEDS = 50 # Total number of LEDs in the strings (including any ignored ones)
FPS = 60  # Frames per second
PICO_LED = Pin('LED', Pin.OUT)


class LEDStrip:
    def __init__(self, num_pixels):
        self.num_pixels = num_pixels
        # Initialize all pixels to off (0, 0, 0)
        self.state = [(0, 0, 0) for _ in range(num_pixels)]
        self.subsections = {}

        # Create and add the default 'all' subsection
        indecies = [x for x in range(num_pixels)],
        state = [(0, 0, 0) for _ in range(num_pixels)]
        self.add_subsection("all", indecies, state)

        # Next bit is 'particular' to the current batch of Plasma Boards
        self.led_strip = plasma.WS2812(NUM_LEDS, color_order=plasma.COLOR_ORDER_RGB)
        self.led_strip.start(FPS)

    def set_pixel(self, index, color):
        if 0 <= index < self.num_pixels:
            self.state[index] = color

    def get_pixel(self, index):
        if 0 <= index < self.num_pixels:
            return self.state[index]
        return None

    def get_state(self):
        return self.state
    
    def set_state(self, new_state):
        if len(new_state) == self.num_pixels:
            self.state = new_state

    def update_strip_hsv(self):
        for i in range(self.num_pixels):
            self.led_strip.set_hsv(i, *self.state[i])

    def update_strip_rgb(self):
        for i in range(self.num_pixels):
            self.led_strip.set_rgb(i, *self.state[i])

    def update_state_from_subsection(self, section_name):
        pixels = self.subsections[section_name].indecies
        colours = self.subsections[section_name].state
        for pixel, colour in zip(pixels, colours):
            self.set_pixel(pixel, colour)
    
    def get_no_pixels(self):
        return self.num_pixels
    
    class SubSection:
        def __init__(self, indecies=[0], state=[(0,0,0)]):
            self.indecies = indecies
            self.state = state
        def get_state(self):
            return self.state
        def get_indecies(self):
            return indecies
        def update_state(self, state):
            state_len = len(state)
            if len(self.indecies) < state_len:
                self.state = state(:len(indecies))
            elif len(self.indecies) > state_len:
                extras = len(state) - len(self.indecies)
                count = 0
                self.state = state
                while extras > 0:
                    extras -= 1
                    self.state.append(state[count])
                    count = (count + 1) % state_len
        
    
    def add_subsection(self, name, indecies, state):
        self.subsections[name] = self.SubSection(indecies, state)

    def update_subsection(self, name, state):
        self.subsections[name].update_state(state)

    

lights = LEDStrip(NUM_LEDS)

lights.set_state([(200, 0, 200) for _ in range(NUM_LEDS)])
lights.update_strip_rgb()
time.sleep(2)

random_start = random.randint(0, 360)
arc_increments = 360 / NUM_LEDS
for pixel in range(NUM_LEDS):
    hue = ((pixel * arc_increments) + random_start) % 360
    lights.set_pixel(pixel, (hue/360,  1, 0.5))
lights.update_strip_hsv()

for _ in range(60):
    random_start = (random_start + arc_increments) % 360
    for pixel in range(NUM_LEDS):
        hue = ((pixel * arc_increments) + random_start) % 360
        lights.set_pixel(pixel, (hue/360,  1, 0.5))
    lights.update_strip_hsv()
    time.sleep(0.1)

# Create some subsections...
def red(count):
    return states.make_single_colour_state_tuple(count, fncs.RED_HSV)
def green(count):
    return states.make_single_colour_state_tuple(count, fncs.GREEN_HSV)
def blue(count):
    return states.make_single_colour_state_tuple(count, fncs.BLUE_HSV)
def yellow(count):
    return [(60/360, 1 , 0.8) for x in range(count)]
def cyan(count):
    return [(180/360, 1 , 0.8) for x in range(count)]
def magenta(count):
    return [(300/360, 1 , 0.8) for x in range(count)
]
lights.add_subsection('one', [x for x in range(10)], red(10))
lights.add_subsection('two', [x for x in range(10,20)], green(10))
lights.add_subsection('three', [x for x in range(20,30)], blue(10))
lights.add_subsection('four', [x for x in range(30,40)],yellow(10))
lights.add_subsection('five', [x for x in range(40,50)],magenta(10))

lights.add_subsection('evens', [x for x in range(0,50,2)], red(25))
lights.add_subsection('odds', [x for x in range(1,50,2)], blue(25))

lights.update_state_from_subsection('evens')
lights.update_state_from_subsection('odds')
lights.update_strip_hsv()
time.sleep(6)

lights.update_state_from_subsection('one')
lights.update_state_from_subsection('two')
lights.update_state_from_subsection('three')
lights.update_state_from_subsection('four')
lights.update_state_from_subsection('five')
lights.update_strip_hsv()
time.sleep(5)

sections = ['A', 'B', 'C', 'D', 'E']
no_of_sections = len(sections)
colours = [red, green, blue, yellow, magenta]
for offset in range(120):
    for count, section in enumerate(sections):
        start = (count+offset) % no_of_sections
        indecies = [x for x in range(start, 50, no_of_sections)]
        length = len(indecies)
        # There probably ought to be an 'update' subsection method...
        lights.add_subsection(section,
                              indecies,
                              colours[count](length))
        #print(f"first index = {indecies[0]}, count = {count}")
        lights.update_state_from_subsection(sections[count])
    lights.update_strip_hsv()
    time.sleep(2)

sections = ['A', 'B', 'C', 'D', 'E']
section_actors = {}
no_of_sections = len(sections)
section_len = lights.get_no_pixels // no_of_sections
extras = lights.get_no_pixels % no_of_sections
prev_end = -1
for section in sections:
    start_pixel = prev_end + 1
    section_indecies = list(range(start_pixel, section_len))
    section_state = [(0,0,0) for x in range(section_len)]
    prev_end += section_len
    if extras > 0:
        prev_end += 1
        extras -= 1
    lights.add_subsection(section,section_indecies,section_state)

steps = 120
for section in sections:
    section_actors[section] = actors.zooming_blocks(section_len,
                                                    [(0,0,0) for x in range(section_len)],
                                                    [(0,0,0) for x in range(section_len)],
                                                    steps,1,1)
for step in range(steps):
    for section, section_actor in section_actors.items():
        lights.update_subsection(section, next(section_actor))
    lights.update_strip_hsv()
    time.sleep(2)
