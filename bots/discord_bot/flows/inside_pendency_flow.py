import discord
from bots.discord_bot.services.question_service import QuestionService
from bots.discord_bot.utils.message_handler import MessageHandler

class InsidePendencyFlow:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.question_service = QuestionService(bot)
        self.message_handler = MessageHandler(bot)

    async def start_flow(self, user: discord.User, channel: discord.TextChannel):
        """
        Inicia o fluxo de 'Pendências Internas', perguntando qual departamento está envolvido.
        """
        try:
            await self.ask_department(user, channel)
        except Exception as e:
            await self.message_handler.handle_message_error(f"Erro no fluxo InsidePendencyFlow para {user.name}: {e}")

    async def ask_department(self, user: discord.User, channel: discord.TextChannel):
        """
        Pergunta ao usuário qual departamento está relacionado à pendência.
        """
        try:
            options = [
                "Tech", "Design", "Marketing", "Comercial", 
                "Social media", "Produção de conteúdo", 
                "Finanças", "RH", "Bizdev"
            ]
            await self.question_service.send_single_select_question(
                user=user,
                channel=channel,
                question="Qual setor está relacionado à pendência?",
                options=options,
                callback=self.handle_department_selection  # Passa o callback para lidar com a seleção
            )
        except Exception as e:
            await self.message_handler.handle_message_error(f"Erro ao enviar a pergunta de seleção de setor para {user.name}: {e}")

    async def handle_department_selection(self, interaction: discord.Interaction, selected_department: str):
        """
        Lida com a seleção do departamento e prossegue para solicitar os detalhes da pendência.
        """
        try:
            await interaction.response.send_message(f"Setor selecionado: {selected_department}.")
            await self.ask_pendency_details(interaction.user, interaction.channel)
        except Exception as e:
            await self.message_handler.handle_message_error(f"Erro ao lidar com a seleção de setor para {interaction.user.name}: {e}")

    async def ask_pendency_details(self, user: discord.User, channel: discord.TextChannel):
        """
        Solicita ao usuário detalhes sobre a pendência, incluindo a tarefa, pessoa responsável e tempo de atraso.
        """
        try:
            # Definir o prompt dinâmico para a resposta escrita
            prompt = (
                "Por favor, detalhe no seguinte formato:\n\n"
                "**Tarefa ou pendência:**\n"
                "**Pessoa responsável:**\n"
                "**Quanto tempo passou do prazo pedido:**"
            )
            # Passa o prompt dinâmico para o QuestionService
            await self.question_service.prompt_for_written_answer(user, channel, prompt)
        except Exception as e:
            await self.message_handler.handle_message_error(f"Erro ao solicitar detalhes da pendência de {user.name}: {e}")
