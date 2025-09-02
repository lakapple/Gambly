import hikari
import arc
import miru

from miru.ext import nav

from itertools import batched

from dependencies import Database
from utils import create_leaderboard_embed


plugin = arc.GatewayPlugin("leaderboard")


@plugin.include
@arc.slash_command(
    name="leaderboard",
    description="Xem bang xep hang so tien"
)
async def leaderboard(
    ctx: arc.GatewayContext,
    client: miru.Client = arc.inject(),
    database: Database = arc.inject(),
):
    batch = batched(await database.get_leaderboard(), 10)
    pages = list(map(create_leaderboard_embed, batch))

    items = [
        nav.PrevButton(),
        nav.IndicatorButton(),
        nav.NextButton(),
    ]

    navigator = nav.NavigatorView(pages=pages, items=items)
    builder = await navigator.build_response_async(client)

    await ctx.respond_with_builder(builder)
    client.start_view(navigator)


@arc.loader
def loader(client: arc.GatewayClient):
    client.add_plugin(plugin)
