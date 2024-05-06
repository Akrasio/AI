import revolt
from revolt.ext import commands
import aiohttp
import asyncio
import openai
import re
import os
from controller import AIC
from dotenv import load_dotenv, dotenv_values
load_dotenv()
config = dotenv_values(".env")
openai.api_base = f"http://{config.get('AI_HOSTNAME')}/v1"
openai.api_key = config.get("AI_APIKEY")
model = config.get("AI_MODEL")
bad_wod = config.get("BAD_WORDS")
bad_reg = "/(?:"+ "|".join(bad_wod.split(", ")) +")/gi"
bad_words = bad_wod.split(", ")

class Client(revolt.Client):
    async def on_message(self, message: revolt.Message):
        if message.author.bot:
            return
        if len(message.raw_mentions) == 1 and message.raw_mentions[0] == self.user.id:
            prompt = message.content.replace(f"<@{message.raw_mentions[0]}>", "")
            if prompt == "" or len(prompt) < 1:
                return
            if any(bad_word in prompt.lower() for bad_word in bad_words):
                print("Ignored!")
                return
            response = openai.Completion.create(
                           model=model,
                           prompt=f'{config.get("AI_STYLE")} {prompt}',
                           max_tokens=50,
                           temperature=0.28,
                           top_p=0.78,
                           n=1,
                           echo=False,
                           stream=False)
            await message.channel.send(re.sub(bad_reg, "[REDACTED]", str(response.choices[0].text)))

async def run_revolt(controller: AIC):
    async with aiohttp.ClientSession() as session:
        client = Client(session, config.get("REVOLT_TOKEN"))
        await client.start()
