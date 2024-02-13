from tapo import ApiClient

from cat.log import log
from cat.mad_hatter.decorators import tool
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

        device.set_color
        
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