import discord
from bots.discord_bot.components.multi_select_list_component import MultiSelectListComponent
from bots.discord_bot.utils.message_handler import MessageHandler

class ListMultiAnswerSelectSubservice:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.message_handler = MessageHandler(bot)

    async def prompt_multi_toggle(self, user: discord.User, channel: discord.TextChannel, options: list, question: str):
        """
        Prompt the user to select multiple options using toggle buttons.
        
        Args:
            user (discord.User): The user who will be prompted.
            channel (discord.TextChannel): The channel to send the selection message.
            options (list): A list of options for the user to toggle.
            question (str): The question or prompt to display to the user.
        """
        try:
            # Utiliza o MultiSelectListComponent para criar a lista de seleção múltipla
            view = MultiSelectListComponent(options)
            await channel.send(f"{user.mention}, {question}", view=view)
        except discord.Forbidden:
            # Se não puder enviar a mensagem, logar e enviar um aviso
            await self.message_handler.handle_message_error(
                f"Não foi possível enviar a pergunta de múltipla escolha para o usuário {user.name}."
            )
        except Exception as e:
            # Tratamento de outros erros
            await self.message_handler.handle_message_error(
                f"Ocorreu um erro ao enviar a pergunta de múltipla escolha para o usuário {user.name}: {e}"
            )
