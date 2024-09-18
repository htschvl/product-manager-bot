import discord
from bots.discord_bot.services.question_service import QuestionService
from bots.discord_bot.utils.message_handler import MessageHandler

class PendencyFlow:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.question_service = QuestionService(bot)
        self.message_handler = MessageHandler(bot)

    async def start_flow(self, user: discord.User, channel: discord.TextChannel):
        """
        Start the Pendency flow, asking if the issue is inside or outside the company.
        """
        try:
            await self.ask_pendency_type(user, channel)
        except Exception as e:
            await self.message_handler.handle_message_error(f"Error in PendencyFlow for {user.name}: {e}")

    async def ask_pendency_type(self, user: discord.User, channel: discord.TextChannel):
        """
        Ask the user if the pendency is inside or outside the company.
        """
        buttons_info = [
            {"label": "Interna", "callback": self.handle_inside_pendency},
            {"label": "Externa", "callback": self.handle_outside_pendency},
        ]
        try:
            await self.question_service.send_dynamic_question(
                user=user,
                question="A pendência é externa à NearX ou interna?",
                buttons_info=buttons_info
            )
        except Exception as e:
            await self.message_handler.handle_message_error(f"Error asking pendency type for {user.name}: {e}")

    async def handle_inside_pendency(self, interaction: discord.Interaction):
        """
        Handle when the user selects 'Inside' (Interna).
        """
        try:
            await interaction.response.defer()

            # Pass the flow to InsidePendencyFlow
            from bots.discord_bot.flows.inside_pendency_flow import InsidePendencyFlow
            inside_pendency_flow = InsidePendencyFlow(self.bot)
            await inside_pendency_flow.start_flow(interaction.user, interaction.channel)
        except Exception as e:
            await self.message_handler.handle_message_error(f"Error handling inside pendency for {interaction.user.name}: {e}")

    async def handle_outside_pendency(self, interaction: discord.Interaction):
        """
        Handle when the user selects 'Outside' (Externa).
        """
        try:
            await interaction.response.defer()
            await interaction.channel.send(f"{interaction.user.mention}, entendi, pendências de fora da empresa. Vamos lidar com isso.")
        except Exception as e:
            await self.message_handler.handle_message_error(f"Error handling outside pendency for {interaction.user.name}: {e}")
