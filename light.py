from tapo import ApiClient

from cat.log import log
from cat.mad_hatter.mad_hatter import MadHatter

class Light:

    def __init__(self) -> None:
        self.client = ApiClient(
            tapo_username=self.username,
            tapo_password=self.password    
        )

    async def get_info(self):
        device = await self.client.l530(self.ip_address)

        log.debug("Getting device info..")
        device_info = await device.get_device_info()

        full_info = device_info.to_dict()

        keys = [
            "brightness",
            "color_temp",
            "hue",
            "saturation",
            "device_on",
            "nickname"
        ]

        info = {k:full_info[k] for k in keys}

        return info

    async def power_on(self):
        device = await self.client.l530(self.ip_address)

        log.debug("Turning device on...")
        await device.on()

    async def power_off(self):
        device = await self.client.l530(self.ip_address)

        log.debug("Turning device off...")
        await device.off()

    async def set_color(self, color: str):
        device = await self.client.l530(self.ip_address)

        log.debug(f"Color in HEX: {color}")

        rgb_color = self.hex_to_rgb(color)
        log.debug(f"Color in RGB: {rgb_color}")

        hsv_color = self.rgb_to_hsv(*rgb_color)
        log.debug(f"Color in HSV: {hsv_color}")

        await device.set_hue_saturation(hsv_color[0], hsv_color[1])
        
    async def set_brightess(self, brightness: int):
        device = await self.client.l530(self.ip_address)

        await device.set_brightness(brightness)

        return f"Brightness set to {brightness}"

    async def brightess_up(self):
        info = await self.get_info()

        new_brightness = info["brightness"]+10
        await self.set_brightess(new_brightness)

        return f"Brightness set to {new_brightness}"


    async def brightess_down(self):
        info = await self.get_info()

        new_brightness = info["brightness"]-10
        await self.set_brightess(new_brightness)

        return f"Brightness set to {new_brightness}"


    @property
    def settings(self):
        return MadHatter().get_plugin().load_settings()
    
    @property
    def username(self):
        return self.settings["username"]
    
    @property
    def password(self):
        return self.settings["password"]
    
    @property
    def ip_address(self):
        return self.settings["ip_address"]
    
    @staticmethod
    def hex_to_rgb(hex_string):
        return tuple(int(hex_string[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hsv(r, g, b):
        # Normalizza i valori RGB nel range [0, 1]
        r /= 255.0
        g /= 255.0
        b /= 255.0

        # Trova il valore massimo e minimo tra i componenti RGB
        cmax = max(r, g, b)
        cmin = min(r, g, b)
        delta = cmax - cmin

        # Calcola il valore (Value)
        v = cmax

        # Se il valore massimo è zero, allora la saturazione e l'angolo di tonalità sono entrambi nulli
        if cmax == 0:
            s = 0
            h = 0
        else:
            # Calcola la saturazione (Saturation)
            s = delta / cmax

            # Calcola l'angolo di tonalità (Hue)
            if delta == 0:
                h = 0
            elif cmax == r:
                h = 60 * (((g - b) / delta) % 6)
            elif cmax == g:
                h = 60 * (((b - r) / delta) + 2)
            elif cmax == b:
                h = 60 * (((r - g) / delta) + 4)

        return (round(h), round(s * 100), round(v * 100))
