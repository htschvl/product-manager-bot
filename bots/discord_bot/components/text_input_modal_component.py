import discord
import logging

class TextInputModalComponent(discord.ui.Modal):
    def __init__(self, title: str, callback):
        """
        Initialize the TextInputPopup with a title and a callback function.

        Args:
            title (str): The title of the popup.
            callback (function): The function to call when the user submits their input.
        """
        super().__init__(title=title)
        self.logger = logging.getLogger(__name__)  # Logger para capturar erros

        # Adiciona um campo de texto para o usuário preencher
        self.text_input = discord.ui.TextInput(label="Digite sua resposta", style=discord.TextStyle.paragraph)
        self.add_item(self.text_input)

        # Callback será chamado quando o usuário enviar o texto
        self.callback_function = callback

    async def on_submit(self, interaction: discord.Interaction):
        """
        Executes the provided callback when the user submits their input, with error handling.
        """
        try:
            user_input = self.text_input.value  # Captura a resposta do usuário
            await self.callback_function(interaction, user_input)  # Passa a resposta para o callback
        except Exception as e:
            # Captura e loga qualquer erro que ocorra durante o processamento do callback
            self.logger.exception(f"Error in TextInputPopup submission: {e}")
            await interaction.response.send_message("An error occurred while processing your input. Please try again later.", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        """
        Handles any errors that occur during the modal interaction.
        """
        # Loga o erro para depuração
        self.logger.exception(f"Unexpected error in TextInputPopup: {error}")
        # Notifica o usuário sobre o erro
        await interaction.response.send_message("An unexpected error occurred. Please try again later.", ephemeral=True)
