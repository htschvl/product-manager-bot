from bots.discord_bot.flows.flow_start import FlowStarter

class FlowManager:
    def __init__(self, bot):
        self.bot = bot
        self.initial_flow = FlowStarter(bot)

    async def start_flow(self, flow_name, user, channel):
        """
        Start the specified flow based on the flow name.
        """
        if flow_name == "initial":
            await self.initial_flow.start_flow(user, channel)
        else:
            await channel.send(f"{user.mention}, desconheço este fluxo: {flow_name}")
