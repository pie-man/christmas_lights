'''
Some routines to set a 'state'. A state being a list of colours.
Potentially colours can be a tuple for red, blue and green (in various orders)
or a tuple for Hue, Saturarion and Value
or a 'hex' value (and possibly other scalar values to store the colour)

It may be that the 'state' should also the indecies of the pixels being set, but
this may get complicated as previously 'actors' which animate lights accept
'states' and apply them to subsections of the string. So somewhere along the
line an 'offset' needs to be used to allow mapping betweeen a 'local' index and
the global one.
'''

# Define some set RGB colours by name
RED_RGB               = (255,   0,   0)
ORANGE_RGB            = (255, 127,   0)
YELLOW_RGB            = (255, 255,   0)
CHARTREUSE_GREEN_RGB  = (127, 255,   0)
GREEN_RGB             = (  0, 255,   0)
SPRING_GREEN_RGB      = (  0, 255, 127)
CYAN_RGB              = (  0, 255, 255)
AZURE_RGB             = (  0, 127, 255)
BLUE_RGB              = (  0,   0, 255)
VIOLET_RGB            = (127,   0, 255)
MAGENTA_RGB           = (255,   0, 255)
ROSE_RGB              = (255,   0, 127)

# Define some set HSV colours by name
RED_HSV               = (  0,   1,   1)
ORANGE_HSV            = ( 30,   1,   1)
YELLOW_HSV            = ( 60,   1,   1)
CHARTREUSE_GREEN_HSV  = ( 90,   1,   1)
GREEN_HSV             = (120,   1,   1)
SPRING_GREEN_HSV      = (150,   1,   1)
CYAN_HSV              = (180,   1,   1)
AZURE_HSV             = (210,   1,   1)
BLUE_HSV              = (240,   1,   1)
VIOLET_HSV            = (270,   1,   1)
MAGENTA_HSV           = (300,   1,   1)
ROSE_HSV              = (330,   1,   1)

def RGB_2_HSV(RGB):
    ''' Converts an integer RGB tuple (value range from 0 to 255)
    to an HSV tuple '''

    # Unpack the tuple for readability
    R, G, B = RGB

    # Compute the H value by finding the maximum of the RGB values
    RGB_Max = max(RGB)
    RGB_Min = min(RGB)

    # Compute the value
    V = RGB_Max;
    if V == 0:
        H = S = 0
        return (H,S,V)


    # Compute the saturation value
    S = 255 * (RGB_Max - RGB_Min) // V

    if S == 0:
        H = 0
        return (H, S, V)

    # Compute the Hue
    if RGB_Max == R:
        H = 0 + 43*(G - B)//(RGB_Max - RGB_Min)
    elif RGB_Max == G:
        H = 85 + 43*(B - R)//(RGB_Max - RGB_Min)
    else: # RGB_MAX == B
        H = 171 + 43*(R - G)//(RGB_Max - RGB_Min)

    return (H, S, V)

def HSV_2_RGB(HSV):
    ''' Converts an integer HSV tuple (value range from 0 to 255) to an
    RGB tuple '''

    # Unpack the HSV tuple for readability
    H, S, V = HSV

    # Check if the color is Grayscale
    if S == 0:
        R = V
        G = V
        B = V
        return (R, G, B)

    # Make hue 0-5
    region = H // 43;

    # Find remainder part, make it from 0-255
    remainder = (H - (region * 43)) * 6; 

    # Calculate temp vars, doing integer multiplication
    P = (V * (255 - S)) >> 8;
    Q = (V * (255 - ((S * remainder) >> 8))) >> 8;
    T = (V * (255 - ((S * (255 - remainder)) >> 8))) >> 8;


    # Assign temp vars based on color cone region
    if region == 0:
        R = V
        G = T
        B = P
    
    elif region == 1:
        R = Q; 
        G = V; 
        B = P;

    elif region == 2:
        R = P; 
        G = V; 
        B = T;

    elif region == 3:
        R = P; 
        G = Q; 
        B = V;

    elif region == 4:
        R = T; 
        G = P; 
        B = V;

    else: 
        R = V; 
        G = P; 
        B = Q;


    return (R, G, B)

def scale_255int_to_1_real(input_val):
   '''Scales an integer, scale 0 to 255, to a real on a scale from 0 to 1'''
   return input_val / 255.0

def scale_255int_to_360_real(input_val):
   '''Scales an integer, scale 0 to 255, to a real on a scale from 0 to 360'''
   return input_val * 360.0 / 255.0

def scale_1_real_to_255int(input_val):
   '''Scales a real on a scale from 0 to 1 to an integer, scale 0 to 255,'''
   return round( input_val * 255.0 )

def scale_360_real_to_255int(input_val):
   '''Scales a real on a scale from 0 to 360 to an integer, scale 0 to 255,'''
   return round( input_val * 255.0 / 360.0 )


def get_random_colour_HSV_arc(spread=360, offset=0,
                              saturation=1.0, value=1.0):
    '''Function to create a HSV value for a random colour
       spread is the 'range' of colours to select from as described by an arc in
       degrees ; default 360, all colours.
       offset is the start point of the arc in degrees ; default is 0 and is
       innefective if spread == 360
       saturation allows for external setting of the saturation value and is
       returned as part of the finished tuple. It may be nice to allow
       controlled random selection of this at some point.
       value, allows for the external setting of the brigtness value part of
       HSV. As with saturation, controlled random selection may be desireable.
    '''
    hue = ((randint(0,spread*10) / 10 ) + offset ) % 360
    return (hue, saturation, value)
 
def get_random_colour_RGB_arc(spread=360, offset=0,
                              saturation=1.0, value=1.0):
    '''Function to create an RGB value for a random colour
       It would be quite difficult to 'think' about an arc round an RGB colour
       circle to select a random colour from within it.
       So I didn't bother. The arc is defined exactly the same as for HSV, but
       this function returns the RGB value generated.
       spread is the 'range' of colours to select from as described by an arc in
       degrees ; default 360, all colours.
       offset is the start point of the arc in degrees ; default is 0 and is
       innefective if spread == 360
       saturation allows for external setting of the saturation value and is
       returned as part of the finished tuple. It may be nice to allow
       controlled random selection of this at some point.
       value, allows for the external setting of the brigtness value part of
       HSV. As with saturation, controlled random selection may be desireable.
       The resulting HSV tuple is then conveerted to an RGB colour.
    '''
    (hue, saturation, value) = get_random_colour_HSV_arc(spread=spread,
                               offset=offset, saturation=saturation,
                               value=value)
    hue_255        = scale_360_real_to_255int(hue)
    saturation_255 = scale_1_real_to_255int(saturation)
    value_255      = scale_1_real_to_255int(value)
    return HSV_2_RGB((hue_255, saturation_255, value_255))
 

