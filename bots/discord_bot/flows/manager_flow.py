import discord
from bots.discord_bot.flows.start_flow import FlowStarter
from bots.discord_bot.utils.message_handler import MessageHandler

class FlowManager:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.initial_flow = FlowStarter(bot)
        self.message_handler = MessageHandler(bot)

    async def start_flow(self, flow_name: str, user: discord.User, channel: discord.TextChannel):
        """
        Start the specified flow based on the flow name.
        Args:
            flow_name (str): The name of the flow to start.
            user (discord.User): The user to interact with.
            channel (discord.TextChannel): The channel where the flow is initiated.
        """
        try:
            if flow_name == "initial":
                await self.initial_flow.start_flow(user, channel)
            else:
                await channel.send(f"{user.mention}, desconheço este fluxo: {flow_name}")
        except Exception as e:
            await self.message_handler.handle_message_error(f"Error in FlowManager for {user.name} while starting flow '{flow_name}': {e}")
