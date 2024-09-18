import discord
import logging

class BinaryButtonsComponent(discord.ui.View):
    def __init__(self, sim_callback, nao_callback):
        """
        Initialize the BinaryButtons view with dynamic callbacks for 'Sim' and 'Não' buttons.

        Args:
            sim_callback (function): The function to call when 'Sim' is clicked.
            nao_callback (function): The function to call when 'Não' is clicked.
        """
        super().__init__(timeout=None)
        self.add_item(SimButton(sim_callback))
        self.add_item(NaoButton(nao_callback))


class SimButton(discord.ui.Button):
    def __init__(self, callback):
        """
        Initialize the 'Sim' button with success style and check emoji.
        """
        super().__init__(label="Sim", style=discord.ButtonStyle.success, emoji="✅")
        self.callback_function = callback
        self.logger = logging.getLogger(__name__)

    async def callback(self, interaction: discord.Interaction):
        """
        Executes the provided callback for the 'Sim' button and handles any exceptions.
        """
        try:
            await self.callback_function(interaction)
        except Exception as e:
            # Log the error and notify the user if the callback fails
            self.logger.exception(f"Error in 'Sim' button callback: {e}")
            await interaction.response.send_message("An error occurred while processing your response. Please try again later.", ephemeral=True)


class NaoButton(discord.ui.Button):
    def __init__(self, callback):
        """
        Initialize the 'Não' button with danger style and cross emoji.
        """
        super().__init__(label="Não", style=discord.ButtonStyle.danger, emoji="❌")
        self.callback_function = callback
        self.logger = logging.getLogger(__name__)

    async def callback(self, interaction: discord.Interaction):
        """
        Executes the provided callback for the 'Não' button and handles any exceptions.
        """
        try:
            await self.callback_function(interaction)
        except Exception as e:
            # Log the error and notify the user if the callback fails
            self.logger.exception(f"Error in 'Não' button callback: {e}")
            await interaction.response.send_message("An error occurred while processing your response. Please try again later.", ephemeral=True)
