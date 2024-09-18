import discord
from bots.discord_bot.components.binary_buttons import BinaryButtons

class WrittenAnswerService:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.user_messages = {}  # Dictionary to track the user's response state

    async def prompt_for_answer(self, user: discord.User, channel: discord.TextChannel):
        """
        Prompts the user to enter a message, waits for the response, and asks for confirmation.
        """
        await channel.send(f"{user.mention}, por favor, escreva sua resposta:")

        def check(m):
            return m.author == user and m.channel == channel

        # Wait for the user's message
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=300)  # 5-minute timeout
        except discord.TimeoutError:
            await channel.send(f"{user.mention}, você demorou muito para responder.")
            return

        # Store the message and ask for confirmation with Yes/No buttons
        self.user_messages[user.id] = msg.content
        await self.ask_for_confirmation(user, channel)

    async def ask_for_confirmation(self, user: discord.User, channel: discord.TextChannel):
        """
        Asks the user if they want to confirm the message they sent using Yes/No buttons.
        """
        message_content = self.user_messages[user.id]
        view = BinaryButtons(
            sim_callback=lambda i: self.confirm_answer(i, user, channel),
            nao_callback=lambda i: self.ask_for_new_answer(i, user, channel)
        )

        # Send the confirmation message with the Yes/No buttons
        await channel.send(
            content=f"{user.mention}, esta é sua resposta final? \n\n**{message_content}**\n",
            view=view
        )

    async def ask_for_new_answer(self, interaction: discord.Interaction, user: discord.User, channel: discord.TextChannel):
        """
        Asks the user to provide a new answer if they clicked 'No'.
        """
        await interaction.response.defer()

        # Re-prompt the user to enter a new answer
        await channel.send(f"{user.mention}, por favor, escreva uma nova resposta:")

        def check(m):
            return m.author == user and m.channel == channel

        try:
            # Wait for the user's new message
            msg = await self.bot.wait_for('message', check=check, timeout=300)
        except discord.TimeoutError:
            await channel.send(f"{user.mention}, você demorou muito para responder.")
            return

        # Store the new message and ask for confirmation again
        self.user_messages[user.id] = msg.content
        await self.ask_for_confirmation(user, channel)

    async def confirm_answer(self, interaction: discord.Interaction, user: discord.User, channel: discord.TextChannel):
        """
        Confirms the user's answer when they click 'Yes'.
        """
        await interaction.response.defer()
        await self.save_answer(user, channel)

    async def save_answer(self, user: discord.User, channel: discord.TextChannel):
        """
        Saves the user's answer (for now just prints it to the console).
        """
        answer = self.user_messages.get(user.id, "No answer found.")
        print(f"User {user.name}'s final answer: {answer}")
        await channel.send(f"{user.mention}, sua resposta foi salva: \n\n**{answer}**")
        # Further logic for saving the answer can be implemented here
