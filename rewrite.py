import time
import random
from machine import Pin # type: ignore
import plasma # type: ignore

NUM_LEDS = 50 # Total number of LEDs in the strings (including any ignored ones)
FPS = 60  # Frames per second
PICO_LED = Pin('LED', Pin.OUT)


class LEDStrip:
    def __init__(self, num_pixels):
        self.num_pixels = num_pixels
        # Initialize all pixels to off (0, 0, 0)
        self.state = [(0, 0, 0) for _ in range(num_pixels)]
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

class Actor:
    def __init__(self, indices):
        self.indices = indices  # List of integers
        self.legth = len(indices)
        self.current_state = [(0, 0, 0) for _ in range(self.legth)]
        self.next_state = [(0, 0, 0) for _ in range(self.legth)]
        self._iterator = iter(self.current_state)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iterator)
    def set_current_state(self, state):
        if len(state) == self.legth:
            self.current_state = state
            self._iterator = iter(self.current_state)
    def set_next_state(self, state):
        if len(state) == self.legth:
            self.next_state = state

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

for _ in range(600):
    random_start = (random_start + arc_increments) % 360
    for pixel in range(NUM_LEDS):
        hue = ((pixel * arc_increments) + random_start) % 360
        lights.set_pixel(pixel, (hue/360,  1, 0.5))
    lights.update_strip_hsv()
    time.sleep(0.5)

