import discord
from bots.discord_bot.services.question_service import QuestionService
from bots.discord_bot.services.written_answer_service import WrittenAnswerService

class PersonalIssuesFlow:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.question_service = QuestionService(bot)
        self.written_answer_service = WrittenAnswerService(bot)

    async def start_flow(self, user: discord.User, channel: discord.TextChannel):
        """
        Start the 'Personal Issues' flow by asking if the user wants to share their issues.
        """
        await self.question_service.send_yes_no_question(
            user=user,
            question="Caso queira dizer o que houve, selecione 'Sim'. Não há pressão. Somente Junior e Caio saberão.",
            sim_callback=self.handle_yes_response,
            nao_callback=self.handle_no_response
        )

    async def handle_yes_response(self, interaction: discord.Interaction):
        """
        Handle 'Yes' response, prompt the user for written feedback.
        """
        await interaction.response.send_message("O que houve? Por favor, escreva sua resposta.")
        await self.written_answer_service.prompt_for_answer(interaction.user, interaction.channel)

    async def handle_no_response(self, interaction: discord.Interaction):
        """
        Handle 'No' response.
        """
        await interaction.response.send_message("Espero que tudo fique bem. Até a próxima.", ephemeral=True)
