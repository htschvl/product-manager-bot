import discord
import logging

class DynamicButtonsComponent(discord.ui.View):
    def __init__(self, buttons_info):
        """
        Initialize the DynamicButtons view with dynamic button labels and callbacks.

        Args:
            buttons_info (list of dict): A list of dictionaries with 'label' and 'callback'.
                Example:
                [
                    {"label": "Option 1", "callback": some_callback_function},
                    {"label": "Option 2", "callback": another_callback_function},
                ]
        """
        super().__init__(timeout=None)
        self.logger = logging.getLogger(__name__)
        
        for button_info in buttons_info:
            label = button_info["label"]
            callback = button_info["callback"]
            self.add_item(GenericButton(label, callback))

class GenericButton(discord.ui.Button):
    def __init__(self, label, callback):
        """
        Initialize a generic button with a dynamic label and callback function.
        """
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.callback_function = callback
        self.logger = logging.getLogger(__name__)

    async def callback(self, interaction: discord.Interaction):
        """
        Executes the provided callback for the button and handles any exceptions.
        """
        try:
            await self.callback_function(interaction)
        except Exception as e:
            # Log the error and notify the user if the callback fails
            self.logger.exception(f"Error in button '{self.label}' callback: {e}")
            await interaction.response.send_message("An error occurred while processing your response. Please try again later.", ephemeral=True)
