import asyncio
import disc
import rev
from controller import AIC
asyncio.get_event_loop().run_until_complete(asyncio.gather(
    rev.run_revolt(AIC),
    disc.run_discord(AIC),
))
