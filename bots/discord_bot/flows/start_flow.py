import discord
from bots.discord_bot.services.question_service import QuestionService
from bots.discord_bot.utils.message_handler import MessageHandler

class FlowStarter:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.question_service = QuestionService(bot)
        self.message_handler = MessageHandler(bot)

    async def start_flow(self, user: discord.User, channel: discord.TextChannel):
        try:
            await self.question_service.send_yes_no_question(
                user=user,
                question="Você sente que conseguiu trabalhar e produzir hoje?",
                sim_callback=self.handle_productive_response,
                nao_callback=self.handle_not_productive_response
            )
        except Exception as e:
            await self.message_handler.handle_message_error(f"Erro ao iniciar o fluxo: {e}")

    async def handle_productive_response(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message("Parabéns! Que você continue assim.", ephemeral=True)
        except Exception as e:
            await self.message_handler.handle_message_error(f"Erro ao enviar resposta produtiva: {e}")

    async def handle_not_productive_response(self, interaction: discord.Interaction):
        try:
            from bots.discord_bot.flows.not_productive_flow import NotProductiveFlow
            not_productive_flow = NotProductiveFlow(self.bot)
            await interaction.response.defer()
            await not_productive_flow.start_flow(interaction.user, interaction.channel)
        except Exception as e:
            await self.message_handler.handle_message_error(f"Erro ao iniciar o fluxo 'não produtivo': {e}")
