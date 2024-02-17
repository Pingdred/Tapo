from pydantic import BaseModel, Field, EmailStr, SecretStr, IPvAnyAddress

from cat.mad_hatter.decorators import plugin


class ConnectionSettings(BaseModel):
    username: EmailStr          = Field(title="Email")
    password: SecretStr         = Field(title="Password")
    ip_address: IPvAnyAddress   = Field(title="Tapo IP address")

@plugin
def settings_model():
    return ConnectionSettings
