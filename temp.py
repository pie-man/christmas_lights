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
# oooh change
boo-yah Kashan
