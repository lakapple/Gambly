import os

import hikari
import arc
import miru
import dotenv

from dependencies import Database


dotenv.load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
assert DISCORD_TOKEN is not None

MONGODB_URI = os.getenv("MONGODB_URI")
assert MONGODB_URI is not None

EXTENSIONS = [
    "extensions.bank",
    "extensions.tai_xiu"
]


bot = hikari.GatewayBot(DISCORD_TOKEN)
arc_client = arc.GatewayClient(bot)
client = miru.Client.from_arc(arc_client)

arc_client.set_type_dependency(Database, Database(MONGODB_URI))

for extension in EXTENSIONS:
    arc_client.load_extension(extension)

bot.run()
