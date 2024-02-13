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


@tool()
def get_lightbulb_info(input, cat):
    """Get the status info for the lightbulb, the info include: brightness, color_temp, hue, saturation, power, name"""
    return run_corutine(
        light.get_info()
    )


@tool()
def power_on_lightbulb(input, cat):
    """Power on a the lightbulb"""
    run_corutine(
        light.power_on()
    )

    return "The light was turned on"


@tool()
def power_off_lightbulb(input, cat):
    """Power on a the lightbulb"""
    run_corutine(
        light.power_off()
    )

    return "The light was turned off"


