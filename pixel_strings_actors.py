import time
from random import randint
from pixel_strings_ext_libs import update_led_string
 
''' The original 'actors' were iterables defined to yeild a given number of
    updates to pixels.
    The presumption being that the 'string' had been notionally divided into
    'sections' upon which an 'actor' acted. The numder of 'steps' for a
    collection of 'actors' was the same and thus as the main loop stepped
    through the updates, all the sections updated at once.
    The original 'sections' were three horizontal loops of the tree all formed
    from the same single string. It even had to include pixels that were between
    the 'loops' and never got illuminated.
    
    In this 'new' iteration of the code, a decision needs to be made as to what
    the interface looks like. i.e. what the actors all need to be provided with
    whether they update thier respective sections of string, or just pass a
    state update (full or partial) back to the main loop for it to update the
    actual string.
    
    count (in) : number of pixels this actor is selecting colours for
    steps (in) : number of 'states' the actor will yield
    old_state (optional?) : the 'state' of the pixels at the start of this
                            actor's tenure. For example actors which manipulate
                            a given state over time, such as rotating it aorund
                            the string, or fading from it to something else.
    new_state (optional?) : For actors where the final state wants to defined
                            exteranlly, such as a fade to black (white, other)
    For states which rely on some kind of calculation, such as bouncing or
    zooming blocks - other parameters will be required to define the numebr and
    lengths of the blocks, pluss possibly the fade times etc.
'''

def section_subsplitting(pixel_count, number_of_blocks, gap_ratio
                         include_blank=False, max_blocks=False):
    '''
        Routine to break a length of pixels into subsections.
        Takes the original length, the desired number of subsections and
        the ratio of the 'illuminated' block to the gaps between blocks.
        So a ration of 0.0 would have no gaps, 1.0 the gaps would be of equal
        length to the iluminated blocks and 3.0 would make gaps 3 times longer
        than illuminated blocks, meaning the illuminated section was 1/4 the
        length of the sub-section.
        The 'include_blank' boolian is for patterns where the run of
        illuminated pixels is assumed to have a 'blank' one at the end so as it
        travels along, no 'clean-up' is required to return to blank.
        The 'max_blocks' boolian is for occasions where itn is desirable to
        adjust the block/gap ration until it is as close as possible to the
        ratio specified, but less than it making the length of illuminated
        pixels the maximum.
    '''
    # Basic check - a -ve gap ratio makes no sense...
    # Could raise an error - but actually want code to continue running as we're
    # just illuminateing some lights here...
    if gap_ratio < 0.0:
        gap_ratio = 0.0
    # First stab at getting the subsection length
    section_length = int(pixel_count // number_of_blocks)
    # More saftety checks. Initial issue was many blocks and a large gap ratio
    # meant when converted to integers, there was no illuminated block
    if section_length < 5:
        number_of_blocks = int(pixel_count // 5)
        print(f"resetting number of blocks to {number_of_blocks} due to short section length")
        section_length = int(pixel_count // number_of_blocks)
    # Actual source of error is when (1 + gap_ratio) > section_length means
    # block_length is 0
    block_length = int(section_length // (1 + gap_ratio))
    gap_length = section_length - block_length
#     print(f"section_length is {section_length}")
#     print(f"block_length is {block_length}")
#     print(f"gap_length is {gap_length}\n")
    while (gap_length / block_length) > gap_ratio:
#         print(f"Calculated {gap_length / block_length}, prepare for lift off...")
        gap_length -= 1
        block_length +=1
#     print(f"Final calculated {gap_length / block_length}, We are in orbit")
    #print(f"section_length is {section_length}")
    #print(f"block_length is {block_length}")
    #print(f"gap_length is {gap_length}\n")

    return block_length

def fade_to_state_HSV_a(count, old_state, new_state, steps=25):
    ''' A function to fade from one 'state' to another.
    This function assumes both 'states' are of length 'count' and that they are lists of tuples defining a colour in terms of Hue, Saturation and Value.
    Normally, to fade from one colour to another, you just alter 'Hue', but if the target colour is white or black, you actually want to adjust saturation or value respectively. (Once you've got to white, or black, for belt-n-braces then adjust the Hue to whatever was provided so the next transition starts with whatever the coder had in mind.)
    '''
    print(f"In fade_to_state_HSV_a for {count} steps")
    transition_tuples = []
    for pixel in range(count):
        if new_state[pixel][1] == 0: # Saturation == 0, new colour is white
            transition_tuples.append( (1, 1.0/steps, 1) )
        elif new_state[pixel][2] == 0: # Value == 0, new colour is black
            transition_tuples.append( (1, 1, 1.0/steps) )
        else: # In this case we're adjusting Hue, primarily, but will allow for the other two to vary as well
            transition_tuples.append( (1.0/steps, 1.0/steps, 1.0/steps) )
        # Check to see if 'wrapping' round from 1 to 0 is 'shorter' than staying within bounds.
        # This relies on Hue having it's modulo taken to put it in a range between 0 and 1
        if (abs(new_state[pixel][0]-old_state[pixel][0]) > 0.5):
            old_state[pixel] = tuple([old_state[pixel][0] -1, old_state[pixel][1], old_state[pixel][2]])
            #old_state[pixel] = tuple(old_state[pixel][0] -1, old_state[pixel][1], old_state[pixel][2])
    for step in range(steps):
        state=[]
        for pixel in range(count):
            state.append(tuple(el2*adj*step + (el1 * (1.0-(adj * step))) for el1, el2, adj in zip(old_state[pixel],new_state[pixel],transition_tuples[pixel])))
        yield state
    yield new_state

def fade_to_state_HSV_b(count, old_state, new_state, steps=25):
    ''' A function to fade from one 'state' to another.
    This function assumes both 'states' are of length 'count' and that they are lists of tuples defining a colour in terms of Hue, Saturation and Value.
    This varient doesn't attempt to do anything 'clever' it justs fades from one set of HSV to another (rolling over
    the HUE boundary if that's shorter than traversing within bounds)
    '''
    print(f"In fade_to_state_HSV_b for {count} steps")
    fake_state = [] # This allows for special fades to black or white, plus shortest route through Hue
    for pixel in range(count):
        fake_pixel_hue, fake_pixel_sat, fake_pixel_val = new_state[pixel]
        if new_state[pixel][2] == 0: # Fading to black : Leave Hue static
            fake_pixel_hue = old_state[pixel][0]
        if new_state[pixel][1] == 0: # Fading to white : Leave Hue Static
            fake_pixel_hue = old_state[pixel][0]
        # Check to see if 'wrapping' round from 1 to 0 is 'shorter' than staying within bounds.
        if (abs(new_state[pixel][0]-old_state[pixel][0]) > 0.5):
            fake_pixel_hue = new_state[pixel][0] + 1
        fake_state.append (tuple([fake_pixel_hue, fake_pixel_sat, fake_pixel_val]))
    for step in range(steps):
        state=[]
        for pixel in range(count):
            old_hue, old_sat, old_val = old_state[pixel]
            new_hue, new_sat, new_val = fake_state[pixel]
            temp_hue = ((new_hue*(step/steps)) + (old_hue * (1.0-(step/steps))) % 1.0)
            temp_sat = (new_sat*(step/steps)) + (old_sat * (1.0-(step/steps)))
            temp_val = (new_val*(step/steps)) + (old_val * (1.0-(step/steps)))
            state.append(tuple([temp_hue, temp_sat, temp_val]))
        yield state
    # By yeilding new_state as the last action we ensure the next 'stage' get's
    # what was expected even if we went clever on fades to white or black
    yield new_state

def zooming_blocks(pixel_count, old_state, new_state, steps=25, number_of_blocks=6, gap_ratio=1.0):
    '''
    Messy bit of demo code which creates a number of 'blocks' (default=6) each
    of a randomly selected colour eveny spaced out along the length of the
    pixel string. The length of the gaps between each block is determined by
    gap_ration (default 1.0) where the length of the gap is the length of the
    'block' multiplied by gap_ratio all scaled to be integers such that
    block_length + gap_length = section_length
    and
    section_length = total_numer_of_pixels_in_string / number_pf_blocks
    '''
    print(f"In Zooming Blocks for {steps} steps")
    state = old_state
    #noblocks = 6
##=-     if gap_ratio < 0.0:
##=-         gap_ratio = 0.0
##=-     section_length = int(pixel_count // number_of_blocks)
##=-     if section_length < 5:
##=-         number_of_blocks = int(pixel_count // 5)
##=-         print(f"resetting number of blocks to {number_of_blocks} due to short section length")
##=-         section_length = int(pixel_count // number_of_blocks)
##=-     block_length = int(section_length // (1 + gap_ratio))
##=-     gap_length = section_length - block_length
##=- #     print(f"section_length is {section_length}")
##=- #     print(f"block_length is {block_length}")
##=- #     print(f"gap_length is {gap_length}\n")
##=-     while (gap_length / block_length) > gap_ratio:
##=- #         print(f"Calculated {gap_length / block_length}, prepare for lift off...")
##=-         gap_length -= 1
##=-         block_length +=1
##=- #     print(f"Final calculated {gap_length / block_length}, We are in orbit")
##=-     #print(f"section_length is {section_length}")
##=-     #print(f"block_length is {block_length}")
##=-     #print(f"gap_length is {gap_length}\n")

    section_length, block_length, gap_length = section_subsplitting(
                                        pixel_count, number_of_blocks, gap_ratio
                                        include_blank=False, max_blocks=False):
    blocks=[]
    colours = []
    # Create a list of lists. Each lists contains a block of indecies for pixels
    # This first bit is a really overengineered way to 'space' out the left over pixels..
    # If there are more 'left over pixels than blocks - add one to the block length until there aren't
    gap_size = pixel_count - (number_of_blocks * section_length)
    print(f"Gap Size is {gap_size}")
    while gap_size >= number_of_blocks:
#         print("A quick lap of the moon folks....\n")
        block_length += 1
        gap_size -= number_of_blocks
    if gap_length > 1:
        block_length += 1
        gap_length -= 1
#     print(f"section_length is still {section_length}")
#     print(f"gap_length is {gap_length}")
#     print(f"block_length is {block_length}")

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

    for _ in range(steps):
        for point in range(block_length):
            count = 0
            for block in blocks:
                block[point] += 1
                block[point] = block[point]%pixel_count
                state[block[point]] = (colours[count],1,values[point])
                count += 1
        #update_led_string(led_strip, pixel_count, indicies, state)
        yield state
        #time.sleep(0.1)
    print("... All Done ...")
    yield new_state

def bouncing_blocks(pixel_count, old_state, new_state, steps=25, number_of_blocks=6, gap_ratio=1.0):
    print(f"In Bouncing Blocks for {steps} steps")
    #noblocks = 6
    state = old_state
##=-     if gap_ratio < 0.0:
##=-         gap_ratio = 0.0
##=-     section_length = int(pixel_count // number_of_blocks)
##=-     if section_length < 5:
##=-         number_of_blocks = int(pixel_count // 5)
##=-         print(f"resetting number of blocks to {number_of_blocks} due to short section length")
##=-         section_length = int(pixel_count // number_of_blocks)
##=-     block_length = int(section_length // (1 + gap_ratio))
##=-     if block_length < 1:
##=-         block_length = 1
##=-     gap_length = section_length - block_length
##=-     #print(f"section_length is {section_length}")
##=-     #print(f"block_length is {block_length}")
##=-     #print(f"gap_length is {gap_length}\n")
##=-     while (gap_length / block_length) > gap_ratio:
##=-         #print(f"Calculated {gap_length / block_length}, prepare for lift off...")
##=-         gap_length -= 1
##=-         block_length +=1
##=-     #print(f"Final calculated {gap_length / block_length}, We are in orbit")
##=-     #print(f"section_length is {section_length}")
##=-     #print(f"block_length is {block_length}")
##=-     #print(f"gap_length is {gap_length}\n")

    section_length, block_length, gap_length = section_subsplitting(
                                        pixel_count, number_of_blocks, gap_ratio
                                        include_blank=False, max_blocks=False):
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
        #update_led_string(led_strip, pixel_count, indicies, state)
        yield state
        #time.sleep(0.1)
    print("... All Done ...")
    yield new_state

#=- def fade_to_state_rgb(pixels, index, new_state, steps=25, reverse=False):
#=-     active_pixels = len(index)
#=-     if active_pixels != len(new_state):
#=-         print("Error in fade_to_state_rgb : Length of states not consistent")
#=-         return
#=-     old_state = get_state_rgb(pixels, index)
#=-     for step in range(steps):
#=-         scale_out = int(100*( steps - (step + 1.0) ) / steps)
#=-         scale_in  = 100 - scale_out
#=-         temp_state=[]
#=-         for i in range(active_pixels):
#=-             old_r, old_g, old_b = old_state[i]
#=-             new_r, new_g, new_b = new_state[i]
#=-             cur_r, cur_g, cur_b = (
#=-                    ((old_r * scale_out + new_r * scale_in) // 100) ,
#=-                    ((old_g * scale_out + new_g * scale_in) // 100) ,
#=-                    ((old_b * scale_out + new_b * scale_in) // 100) )
#=-             temp_state.append((cur_r, cur_g, cur_b))
#=-             pixels.set_pixel(index[i],
#=-                     Adafruit_WS2801.RGB_to_color( cur_r, cur_g, cur_b ))
#=-         yield

#<=>- def fade_to_color_rgb(pixels, index, color=(0, 0, 0),
#<=>-                       steps=25, reverse=False):
#<=>-     '''Fades to a single colour state.
#<=>-     Requires the pixels object, a list for length (index) and a colour -RGB
#<=>-     tuple.
#<=>-     Optionally, set teh number of steps to fade over and whether to reverse the
#<=>-     state to fade to (makes no difference here, but is passed to more generic
#<=>-     routine)
#<=>-     Returns an 'actor' function. '''
#<=>-     active_pixels = len(index)
#<=>-     new_state = []
#<=>-     for i in range(active_pixels):
#<=>-         new_state.append(color)
#<=>-     return fade_to_state_rgb(pixels, index, new_state, steps)
#<=>-  
#<=>- def fade_to_black(pixels, index, dummy_attr, steps=25, reverse=False):
#<=>-     return fade_to_color_rgb(pixels, index, color=(0, 0, 0), steps=steps)
#<=>- 
#<=>- def fade_to_white(pixels, index, dummy_attr, steps=25, reverse=False):
#<=>-     return fade_to_color_rgb(pixels, index, color=(255, 255, 255),
#<=>-                              steps=steps)

#=- def rotate_state(pixels, index, skip=1, steps=25, reverse=False):
#=-     active_pixels = len(index)
#=-     current_state = get_state(pixels, index)
#=-     if reverse:
#=-         skip = 0 - skip
#=-     for step in range(steps):
#=-         new_state = ( current_state[0+skip:active_pixels] +
#=-                       current_state[0:(skip - active_pixels)% active_pixels] )
#=-         for i in range(active_pixels):
#=-             pixels.set_pixel(index[i], new_state[i] )
#=-         current_state = new_state
#=-         yield

#=- def rainbow_cycle(pixels, index, attribute=(256, 256,1),
#=-                   steps=25, reverse=False):
#=-     " light up the full block of pixels and then cycle the colours around"
#=-     full_wheel = attribute[0]
#=-     arc_span   = attribute[1]
#=-     laps       = attribute[2]
#=-     length = len(index)
#=-     # cycle through all spread colors in the wheel
#=- 
#=-     for step in range(steps):
#=-         pixel_positions = get_wheel_position (length, step, steps,
#=-                 laps=laps, full_wheel=full_wheel, arc_span=arc_span,
#=-                 reverse=reverse)
#=-         for i in range(length):
#=-             colour = wheel(pixel_positions[i], spread=full_wheel)
#=-             pixels.set_pixel(index[i], colour )
#=-         yield # Return 'control' to main program somewhere

#=- def light_up_successive_rgb(pixels, index, new_state,
#=-                             steps=25, reverse=False):
#=-     ''' Takes an index of pixels, and a new 'state' to set those pixels to.
#=-     Uses the 'pixel_by_step' function to calculate how many pixels (clusters)
#=-     to set at each step, or how many steps to stay on the same pixel if
#=-     steps outnumber pixels.
#=-     Then sets the corresponding number of pixels for the step and yields.'''
#=-     active_pixels = len(index)
#=-     if active_pixels != len(new_state):
#=-         print("Error in fade_to_state_rgb : Length of states not consistent")
#=-         return
#=-     clusters = pixels_by_step(active_pixels, steps)
#=-     if reverse:
#=-         clusters.reverse()
#=-     for cluster in clusters:
#=-         for i in cluster:
#=-             pixel_colour = Adafruit_WS2801.RGB_to_color(
#=-                     new_state[i][0], new_state[i][1],
#=-                     new_state[i][2])
#=-             pixels.set_pixel(index[i], pixel_colour)
#=-         yield

#<=>- def go_out_successive_rgb(pixels, index, not_used, steps=25, reverse=False):
#<=>-     '''Turns the pixels 'off' in clusters such that there are the same
#<=>-     number of clusters as there are steps.'''
#<=>-     state = make_single_colour_state_rgb(index, (0,0,0))
#<=>-     return self.light_up_successive(pixels, index, state,
#<=>-                                     steps, reverse)
#<=>- 
#<=>- def go_dim_successive_rgb(pixels, index, not_used, steps=25, reverse=False):
#<=>-     '''Turns the pixels 'dark' in clusters such that there are the same
#<=>-     number of clusters as there are steps.'''
#<=>-     state = make_single_colour_state_rgb(index, (1,1,1))
#<=>-     return self.light_up_successive(pixels, index, state,
#<=>-                                     steps, reverse)

#=- def appear_from_end_rgb(pixels, index, color=(255, 0, 0), steps=25,
#=-                         reverse=False):
#=-     '''Chases a 'pixel' from one end, to the other, where it remains
#=-     illuminated. Thus as as each 'chase' ends one more pixel is permemanly
#=-     illuminated until the entire string is illuminated.
#=-     The hard part here is going to be how to work out how to complete
#=-     this in a set number of steps as it naturally has n(n+1)/2 steps where
#=-     n is no. of pixels'''
#=-     pos = 0
#=-     jump = 1
#=-     start = 0
#=-     end = len(index) -1
#=-     order = range(start,end,jump)
#=-     if reverse:
#=-         order.reverse()
#=-         jump =-1
#=-         start = len(index) -1
#=-         end = 0
#=-     for i in order:
#=-         old_j = end
#=-         for j in (range(end, i-jump, 0 - jump)):
#=-             pixels.set_pixel(index[old_j],
#=-                    Adafruit_WS2801.RGB_to_color( 0,0,0 ))
#=-             # set then the pixel at position j
#=-             pixels.set_pixel(index[j],
#=-                     Adafruit_WS2801.RGB_to_color( color[0], color[1],
#=-                                                   color[2] ))
#=-             pixels.show()
#=-             #print(j, old_j)
#=-             old_j = j
#=-             time.sleep(0.02)
#=-         yield

#=- def pixels_by_step(pixel_count, steps):
#=-     ''' Takes the number of steps a pattern is going to be displayed for
#=-     and the number of pixels present. Then it calculates the number of
#=-     pixels that need to be adjusted each step, or how many steps to stick
#=-     with the same pixel.
#=-     this version seems to assume a contiguous set of indecies, which might not be valid so lines like 
#=-     'range (fred[i], fred[i+1])' would not produce expected results in non-contiguous lists of pixels.
#=-     That and at Python3 range is an interator, not a list, which would alos probably cause issues.'''
#=-     # create a list of 'steps' length that is as evenly spaced throughout
#=-     # the number of pixels provided.
#=-     fred=[int(float(pixel_count * x)/steps) for x in range(steps)]
#=-     # add an extra final element as we want 'steps' transiitons between
#=-     # 2 points
#=-     fred.append(pixel_count)
#=-     #print ("fred is : {0:}".format(fred))
#=-     list_out=[]
#=-     # loop over the transitions calculating which pixels are 'between' them
#=-     for i in range(len(fred)-1):
#=-         if fred[i] == fred[i+1]:
#=-             # No pixels between the end points, just set first pixel
#=-             dave = [fred[i]]
#=-         else:
#=-             # Some pixels between the end points, range from first to last
#=-             dave= range(fred[i],fred[i+1])
#=-         #print("iter {0:3d} : {1:}".format(i, dave))
#=-         list_out.append(dave)
#=-     return list_out

#=- def get_wheel_position(pixel_length, loop_index, steps_total,
#=-                        laps=1, full_wheel=256, arc_span=256, reverse=False):
#=-     '''We use each pixel as a fraction of the color wheel.
#=-     The full wheel has "full_wheel colours in it.
#=-     The arc_span is the length of the arc on that wheel represented by the
#=-     pixels we have to hand.
#=-     So if arc_span = full_wheel then the pixels will have all the colours
#=-     Find the position of the first pixel in the arc.'''
#=-     start_pos = int((loop_index / float(steps_total)) * laps * full_wheel)
#=-     # Calculate the location of each pixel along the arc
#=-     # the % full_wheel ensures the wheel loops back to the begining.
#=-     pixel_locs = [(int(x * (float(arc_span) / float(pixel_length)))
#=-                   + start_pos) % full_wheel for x in range(pixel_length)]
#=-     if reverse:
#=-         pixel_locs.reverse()
#=-     #print("start_pos = {0:4d} : pixels at : {1:}".format(start_pos, pixel_locs))
#=-     return pixel_locs

#=- # Define an alternative function to interpolate between different hues.
#=- # This function defines 'spread' separate colours
#=- def wheel(pos, spread):
#=-     (red, green, blue) = wheel_rgb(pos, spread)
#=-     return Adafruit_WS2801.RGB_to_color(red, green, blue)

#=- def wheel_rgb(pos, spread):
#=-     pos = pos % spread
#=-     band = spread/3.0
#=-     def scale_val(val):
#=-         mult = 255.0 / band
#=-         return int(val * mult)
#=-     if pos < band:
#=-         return (scale_val(pos), scale_val(int(band - pos)), 0)
#=-     elif pos < (2 * band):
#=-         pos -= int(band)
#=-         return (scale_val(int(band - pos)), 0, scale_val(pos))
#=-     else:
#=-         pos -= int(2 * band)
#=-         return (0, scale_val(pos), scale_val(int(band - pos)))

#<=>- def get_random_colour_rgb(spread=360):
#<=>-     pos = randint(0,spread)
#<=>-     return wheel_rgb(pos, spread)
#<=>-  
#<=>- def get_random_colour(spread=360):
#<=>-     pos = randint(0,spread)
#<=>-     return wheel(pos, spread)
 
#=- def brightness_decrease(pixels, wait=0.01, step=1):
#=-     for j in range(int(256 // step)):
#=-         for i in range(pixels.count()):
#=-             r, g, b = pixels.get_pixel_rgb(i)
#=-             r = int(max(0, r - step))
#=-             g = int(max(0, g - step))
#=-             b = int(max(0, b - step))
#=-             pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color( r, g, b ))
#=-         pixels.show()
#=-         if wait > 0:
#=-             time.sleep(wait)
 
#=- def blink_color(pixels, blink_times=5, wait=0.5, color=(255,0,0)):
#=-     for i in range(blink_times):
#=-         # blink two times, then wait
#=-         pixels.clear()
#=-         for j in range(2):
#=-             for k in range(pixels.count()):
#=-                 pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
#=-             pixels.show()
#=-             time.sleep(0.08)
#=-             pixels.clear()
#=-             pixels.show()
#=-             time.sleep(0.08)
#=-         time.sleep(wait)
 
#=- def ping_pong(pixels, color1=(110, 50, 0), color2=(0, 0, 0), wait=0.05, repeat=5):
#=-     pos = 0
#=-     pixels.clear()
#=-     old_lit=0
#=-     for count in range(repeat):
#=-         for i in range(pixels.count()):
#=-             pixels.set_pixel(old_lit, Adafruit_WS2801.RGB_to_color( *color2 ))
#=-             pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color( *color1 ))
#=-             old_lit = i
#=-             pixels.show()
#=-             time.sleep(wait)
#=-         for i in reversed(range(pixels.count())):
#=-             pixels.set_pixel(old_lit, Adafruit_WS2801.RGB_to_color( *color2 ))
#=-             pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color( *color1 ))
#=-             old_lit = i
#=-             pixels.show()
#=-             time.sleep(wait)
            
#=- class bundle:
#=-     ''' Are you thinking what I'm thinking - yup a docstring would have just been ace...
#=-     It looks to me like the purpose of this class is to store a 'bundle' of functions (actors?) and then
#=-     step through each of them for the defined number of steps.
#=-     So, imagine the long physical string of LEDs has been programatically divided into "sections", each section has it's own length, whichcould all be different, and each section can be displaying the results opf it's own 'function'.
#=-     The original setup was the string formed 3 horizontal loops round the tree (and there were a couple of 'pixels' that weren't used as they were between loops). So each loop could be set to a differnet colour, or the middle loop could gently rotate a rainbow fade in the opposite direction to the other two.
#=-     Things to note:
#=-        In the original examples the call to pixels.set_pixel() effectively filled
#=-     a buffer somewhere with the next 'state' for that pixel and then pixels.show()
#=-     actually altered all the pixels in the string to the new state.
#=-        The number of steps a function was supposed to work across was run-time definable, which is why there's a function to calculate how many pixels, if any, to adjust at each step.
#=- 
#=-     '''
#=-     def __init__(self, pixels, wait=0.7, steps=25):
#=-         self.max_pixels=pixels.count() # curious as to what this was used or intended to be used for
#=-         self.steps = steps # number of steps a 'budle' of functions will be executed over
#=-         self.pixels = pixels # the 'pixels' object to provide base functions for operations on the LED string
#=-         self.wait = wait # A wait time between 'steps'
#=-         self.functions = [] # An empty list of functions, which get added individually, hold their own lists of indecies to affect, and basically have a yeild, that does so after the next 'state' generated by that function has been set
#=-         self.run=True # I'd love to remember why this is here... I assume it was to stop things being looped over more times than a fuinction had been built to run (yeild entries) - but that seems a little odd.
#=-     def add_function(self, function, index, attribute=None, reverse=False):
#=-         self.functions.append(function(self.pixels, index, attribute, steps=self.steps, reverse=reverse))
#=-     def run_bundle(self):
#=-         if self.run:
#=-             for i in range(self.steps):
#=-                 for function in self.functions:
#=-                     function.next()
#=-                 self.pixels.show()
#=-                 time.sleep(self.wait)
#=-             self.run=False

