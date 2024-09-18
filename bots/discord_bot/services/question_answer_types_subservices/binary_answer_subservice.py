import discord
from bots.discord_bot.components.binary_buttons_component import BinaryButtonsComponent
from bots.discord_bot.utils.message_handler import MessageHandler

class BinaryQuestionSubservice:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.message_handler = MessageHandler(bot)

    async def send_yes_no_question(self, user: discord.User, question: str, sim_callback, nao_callback):
        """
        Send a yes/no question to the user with 'Sim' and 'Não' buttons.
        
        Args:
            user (discord.User): The user to send the question to.
            question (str): The text of the yes/no question.
            sim_callback (function): The callback for when 'Sim' is clicked.
            nao_callback (function): The callback for when 'Não' is clicked.
        """
        try:
            # Utiliza o BinaryButtonsComponent para criar os botões de resposta
            view = BinaryButtonsComponent(sim_callback=sim_callback, nao_callback=nao_callback)
            await user.send(content=question, view=view)
        except discord.Forbidden:
            # Se não puder enviar a mensagem, logar e enviar um aviso
            await self.message_handler.handle_message_error(
                f"Não foi possível enviar a pergunta 'Sim/Não' para o usuário {user.name}."
            )
        except Exception as e:
            # Tratamento de outros erros
            await self.message_handler.handle_message_error(
                f"Ocorreu um erro ao enviar a pergunta para o usuário {user.name}: {e}"
            )
