import hikari


def create_leaderboard_embed(leaderboard_data: list[tuple[int, int]]) -> hikari.Embed:
    embed = hikari.Embed(
        title="Bang xep hang",
        color=hikari.Color.from_hex_code("0000FF")
    )

    for index, (discord_id, balance) in enumerate(leaderboard_data, start=1):
        embed.add_field(
            name=f"{index}. {discord_id}: {balance}",
            inline=False,
        )

    return embed
