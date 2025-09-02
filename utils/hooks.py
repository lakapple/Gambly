import arc

from commons import errors


async def has_admin(
    ctx: arc.GatewayContext,
):
    if ctx.user.username != "lakapple":
        raise errors.UserIsNotAdminError()
