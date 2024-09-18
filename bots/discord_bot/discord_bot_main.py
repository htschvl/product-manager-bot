import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bots.discord_bot.services.message_service import MessageService
from bots.discord_bot.commands.ping import Ping

class DiscordBotInit:
    def __init__(self):
        # Load environment variables from .env
        load_dotenv()

        # Get the bot token from environment variables
        self.token = os.getenv("DISCORD_TOKEN")

        # Set up the required intents
        intents = discord.Intents.default()
        intents.message_content = True  # This is required to read message content
        intents.members = True  # Enable GUILD_MEMBERS intent to access server members

        # Initialize the bot with the correct intents
        self.bot = commands.Bot(command_prefix="!", intents=intents)

        # Create instances of service classes
        self.message_service = MessageService(self.bot)

        # Add bot event handlers
        self.bot.event(self.on_ready)

    async def on_ready(self):
        """Event triggered when the bot is ready."""
        print(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')
        
        # Load the Ping command
        await self.bot.add_cog(Ping(self.bot))

        # Try to send a message to the user if it's the right time
        user_id = 1036860548446429245
        await self.message_service.send_message_if_valid_time(user_id)

    def start(self):
        """Starts the bot and connects it to Discord."""
        self.bot.run(self.token)
