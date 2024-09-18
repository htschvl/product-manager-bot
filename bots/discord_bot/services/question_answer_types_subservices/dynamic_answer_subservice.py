import discord
from bots.discord_bot.components.dynamic_buttons_component import DynamicButtonsComponent
from bots.discord_bot.utils.message_handler import MessageHandler

class DynamicQuestionSubservice:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.message_handler = MessageHandler(bot)

    async def send_dynamic_question(self, user: discord.User, question: str, buttons_info: list):
        """
        Send a dynamic question to the user with custom buttons.
        
        Args:
            user (discord.User): The user to send the question to.
            question (str): The text of the question.
            buttons_info (list of dict): A list of dictionaries with 'label' and 'callback'.
                Example:
                [
                    {"label": "Option 1", "callback": some_callback_function},
                    {"label": "Option 2", "callback": another_callback_function},
                ]
        """
        try:
            # Utiliza o DynamicButtonsComponent para criar botões dinâmicos
            view = DynamicButtonsComponent(buttons_info)
            await user.send(content=question, view=view)
        except discord.Forbidden:
            # Se não puder enviar a mensagem, logar e enviar um aviso
            await self.message_handler.handle_message_error(
                f"Não foi possível enviar a pergunta dinâmica para o usuário {user.name}."
            )
        except Exception as e:
            # Tratamento de outros erros
            await self.message_handler.handle_message_error(
                f"Ocorreu um erro ao enviar a pergunta dinâmica para o usuário {user.name}: {e}"
            )
