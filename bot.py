import discord
import asyncio
from discord.ext import commands
import asyncio
import openai
import re
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()
config = dotenv_values(".env")
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
openai.api_base = f"http://{config.get('AI_HOSTNAME')}/v1"
openai.api_key = config.get("AI_APIKEY")
model = config.get("AI_MODEL")
bad_wod = config.get("BAD_WORDS")
bad_reg = "/(?:"+ "|".join(bad_wod.split(", ")) +")/gi"
bot = commands.Bot(command_prefix="/", intents=intents)
bad_words = bad_wod.split(", ")

@bot.event
async def on_ready():
    print(f"Ready as {bot.user.name}")
    await bot.change_presence(
        activity=discord.CustomActivity(name="🌸 Becoming Human..."),
        status=discord.Status.dnd
    )
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.channel.id == int(config.get("AI_CHANNEL")):
        prompt = message.content.replace(bot.user.mention, "")
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
bot.run(config.get("DISCORD_TOKEN"))
