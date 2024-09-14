import asyncio
import openai
import re
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()
import hikari
from controller import AIC
config = dotenv_values(".env")
openai.api_base = f"http://{config.get('AI_HOSTNAME')}/v1"
openai.api_key = config.get("AI_APIKEY")
model = config.get("AI_MODEL")
bad_wod = config.get("BAD_WORDS")
bad_reg = "/(?:"+ "|".join(bad_wod.split(", ")) +")/gi"
bad_words = bad_wod.split(", ")

my_intents = (
        hikari.Intents.GUILDS             |
        hikari.Intents.GUILD_EMOJIS       |
        hikari.Intents.GUILD_MESSAGES     |
        hikari.Intents.MESSAGE_CONTENT
    )
async def run_discord(controller: AIC):
    client = hikari.GatewayBot(intents=my_intents, token=config.get("DISCORD_TOKEN"))

    @client.listen()
    async def on_ready(event: hikari.StartedEvent):
        print(f"Now Ready as {client.get_me().username}")

    @client.listen()
    async def on_message(event: hikari.GuildMessageCreateEvent):
        if event.message.author.is_bot:
            return
        if event.message.channel_id == 1240127564895490082:
            print(event.message)
            return this.send_revolt(event.message.content, event.message.author)

        if event.message.channel_id == int(config.get("AI_CHANNEL")):
            if event.message.content == "":
                return

            prompt = event.message.content.replace("/(?:\<\@\!{client.get_me().id\}\>|<@{client.get_me().id}/g", "")
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
            await event.message.respond(re.sub(bad_reg, "[REDACTED]", str(response.choices[0].text)))

    @client.listen()
    async def on_ready(event: hikari.StartedEvent):
        print(f'Logged into Discord as {client.get_me().username}')

    await client.start()
