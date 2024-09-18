import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bots.discord_bot.services.send_timely_message_service import SendTimelyMessageService
from bots.discord_bot.commands.ping import Ping
from bots.discord_bot.utils.message_handler import MessageHandler
from bots.discord_bot.commands.send_report import SendReport  # Import the Slash command cog

class DiscordBotInit:
    def __init__(self):
        # Load environment variables from .env
        load_dotenv()

        # Get the bot token from environment variables
        self.token = os.getenv("DISCORD_TOKEN")

        # Set up the required intents
        intents = discord.Intents.default()
        intents.message_content = True  # Required to read message content
        intents.members = True  # Enable GUILD_MEMBERS intent to access server members

        # Initialize the bot with the correct intents
        self.bot = commands.Bot(command_prefix="!", intents=intents)

        # Create service instances
        self.message_service = SendTimelyMessageService(self.bot)
        self.message_handler = MessageHandler(self.bot)

        # Register event handlers
        self.bot.event(self.on_ready)
        self.bot.event(self.on_message)

    async def on_ready(self):
        """Event triggered when the bot is ready."""
        print(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')

        # Load the Ping command cog
        await self.bot.add_cog(Ping(self.bot))

        # Register and sync the Slash command cog
        await self.bot.add_cog(SendReport(self.bot))
        await self.bot.tree.sync()  # Sync the slash commands with Discord

        # Example: Try to send a message to a specific user if it's the right time
        user_id = 1036860548446429245  # Replace with the actual user ID
        await self.message_service.send_message_if_valid_time(user_id)

    async def on_message(self, message: discord.Message):
        """Handle incoming messages using the MessageHandler."""
        await self.message_handler.on_message(message)

    def start(self):
        """Start the bot and connect it to Discord."""
        if self.token:
            self.bot.run(self.token)
        else:
            print("Bot token not found in environment variables.")
