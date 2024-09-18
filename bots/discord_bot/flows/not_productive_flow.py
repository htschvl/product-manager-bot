import discord
from bots.discord_bot.services.question_service import QuestionService
from bots.discord_bot.utils.message_handler import MessageHandler

class NotProductiveFlow:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.question_service = QuestionService(bot)
        self.message_handler = MessageHandler(bot)

    async def start_flow(self, user: discord.User, channel: discord.TextChannel):
        """
        Start the 'Not Productive' flow by asking why the user wasn't productive.
        """
        try:
            await self.ask_reason_not_productive(user, channel)
        except Exception as e:
            await self.message_handler.handle_message_error(f"Error in NotProductiveFlow for {user.name}: {e}")

    async def ask_reason_not_productive(self, user: discord.User, channel: discord.TextChannel):
        """
        Ask the user why they were not productive using dynamic buttons.
        """
        buttons_info = [
            {"label": "Questões pessoais ou imprevistos", "callback": self.handle_personal_issues},
            {"label": "Pendências de outras partes", "callback": self.handle_external_dependencies},
        ]
        try:
            await self.question_service.send_dynamic_question(
                user=user,
                question="Por que você não conseguiu ser produtivo?",
                buttons_info=buttons_info
            )
        except Exception as e:
            await self.message_handler.handle_message_error(f"Error sending reason not productive question to {user.name}: {e}")

    async def handle_personal_issues(self, interaction: discord.Interaction):
        """
        Handle the flow for personal issues and proceed to the 'Personal Issues' flow.
        """
        from bots.discord_bot.flows.personal_issues_flow import PersonalIssuesFlow
        try:
            personal_issues_flow = PersonalIssuesFlow(self.bot)
            await interaction.response.defer()
            await personal_issues_flow.start_flow(interaction.user, interaction.channel)
        except Exception as e:
            await self.message_handler.handle_message_error(f"Error handling personal issues for {interaction.user.name}: {e}")

    async def handle_external_dependencies(self, interaction: discord.Interaction):
        """
        Handle the flow for external dependencies and proceed to the 'Pendency' flow.
        """
        from bots.discord_bot.flows.pendency_flow import PendencyFlow
        try:
            pendency_flow = PendencyFlow(self.bot)
            await interaction.response.defer()
            await pendency_flow.start_flow(interaction.user, interaction.channel)
        except Exception as e:
            await self.message_handler.handle_message_error(f"Error handling external dependencies for {interaction.user.name}: {e}")
