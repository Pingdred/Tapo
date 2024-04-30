import math
from cat.mad_hatter.decorators import tool

from .light import Light

light = Light()

#--------------------- INFO ---------------------
@tool
async def get_lightbulb_info(_, cat):
    """Get the status info for the lightbulb, the info include: 
        - Brightness; 
        - Color Temperature;
        - Hue color;
        - Saturation;
        - Status of the light, On or Off;
        - Lightbulb name;"""
    return await light.get_info()

@tool 
async def get_lightbulb_brigtness(_, cat):
    """Get the current lightbulb brightness."""
    brightness = (await light.get_info())["brightness"]

    return f"The lightbulb brightness is: {brightness}"

@tool
async def get_lightbulb_status(_, cat):
    """Get the current lightbulb power status."""
    device_on =  (await light.get_info())["device_on"]

    status = "On" if device_on else "Off"

    return f"The lightbulb is: {status}"

@tool
async def get_lightbulb_name(_, cat):
    """Get the current lightbulb brightness."""
    name =  (await light.get_info())["nickname"]

    return f"The lightbulb brightness is: {name}"

@tool
async def get_lightbulb_color(_, cat):
    """Get the current lightbulb color."""
    color = await light.get_rgb_color()

    return f"The lightbulb color in RGB is: {color.__repr__()}"


#--------------------- Power ---------------------
@tool
async def power_on_lightbulb(_, cat):
    """Power on the lightbulb."""
    
    await light.power_on()
    

    return "The light was turned on"

@tool
async def power_off_lightbulb(_, cat):
    """Power on the lightbulb."""
    await light.power_off()

    return "The light was turned off"


#--------------------- Color ---------------------
@tool
async def set_lightbulb_color(hex_color, cat):
    "Set the lightbulb color. Input is the color in HEX like FF0000."
    await light.set_color(hex_color)
    return "Color changed"


#--------------------- Brightness ---------------------
@tool
async def set_lightbulb_brightness(brightness, cat):
    """Set the lightbulb brightness. Input is the brightness value between 1 and 100."""

    if brightness.isnumeric():

        brightness = int(brightness)

        if brightness < 1 or brightness > 100:
            return "Lightbulb brightness must be between 1 and 100."
        
        await light.set_brightess(brightness)
        
        return f"Brightness set to {brightness}"

@tool
async def reduce_the_lightbulb_brightness(reduce_by, cat):
    """Reduce the lightbulb brightness. Input is the percentage of brightness to be reduced between 1 and 100."""
    brightness = await calc_new_brightness(-int(reduce_by))
    await light.set_brightess(brightness)
    
    return f"Brightness reduced by {reduce_by}%"
    
@tool
async def increase_the_lightbulb_brightness(increase_by, cat):
    """Reduce the lightbulb brightness. Input is the percentage of brightness to be increased between 1 and 100."""
    brightness = await calc_new_brightness(int(increase_by))
    await light.set_brightess(brightness)
    
    return f"Brightness increased by {increase_by}%"


async def calc_new_brightness(perc: int):
    info = await light.get_info()

    current_brightness = info["brightness"]

    if perc == 0:
        return current_brightness

    if perc > 100:
        perc = 100

    if perc < 100:
        perc == -100

    return current_brightness + math.floor((current_brightness*perc)/100)
