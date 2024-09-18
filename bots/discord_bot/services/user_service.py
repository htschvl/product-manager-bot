import discord

class UserService:
    def __init__(self, bot: discord.Client):
        self.bot = bot

    async def fetch_user(self, user_id: int) -> discord.User:
        user = self.bot.get_user(user_id)
        if user is None:
            try:
                user = await self.bot.fetch_user(user_id)
            except discord.NotFound:
                print(f"User with ID {user_id} not found in Discord.")
                return None
        return user
