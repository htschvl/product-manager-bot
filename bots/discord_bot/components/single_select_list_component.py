import discord
import logging

class SingleSelectComponent(discord.ui.View):
    def __init__(self, options, callback):
        """
        Initialize the SingleSelectView with options and a callback function.

        Args:
            options (list): A list of options (strings) that the user can choose from.
            callback (function): The function to call when an option is selected.
        """
        super().__init__(timeout=None)
        self.logger = logging.getLogger(__name__)  # Logger para capturar erros

        # Adiciona o Select Menu com as opções fornecidas e o callback
        self.add_item(
            SingleSelectMenu(options, callback)
        )


class SingleSelectMenu(discord.ui.Select):
    def __init__(self, options, callback):
        """
        Initialize the SingleSelectMenu with a list of options and a callback function.

        Args:
            options (list): A list of options (strings) that the user can choose from.
            callback (function): The function to call when an option is selected.
        """
        super().__init__(
            placeholder="Selecione uma opção",
            options=[discord.SelectOption(label=option) for option in options],
            min_values=1,  # O mínimo de uma seleção
            max_values=1   # O máximo de uma seleção
        )
        self.callback_function = callback
        self.logger = logging.getLogger(__name__)

    async def callback(self, interaction: discord.Interaction):
        """
        Executes the provided callback when an option is selected, with error handling.
        """
        try:
            selected_option = self.values[0]  # Obtém a opção selecionada
            await self.callback_function(interaction, selected_option)  # Chama o callback com a seleção
        except Exception as e:
            # Captura e loga qualquer erro que ocorra durante o processamento do callback
            self.logger.exception(f"Error in SingleSelectMenu callback: {e}")
            await interaction.response.send_message("Ocorreu um erro ao processar sua seleção. Por favor, tente novamente mais tarde.", ephemeral=True)
