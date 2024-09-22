# The intention of this module is to create a common interface to the various
# rgb pixel strin l;ibrary types so the same program elements can be reused
# across different boards and with different libraries.

#This should probably be setting up 'objects' with attributes for the various
# elements (on board leds, buttons, etc) and methods such as "start" the string

# WS2801 libraries (Adafruit : micropython)


# WS2812 / NeoPixel LEDs (Pimoroni Plasma Stick : Circuit Python)


def plasma_stick_WS2812(NUM_LEDS):
    import plasma
    from plasma import plasma_stick
    
    # The onboard LED - probably don't need it...
    #from machine import Pin
    #pico_led = Pin('LED', Pin.OUT)

    led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_RGB)
    led_strip.start()
    return led_strip

def update_led_string(led_strip, strip_length, indicies, state,
                      colour_type='HSV', clean=False):
    ''' Match the colour settings in 'state' to the indices provided and apply
    them to the led_strip. If clean IS set, turn all other LEDs in the
    strip off
    This is currently written for Circuit Python WS2812 libraries - need to
    refactor this as a method of each of the different led strip objects'''
    
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
