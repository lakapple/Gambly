import hikari
import arc

from dependencies import Database
from commons import errors
from utils import hooks


plugin = arc.GatewayPlugin("bank")

bank = plugin.include_slash_group(
    name="bank",
    description="Ngan hang dia phu"
)


@bank.include
@arc.with_hook(hooks.has_admin)
@arc.slash_subcommand(
    name="set-balance",
    description="Set balance for a user"
)
async def set_balance(
    ctx: arc.GatewayContext,
    user: arc.Option[hikari.User, arc.UserParams("Nguoi can dat so du")],
    amount: arc.Option[int, arc.IntParams("So tien can dat")],
    database: Database = arc.inject(),
):
    discord_id = user.id

    await database.set_balance(discord_id, amount)

    await ctx.respond(
        embed=hikari.Embed(
            title="Thanh cong",
            description=f"Da dat so du cua {user.mention} thanh {amount} dong",
            color=hikari.Color.from_hex_code("00FF00")
        )
        .add_field(
            name="Field 1",
            value="field 1",
            inline=True,
        )
        .add_field(
            name="Field 2",
            value="field 2",
            inline=True,
        )
        .set_author(
            name=ctx.user.display_name,
            icon=ctx.user.make_avatar_url(),
        )
        .set_footer(
            text="Day la mot footer"
        )
        .set_thumbnail(ctx.user.display_avatar_url)
        .set_image(user.display_avatar_url)
    )

@set_balance.set_error_handler
async def set_balance_error_handler(
    ctx: arc.GatewayContext,
    error: Exception,
):
    match error:
        case arc.errors.InvokerMissingPermissionsError():
            await ctx.respond("Ban khong co quyen thuc hien lenh nay")

        case errors.UserIsNotAdminError():
            await ctx.respond(
                embed=hikari.Embed(
                    title="Loi",
                    description="Ban khong co quyen admin",
                    color=hikari.Color.from_hex_code("FF0000")
                )
            )


@bank.include
@arc.slash_subcommand(
    name="transfer",
    description="Donate"
)
async def transfer(
    ctx: arc.GatewayContext,
    to: arc.Option[hikari.User, arc.UserParams("Nguoi can tu thien")],
    amount: arc.Option[int, arc.IntParams("So tien")],
    database: Database = arc.inject(),
):
    sender_discord_id = ctx.user.id
    recipient_discord_id = to.id

    sender_balance = await database.get_balance(sender_discord_id)
    recipient_balance = await database.get_balance(recipient_discord_id)

    await database.set_balance(sender_discord_id, sender_balance - amount)
    await database.set_balance(recipient_discord_id, recipient_balance + amount)


@bank.include
@arc.slash_subcommand(
    name="register",
    description="Chao mung den voi dia nguc uc uc uc"
)
async def register(
    ctx: arc.GatewayContext,
    database: Database = arc.inject(),
):
    discord_id = ctx.user.id

    await database.register(discord_id)

    await ctx.respond("Dang ki thanh cong")

@arc.loader
def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)
