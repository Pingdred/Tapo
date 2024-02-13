import asyncio
from cat.mad_hatter.decorators import tool
from .light import Light

light = Light()

def run_corutine(coro):
    # Salva il loop di eventi corrente prima di creare un nuovo loop
    try:
        loop_originale = asyncio.get_running_loop()
    except RuntimeError:
        loop_originale = None 

    # Avvia un nuovo ciclo di eventi asyncio per eseguire la coroutine
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        res = loop.run_until_complete(coro)
    finally:
        # Chiudi il nuovo ciclo di eventi
        loop.close()
        
        # Ripristina il loop di eventi originale
        asyncio.set_event_loop(loop_originale)

    return res


@tool
def get_lightbulb_info(_, cat):
    """Get the status info for the lightbulb, the info include: brightness, color_temp, hue, saturation, power, name"""
    return run_corutine(
        light.get_info()
    )


@tool
def power_on_lightbulb(_, cat):
    """Power on a the lightbulb, Ho avuto un idea"""
    run_corutine(
        light.power_on()
    )

    return "The light was turned on"


@tool
def power_off_lightbulb(_, cat):
    """Power on a the lightbulb"""
    run_corutine(
        light.power_off()
    )

    return "The light was turned off"


@tool
def set_lightbulb_color(hex_color, cat):
    "Set the lightbulb color. Input is the color in HEX like FF0000"
    run_corutine(
        light.set_color(hex_color)
    )

    return "Color changed"

@tool
def set_lightbulb_brightness(brightness, cat):
    """Set the lightbulb brightness. Input is the brightness value between 0 and 100, or up, down, max, min"""

    if brightness.isnumeric():
        if int(brightness) < 0 or int(brightness) > 100:
            return "Lightbulb brightness must be between 0 and 100."
        
        run_corutine(
            light.set_brightess(int(brightness))
        )

        return "Brightness changed"    
        
    # if brightness.lower() == "up":
    #     run_corutine(
    #         light.brightess_up()
    #     )
    #     return "Brightness up"

    # if brightness.lower() == "down":
    #     run_corutine(
    #         light.brightess_down()
    #     )
    #     return "Brightness down"
    
    # if brightness.lower() == "max":
    #     run_corutine(
    #         light.set_brightess(100)
    #     )
    #     return "Bulb brightness at maximum"
    
    # if brightness.lower() == "min":
    #     run_corutine(
    #         light.set_brightess(1)
    #     )
    #     return "Bulb brightness at minumum"


