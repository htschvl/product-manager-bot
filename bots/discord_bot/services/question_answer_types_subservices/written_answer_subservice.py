import discord
from bots.discord_bot.utils.message_handler import MessageHandler
from bots.discord_bot.services.question_answer_types_subservices.binary_answer_subservice import BinaryQuestionSubservice

class WrittenAnswerSubservice:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.user_messages = {}  # Dicionário para armazenar a resposta do usuário
        self.message_handler = MessageHandler(bot)
        self.binary_question_service = BinaryQuestionSubservice(bot)  # Usando o subserviço de pergunta binária

    async def prompt_for_answer(self, user: discord.User, channel: discord.TextChannel, prompt: str):
        """
        Solicita que o usuário insira uma mensagem, aguarda a resposta e pede confirmação.

        Args:
            user (discord.User): O usuário que receberá o prompt.
            channel (discord.TextChannel): O canal onde o prompt será enviado.
            prompt (str): O texto do prompt que será enviado ao usuário.
        """
        try:
            # Enviar o prompt dinâmico
            await channel.send(f"{prompt}")

            # Aguarda a resposta do usuário
            def check(m):
                return m.author == user and m.channel == channel

            msg = await self.bot.wait_for('message', check=check, timeout=300)  # 5 minutos de timeout

            # Armazena a resposta e prossegue para confirmação
            self.user_messages[user.id] = msg.content
            await self.ask_for_confirmation(user, channel)

        except discord.TimeoutError:
            await channel.send(f"{user.mention}, você demorou muito para responder.")
        except Exception as e:
            await self.message_handler.handle_message_error(f"Erro ao solicitar resposta de {user.name}: {e}")

    async def ask_for_confirmation(self, user: discord.User, channel: discord.TextChannel):
        """
        Pede confirmação da resposta do usuário usando o subserviço de pergunta binária.
        """
        message_content = self.user_messages[user.id]

        # Usa o subserviço de pergunta binária para perguntar "Sim" ou "Não"
        await self.binary_question_service.send_yes_no_question(
            user=user,
            question=f"{user.mention}, esta é sua resposta final?\n\n**{message_content}**\n",
            sim_callback=lambda i: self.confirm_answer(i, user, channel),
            nao_callback=lambda i: self.ask_for_new_answer(i, user, channel)
        )

    async def ask_for_new_answer(self, interaction: discord.Interaction, user: discord.User, channel: discord.TextChannel):
        """
        Solicita que o usuário forneça uma nova resposta se ele clicar em 'Não'.
        """
        await interaction.response.defer()

        # Re-prompt para uma nova resposta
        await self.prompt_for_answer(user, channel, "Por favor, escreva uma nova resposta:")

    async def confirm_answer(self, interaction: discord.Interaction, user: discord.User, channel: discord.TextChannel):
        """
        Confirma a resposta do usuário quando ele clica em 'Sim'.
        """
        await interaction.response.defer()
        await self.save_answer(user, channel)

    async def save_answer(self, user: discord.User, channel: discord.TextChannel):
        """
        Salva a resposta do usuário (neste caso, apenas imprime no console).
        """
        answer = self.user_messages.get(user.id, "Nenhuma resposta encontrada.")
        print(f"Resposta final de {user.name}: {answer}")
        await channel.send(f"{user.mention}, sua resposta foi salva:\n\n**{answer}**")
