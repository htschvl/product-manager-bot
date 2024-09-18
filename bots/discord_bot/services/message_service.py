import discord
from bots.discord_bot.services.user_service import UserService
from bots.discord_bot.utils.time_utils import TimeUtils
from bots.discord_bot.flows.flow_manager import FlowManager
from bots.discord_bot.services.written_answer_service import WrittenAnswerService

class MessageService:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.user_service = UserService(bot)
        self.time_utils = TimeUtils()
        self.flow_manager = FlowManager(bot)
        self.written_answer_service = WrittenAnswerService(bot)
        self.current_mode = None  # To track whether we're in binary or written mode

    async def send_message_if_valid_time(self, user_id: int):
        """
        Sends a message to the user only if it's a valid time according to the TimeUtils.
        """
        if self.time_utils.is_valid_time():
            user = await self.user_service.fetch_user(user_id)

            if user is not None:
                try:
                    # Start the initial flow (which uses BinaryButtons)
                    await self.flow_manager.start_flow("initial", user, user.dm_channel)
                    self.current_mode = "binary"  # Binary mode is activated
                    print(f"Message with buttons sent to user {user_id}")
                except discord.Forbidden:
                    print(f"Cannot send messages to user {user_id}, permission error.")
            else:
                print(f"User with ID {user_id} not found.")
        else:
            print("It's not a valid time to send messages.")

    async def handle_written_response(self, user: discord.User, channel: discord.TextChannel):
        """
        Handle written response, ensuring mutual exclusivity with BinaryButtons.
        """
        if self.current_mode != "binary":
            await self.written_answer_service.prompt_for_answer(user, channel)
            self.current_mode = "written"  # Set to written mode
        else:
            await channel.send("Cannot process written responses while awaiting button selection.")

    async def handle_binary_response(self, user: discord.User, interaction: discord.Interaction):
        """
        Handle binary button response (Yes/No), ensuring mutual exclusivity with WrittenAnswerService.
        """
        if self.current_mode != "written":
            # Process binary response and reset mode for the next interaction
            await interaction.response.send_message("Processing your selection...", ephemeral=True)
            self.current_mode = "binary"
        else:
            await interaction.response.send_message("Cannot interact with buttons while expecting a written response.", ephemeral=True)

    def reset_mode(self):
        """
        Resets the current mode after a flow or interaction completes, allowing a new interaction.
        """
        self.current_mode = None
