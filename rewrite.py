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
        def __init__(self, indecies=[0], current_state=[(0,0,0)]):
            self.indecies = indecies
            self.state = current_state
        def get_state(self):
            return self.state
        def get_indecies(self):
            return indecies
        def update_state(self, new_state):
            state_len = len(new_state)
            if len(self.indecies) < state_len:
                self.state = new_state[0:len(self.indecies)]
                print(f"truncating state len {state_len} to {len(self.indecies)}")
            elif len(self.indecies) > state_len:
                extras = len(new_state) - len(self.indecies)
                count = 0
                self.state = new_state
                print(f"Padding state len {len(self.state)} by {extras}")
                while extras > 0:
                    extras -= 1
                    self.state.append(new_state[count])
                    count = (count + 1) % state_len
            else:
                self.state = new_state
        
    
    def add_subsection(self, name, indecies, state):
        self.subsections[name] = self.SubSection(indecies, state)

    def update_subsection(self, name, state):
        print(f"Calling SubSection.update_state on {name} with {len(state)} pixels...")
        self.subsections[name].update_state(state)

    

lights = LEDStrip(NUM_LEDS)

print(f"Going pale purple for 5")
lights.set_state([(200, 0, 200) for _ in range(NUM_LEDS)])
lights.update_strip_rgb()
time.sleep(5)

print(f"Rotating the rainbow for 10")
random_start = random.randint(0, 360)
arc_increments = 360 / NUM_LEDS
for pixel in range(NUM_LEDS):
    hue = ((pixel * arc_increments) + random_start) % 360
    lights.set_pixel(pixel, (hue/360,  1, 0.5))
lights.update_strip_hsv()

for _ in range(100):
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
time.sleep(2)

print(f"% blocks of solid colour for 5")
lights.update_state_from_subsection('one')
lights.update_state_from_subsection('two')
lights.update_state_from_subsection('three')
lights.update_state_from_subsection('four')
lights.update_state_from_subsection('five')
lights.update_strip_hsv()
time.sleep(5)

print(f"A repeating pattern of colours that rotates for 20")
sections = ['A', 'B', 'C', 'D', 'E']
no_of_sections = len(sections)
colours = [red, green, blue, yellow, magenta]
for offset in range(20):
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
    time.sleep(1)

print(f"3 'subsections' with 'zooming blocks' for 2 mins")
lights.set_state([(0, 0, 0) for _ in range(NUM_LEDS)])
lights.update_strip_rgb()
sections = ['A', 'B', 'C']
section_actors = {}
no_of_sections = len(sections)
section_len = lights.get_no_pixels() // no_of_sections
print(f"Section length is {section_len}")
extras = lights.get_no_pixels() % no_of_sections
extras = 0
print(f"Number of extras is {extras}")
start_pixel = 0
for section in sections:
    if section in ['A','C']:
        section_len = 10
    else:
        section_len = 30
    end_pixel = start_pixel + section_len
    section_indecies = list(range(start_pixel, end_pixel))
    section_state = [(0,0,0) for x in range(section_len)]
    if extras > 0:
        end_pixel += 1
        lights.set_pixel(end_pixel, (0, 0, 0))
        extras -= 1
    print(f"Adding section {section}, with {len(section_indecies)} indecies and {len(section_state)} pixels")
    print(f"indecies are  : {section_indecies}")
    lights.add_subsection(section,section_indecies,section_state)
    start_pixel = end_pixel

steps = 1200
for section in sections:
    if section in ['A','C']:
        noblocks = 1
        gaplen = 0
        section_len = 10
    else:
        noblocks = 4
        gaplen = 1
        section_len = 30
    section_actors[section] = actors.zooming_blocks(section_len,
                                                    [(0,0,0) for x in range(section_len)],
                                                    [(0,0,0) for x in range(section_len)],
                                                    steps,noblocks,gaplen)
for step in range(steps):
    for section, section_actor in section_actors.items():
        new_state = next(section_actor)
        #print(f"Section {section} got state ({len(new_state)}) {new_state[0:5]}...")
        #print(f"Updating section {section} with {new_state[0:5]}....{new_state[-1]}")
        lights.update_subsection(section, new_state)
        #print(f"Updating state from subsection {section}")
        lights.update_state_from_subsection(section)
    lights.update_strip_hsv()
    print(f"curently at step no {step}")
    time.sleep(0.1)
