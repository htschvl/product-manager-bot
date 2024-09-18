import discord

class BinaryButtons(discord.ui.View):
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
        super().__init__(label="Sim", style=discord.ButtonStyle.success, emoji="✅")
        self.callback_function = callback

    async def callback(self, interaction: discord.Interaction):
        await self.callback_function(interaction)


class NaoButton(discord.ui.Button):
    def __init__(self, callback):
        super().__init__(label="Não", style=discord.ButtonStyle.danger, emoji="❌")
        self.callback_function = callback

    async def callback(self, interaction: discord.Interaction):
        await self.callback_function(interaction)
