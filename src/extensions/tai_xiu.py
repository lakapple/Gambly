import arc

plugin = arc.GatewayPlugin("tai_xiu")

@arc.loader
def loader(client: arc.GatewayClient):
    client.add_plugin(plugin)
