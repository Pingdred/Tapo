from pydantic import BaseModel, IPvAnyAddress

from cat.mad_hatter.decorators import plugin


class ConnectionSettings(BaseModel):
    username: str
    password: str
    ip_address: IPvAnyAddress

@plugin
def settings_model():
    return ConnectionSettings