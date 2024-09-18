import discord
from bots.discord_bot.services.user_service import UserService
from bots.discord_bot.utils.time_utils import TimeUtils
from bots.discord_bot.flows.manager_flow import FlowManager
from bots.discord_bot.services.question_answer_types_subservices.written_answer_subservice import WrittenAnswerSubservice
from bots.discord_bot.utils.message_handler import MessageHandler

class SendTimelyMessageService:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.user_service = UserService(bot)
        self.time_utils = TimeUtils()
        self.flow_manager = FlowManager(bot)
        self.written_answer_service = WrittenAnswerSubservice(bot)
        self.message_handler = MessageHandler(bot)
        self.current_mode = None  # Track current interaction mode (binary or written)

    async def send_message_if_valid_time(self, user_id: int):
        """
        Sends a message to the user if it's within a valid time window.
        """
        if self.time_utils.is_valid_time():
            user = await self.user_service.fetch_user(user_id)
            if user is not None:
                try:
                    # Start the initial flow, which handles binary button interaction
                    await self.flow_manager.start_flow("initial", user, user.dm_channel)
                    self.current_mode = "binary"
                    print(f"Message with buttons sent to user {user_id}")
                except discord.Forbidden:
                    print(f"Cannot send messages to user {user_id}, permission error.")
                except Exception as e:
                    await self.message_handler.handle_message_error(f"Failed to send message to {user.name}: {e}")
            else:
                print(f"User with ID {user_id} not found.")
        else:
            print("Not a valid time to send messages.")

    async def handle_written_response(self, user: discord.User, channel: discord.TextChannel):
        """
        Handles a written response, ensuring exclusivity with binary button interaction.
        """
        if self.current_mode != "binary":
            try:
                await self.written_answer_service.prompt_for_answer(user, channel)
                self.current_mode = "written"
            except Exception as e:
                await self.message_handler.handle_message_error(f"Error handling written response from {user.name}: {e}")
        else:
            await channel.send("Cannot process written responses while waiting for button selection.")

    async def handle_binary_response(self, interaction: discord.Interaction):
        """
        Handles a binary button (Yes/No) response, ensuring exclusivity with written interaction.
        """
        user = interaction.user
        if self.current_mode != "written":
            try:
                await interaction.response.send_message("Processing your selection...", ephemeral=True)
                # After processing, reset the mode for future interactions
                self.current_mode = "binary"
            except Exception as e:
                await self.message_handler.handle_message_error(f"Error handling binary response from {user.name}: {e}")
        else:
            await interaction.response.send_message("Cannot interact with buttons while expecting a written response.", ephemeral=True)

    def reset_mode(self):
        """
        Resets the current mode after completing an interaction, allowing new interactions.
        """
        self.current_mode = None
