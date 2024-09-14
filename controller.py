from typing import Dict, Optional, Union
import hikari
import revolt

class AIC:
    def __init__(self) -> None:
        self.revolt: Optional[revolt.Client] = None

    def configure_revolt(self, revolt_client: revolt.Client):
        self.revolt = revolt_client

    def send_revolt(self, revolt_client:revolt.Client, message: hikari.messages):
        self.revolt = revolt_client
        self.revolt.get_channel("01GRZ3M26YJE2PJGTG71YNE2NH").send(message.content, masquerade=message.author)
