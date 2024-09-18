from bots.discord_bot.services.user_service import UserService
from bots.discord_bot.utils.time_utils import TimeUtils
import discord

class MessageService:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.user_service = UserService(bot)
        self.time_utils = TimeUtils()

    async def send_message_if_valid_time(self, user_id: int):
        if self.time_utils.is_valid_time():
            user = await self.user_service.fetch_user(user_id)
            
            if user is not None:
                try:
                    await user.send("Hello! It's a weekday and within the valid time, have a productive day!")
                    print(f"Message sent to user {user_id}")
                except discord.Forbidden:
                    print(f"Cannot send messages to user {user_id}, permission error.")
            else:
                print(f"User with ID {user_id} not found.")
        else:
            print("It's not a valid time to send messages.")
