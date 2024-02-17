import colorsys
from typing import Any, Dict, Tuple

from tapo import ApiClient

from cat.log import log
from cat.mad_hatter.mad_hatter import MadHatter

class Light:

    def __init__(self) -> None:
        self.client = ApiClient(
            tapo_username=self.username,
            tapo_password=self.password    
        )
        
        self._device = None

    async def _get_device(self):
        if not self._device:
            self._device = await self.client.l530(self.ip_address)  
        return self._device
    

    async def get_info(self):
        log.debug("Getting device info..")
        device = await self._get_device()
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
        log.debug("Turning device on...")
        device = await self._get_device()
        await device.on()

    async def power_off(self):
        log.debug("Turning device off...")
        device = await self._get_device()
        await device.off()


    async def get_rgb_color(self) -> Tuple[int,int,int]:
        info = await self.get_info()

        h = info["hue"]
        s = info["saturation"]
        v = info["brightness"]

        return self._hsv_to_rgb(h,s,v)

    async def set_color(self, color: str):
        log.debug(f"Color in HEX: {color}")

        rgb_color = self._hex_to_rgb(color)
        log.debug(f"Color in RGB: {rgb_color}")

        hsv_color = self._rgb_to_hsv(*rgb_color)
        log.debug(f"Color in HSV: {hsv_color}")

        hue = 1 if hsv_color[0] == 0 else hsv_color[0]
        saturation = 1 if hsv_color[1] == 0 else hsv_color[1]

        device = await self._get_device()
        await device.set_hue_saturation(hue, saturation)
        
        
    async def set_brightess(self, brightness: int):
        device = await self._get_device()
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
    def settings(self) -> Dict[str,Any]:
        return MadHatter().get_plugin().load_settings()
    
    @property
    def username(self) -> str:
        return self.settings["username"]
    
    @property
    def password(self) -> str:
        return self.settings["password"]
    
    @property
    def ip_address(self) -> str:
        return self.settings["ip_address"]
    

    @staticmethod
    def _hex_to_rgb(hex_string) -> Tuple[int,int,int]:
        return tuple(int(hex_string[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def _rgb_to_hsv(r, g, b) -> Tuple[int,int,int]:
        # Normalizza i valori RGB nel range [0, 1]
        r /= 255.0
        g /= 255.0
        b /= 255.0

        h,s,v = colorsys.rgb_to_hsv(r,g,b)

        return (round(h * 360), round(s * 100), round(v * 100))
    
    @staticmethod
    def _hsv_to_rgb(h, s, v) -> Tuple[int,int,int]:
        h /= 360.0
        s /= 100.0
        v /= 100.0

        r, g, b = colorsys.hsv_to_rgb(h,s,v)
        
        return (round(r * 255), round(g * 255), round(b * 255))
