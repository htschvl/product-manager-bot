import discord
import logging

class MessageHandler:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    async def on_message(self, message: discord.Message):
        """
        Handles incoming messages. This method will be called every time a message is sent in a text channel.
        """
        try:
            if message.author == self.bot.user:
                return  # Ignora as mensagens enviadas pelo próprio bot

            # Logando a mensagem recebida
            self.logger.info(f"Message from {message.author}: {message.content}")

            # Processando comandos se houverem
            await self.bot.process_commands(message)

        except discord.HTTPException as http_error:
            self.logger.error(f"HTTPException: Failed to process message from {message.author}: {http_error}")
            await message.channel.send("There was an issue processing your message. Please try again later.")
        
        except discord.Forbidden as forbidden_error:
            self.logger.warning(f"Forbidden: Insufficient permissions to process message from {message.author}: {forbidden_error}")
            await message.channel.send("I don't have permission to read or respond in this channel.")

        except discord.NotFound as not_found_error:
            self.logger.error(f"NotFound: Unable to process message because it was not found: {not_found_error}")
        
        except Exception as general_error:
            self.logger.exception(f"Unexpected error when handling message from {message.author}: {general_error}")
            await message.channel.send("An unexpected error occurred while processing your message.")

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """
        Handles reactions added to messages.
        """
        try:
            if user == self.bot.user:
                return  # Ignora reações do próprio bot

            # Logando a reação recebida
            self.logger.info(f"Reaction {reaction.emoji} added by {user.name} to message {reaction.message.id}")

            # Ações baseadas na reação
            await reaction.message.channel.send(f"{user.name} reacted with {reaction.emoji}")

        except discord.Forbidden as forbidden_error:
            self.logger.warning(f"Forbidden: Insufficient permissions to handle reactions: {forbidden_error}")
        
        except Exception as general_error:
            self.logger.exception(f"Unexpected error when handling reaction by {user.name}: {general_error}")

    async def on_error(self, event_method, *args, **kwargs):
        """
        A generic error handler for all unhandled errors in Discord events.
        """
        self.logger.error(f"Error in {event_method}: {args} {kwargs}")

    async def handle_message_error(self, error_message: str):
        """
        Handles errors that occur when processing messages or reactions.
        """
        try:
            self.logger.error(error_message)
        except Exception as log_error:
            self.logger.exception(f"Failed to log error: {log_error}")
