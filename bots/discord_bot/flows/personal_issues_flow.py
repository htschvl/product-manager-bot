import discord
from bots.discord_bot.services.question_service import QuestionService
from bots.discord_bot.utils.message_handler import MessageHandler
from bots.discord_bot.services.question_answer_types_subservices.written_answer_subservice import WrittenAnswerSubservice

class PersonalIssuesFlow:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.question_service = QuestionService(bot)
        self.written_answer_service = WrittenAnswerSubservice(bot)
        self.message_handler = MessageHandler(bot)

    async def start_flow(self, user: discord.User, channel: discord.TextChannel):
        """
        Start the 'Personal Issues' flow by asking if the user wants to share their issues.
        """
        try:
            await self.question_service.send_yes_no_question(
                user=user,
                question="Caso queira dizer o que houve, selecione 'Sim'. Não há pressão. Somente Junior e Caio saberão.",
                sim_callback=self.handle_yes_response,
                nao_callback=self.handle_no_response
            )
        except Exception as e:
            await self.message_handler.handle_message_error(f"Error starting PersonalIssuesFlow for {user.name}: {e}")

    async def handle_yes_response(self, interaction: discord.Interaction):
        """
        Handle 'Yes' response, prompt the user for written feedback.
        """
        try:
            await interaction.response.defer()

            # Add the prompt string when calling the written answer service
            prompt = (
                "O que houve?"
            )
            await self.written_answer_service.prompt_for_answer(interaction.user, interaction.channel, prompt)
        except Exception as e:
            await self.message_handler.handle_message_error(f"Error handling 'Yes' response for {interaction.user.name}: {e}")

    async def handle_no_response(self, interaction: discord.Interaction):
        """
        Handle 'No' response.
        """
        try:
            await interaction.response.defer()
            await interaction.followup.send("Espero que tudo fique bem. Até a próxima.", ephemeral=True)
        except Exception as e:
            await self.message_handler.handle_message_error(f"Error handling 'No' response for {interaction.user.name}: {e}")
