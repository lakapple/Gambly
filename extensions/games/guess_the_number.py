from types import new_class
import hikari
import arc
import miru

import random

from dependencies import Database


plugin = arc.GatewayPlugin("guess_the_number")


class GuessTheNumberView(miru.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @miru.button(
        label="<= 10",
        style=hikari.ButtonStyle.PRIMARY
    )
    async def less_than_10_button(
        self,
        ctx: miru.ViewContext,
        button: miru.Button
    ):
        modal = SoTienModal(chosen_option="<=10")
        await ctx.respond_with_modal(modal)

    @miru.button(
        label=">= 11",
        style=hikari.ButtonStyle.PRIMARY
    )
    async def greater_than_11_button(
        self,
        ctx: miru.ViewContext,
        button: miru.Button
    ):
        modal = SoTienModal(chosen_option=">=11")
        await ctx.respond_with_modal(modal)


class SoTienModal(miru.Modal):
    def __init__(self, chosen_option: str):
        self.chosen_option = chosen_option
        super().__init__(title="Nhap so tien muon dat")

    so_tien = miru.TextInput(
        label="So tien ban chon",
        placeholder="Nhap so tien vao day",
        required=True
    )

    @plugin.inject_dependencies
    async def callback(
        self,
        ctx: miru.ModalContext,
        database: Database = arc.inject()
    ):
        result = random.randint(3, 17)
        so_tien = int(self.so_tien.value)

        if result <= 10 and self.chosen_option == "<=10" \
        or result >= 11 and self.chosen_option == ">=11":
            await ctx.respond(
                embed=hikari.Embed(
                    title="Ban da thang",
                    description=f"So ket qua la {result}, ban da thang {so_tien * 2} dong",
                    color=hikari.Color.from_hex_code("00FF00")
                )
            )

            new_balance = await database.get_balance(ctx.user.id) + so_tien * 2
            await database.set_balance(ctx.user.id, new_balance)

        else:
            await ctx.respond(
                embed=hikari.Embed(
                    title="Ban da thua",
                    description=f"So ket qua la {result}, ban da thua {so_tien} dong",
                    color=hikari.Color.from_hex_code("FF0000")
                )
            )

            new_balance = await database.get_balance(ctx.user.id) - so_tien
            await database.set_balance(ctx.user.id, new_balance)


@plugin.include
@arc.slash_command(
    name="doan-so",
    description="Khong phai tai xiu"
)
async def guess_the_number(
    ctx: arc.GatewayContext,
    client: miru.Client = arc.inject(),
):
    view = GuessTheNumberView()

    await ctx.respond(
        embed=hikari.Embed(
            title="Doan so",
            description="Chon 1 trong 2",
            color=hikari.Color.from_hex_code("0000FF")
        ),
        components=view
    )

    client.start_view(view)


@arc.loader
def loader(client: arc.GatewayClient):
    client.add_plugin(plugin)
