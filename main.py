# hikari: API wrapper for Discord
# arc: Command framework for hikari
# miru: UI framework for hikari
# python-dotenv: For loading .env file
# pymongo: MongoDB driver for Python

import hikari
import arc
import miru

import dotenv
import os

from dependencies import Database


dotenv.load_dotenv()


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
assert DISCORD_TOKEN is not None

MONGODB_URI = os.getenv("MONGODB_URI")
assert MONGODB_URI is not None


bot = hikari.GatewayBot(DISCORD_TOKEN)
arc_client = arc.GatewayClient(bot)
miru_client = miru.Client.from_arc(arc_client)

arc_client.set_type_dependency(Database, Database(MONGODB_URI))

arc_client.load_extensions_from("extensions")


@arc_client.listen()
async def on_startup(event: arc.StartedEvent):
    print("Bot is online")


@arc_client.listen()
async def on_shutdown(event: arc.StoppingEvent):
    print("Bot is offline")


bot.run()
