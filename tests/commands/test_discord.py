import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from discord.ext import commands
from bots.discord_bot.commands.ping import Ping
import discord

@pytest.mark.asyncio
async def test_ping():
    # Enable intents including message content
    intents = discord.Intents.default()
    intents.message_content = True

    # Initialize the bot with the correct intents
    bot = commands.Bot(command_prefix="!", intents=intents)

    # Add the Ping cog (await as it's async)
    ping_cog = Ping(bot)
    await bot.add_cog(ping_cog)

    # Mock the context
    ctx = MagicMock()
    ctx.bot = bot
    ctx.message = MagicMock()
    ctx.author = MagicMock()

    # Mock the context's send function as an async method
    ctx.send = AsyncMock()

    # Directly call the ping command
    await ping_cog.ping(ctx)

    # Check if the "Pong!" message was sent
    ctx.send.assert_called_once_with("Pong!")
