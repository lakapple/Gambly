import hikari
import arc

from dependencies import Database


plugin = arc.GatewayPlugin("balance")

bank = plugin.include_slash_group(
    name="bank",
    description="Ngan hang dia phu",
)

@bank.include
@arc.slash_subcommand(
    name="transfer",
    description="Cong vien thuy tinh"
)
async def transfer(
    ctx: arc.GatewayContext,
    to: arc.Option[hikari.User, arc.UserParams("Nguoi can tu thien")],
    amount: arc.Option[int, arc.IntParams("So tien")],

    database: Database = arc.inject()
):
    sender_discord_id = ctx.user.id
    recipient_discord_id = to.id

    sender_balance = await database.get_balance(sender_discord_id)
    recipient_balance = await database.get_balance(recipient_discord_id)

    await database.set_balance(sender_discord_id, sender_balance - amount)
    await database.set_balance(recipient_discord_id, recipient_balance + amount)


@bank.include
@arc.slash_subcommand(
    name="register"
)
async def register(
    ctx: arc.GatewayContext,
    database: Database = arc.inject(),
):
    discord_id = ctx.user.id
    await database.register_user(discord_id)

    await ctx.respond("Registerd")


@arc.loader
def loader(client: arc.GatewayClient):
    client.add_plugin(plugin)
