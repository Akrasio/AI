from typing import Dict, Optional, Union
import revolt

class AIC:
    def __init__(self) -> None:
        self.revolt: Optional[revolt.Client] = None

    def configure_revolt(self, revolt_client: revolt.Client):
        self.revolt = revolt_client
