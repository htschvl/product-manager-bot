import discord

class DynamicButtons(discord.ui.View):
    def __init__(self, buttons_info):
        """
        Initialize the GenericButtons view with dynamic button labels and callbacks.

        Args:
            buttons_info (list of dict): A list of dictionaries with 'label' and 'callback'.
                Example:
                [
                    {"label": "Option 1", "callback": some_callback_function},
                    {"label": "Option 2", "callback": another_callback_function},
                ]
        """
        super().__init__(timeout=None)
        for button_info in buttons_info:
            label = button_info["label"]
            callback = button_info["callback"]
            self.add_item(GenericButton(label, callback))

class GenericButton(discord.ui.Button):
    def __init__(self, label, callback):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.callback_function = callback

    async def callback(self, interaction: discord.Interaction):
        await self.callback_function(interaction)
