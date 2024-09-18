import discord
from bots.discord_bot.services.question_service import QuestionService

class FlowStarter:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.question_service = QuestionService(bot)

    async def start_flow(self, user: discord.User, channel: discord.TextChannel):
        """
        Start the initial flow by asking if the user was productive today.
        """
        await self.question_service.send_yes_no_question(
            user=user,
            question="Você sente que conseguiu trabalhar e produzir hoje?",
            sim_callback=self.handle_productive_response,
            nao_callback=self.handle_not_productive_response
        )

    async def handle_productive_response(self, interaction: discord.Interaction):
        """
        Handle the case where the user says they were productive.
        """
        await interaction.response.send_message("Parabéns! Que você continue assim.", ephemeral=True)

    async def handle_not_productive_response(self, interaction: discord.Interaction):
        """
        Handle the case where the user says they were not productive.
        Proceed to the 'Not Productive' flow.
        """
        from bots.discord_bot.flows.flow_not_productive import NotProductiveFlow
        not_productive_flow = NotProductiveFlow(self.bot)
        await interaction.response.defer()
        await not_productive_flow.start_flow(interaction.user, interaction.channel)
