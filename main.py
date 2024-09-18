from bots.discord_bot.discord_bot_main import DiscordBotInit

if __name__ == "__main__":
    # Initialize and start the Discord bot service
    discord_bot_service = DiscordBotInit()
    discord_bot_service.start()
