import discord
from bots.discord_bot.services.question_service import QuestionService

class NotProductiveFlow:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.question_service = QuestionService(bot)

    async def start_flow(self, user: discord.User, channel: discord.TextChannel):
        """
        Start the 'Not Productive' flow by asking why the user wasn't productive.
        """
        buttons_info = [
            {"label": "Questões pessoais ou imprevistos", "callback": self.handle_personal_issues},
            {"label": "Pendências de outras partes", "callback": self.handle_external_dependencies},
        ]
        await self.question_service.send_dynamic_question(
            user=user,
            question="Por que você não conseguiu ser produtivo?",
            buttons_info=buttons_info
        )

    async def handle_personal_issues(self, interaction: discord.Interaction):
        """
        Handle the flow for personal issues.
        Proceed to the 'Personal Issues' flow.
        """
        from bots.discord_bot.flows.flow_personal_issues import PersonalIssuesFlow
        personal_issues_flow = PersonalIssuesFlow(self.bot)
        await interaction.response.defer()
        await personal_issues_flow.start_flow(interaction.user, interaction.channel)

    async def handle_external_dependencies(self, interaction: discord.Interaction):
        """
        Handle external dependencies.
        """
        await interaction.response.send_message("Entendido, questões externas podem atrapalhar. Esperamos que melhore.", ephemeral=True)
