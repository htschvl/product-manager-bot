import discord
import logging

class MultiSelectListComponent(discord.ui.View):
    def __init__(self, options, callback):
        """
        Initialize the MultiSelectView with multiple options and a callback function.

        Args:
            options (list): A list of options (strings) that the user can choose from.
            callback (function): The function to call when one or more options are selected.
        """
        super().__init__(timeout=None)
        self.logger = logging.getLogger(__name__)  # Logger para capturar erros

        # Adiciona um Select Menu com as opções fornecidas
        self.add_item(MultiSelectMenu(options, callback))


class MultiSelectMenu(discord.ui.Select):
    def __init__(self, options, callback):
        """
        Initialize the MultiSelectMenu with a list of options and a callback function.

        Args:
            options (list): A list of options (strings) that the user can choose from.
            callback (function): The function to call when one or more options are selected.
        """
        super().__init__(
            placeholder="Selecione uma ou mais opções",
            options=[discord.SelectOption(label=option) for option in options],
            min_values=1,  # O mínimo de uma seleção
            max_values=len(options)  # O máximo é o número total de opções
        )
        self.callback_function = callback
        self.logger = logging.getLogger(__name__)

    async def callback(self, interaction: discord.Interaction):
        """
        Executes the provided callback when one or more options are selected, with error handling.
        """
        try:
            selected_options = self.values  # Obtém as opções selecionadas (pode ser mais de uma)
            await self.callback_function(interaction, selected_options)
        except Exception as e:
            # Captura e loga qualquer erro que ocorra durante o processamento do callback
            self.logger.exception(f"Error in MultiSelectMenu callback: {e}")
            await interaction.response.send_message("An error occurred while processing your selection. Please try again later.", ephemeral=True)
