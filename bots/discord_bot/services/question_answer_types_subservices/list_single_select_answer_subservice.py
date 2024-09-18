import discord
from bots.discord_bot.components.single_select_list_component import SingleSelectComponent

class ListSingleSelectAnswerSubservice:
    def __init__(self, bot: discord.Client):
        self.bot = bot

    async def prompt_single_select(self, user: discord.User, channel: discord.TextChannel, options: list, question: str, callback):
        """
        Prompt the user to select a single option from the given list and pass the callback.
        
        Args:
            user (discord.User): The user being prompted.
            channel (discord.TextChannel): The channel to send the question to.
            options (list): A list of options to select from.
            question (str): The question to display.
            callback (function): The function to call when the user selects an option.
        """
        try:
            view = SingleSelectComponent(options, callback)
            await channel.send(f"{user.mention}, {question}", view=view)
        except Exception as e:
            print(f"Error sending single select question to {user.name}: {e}")
