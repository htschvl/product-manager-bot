import discord
from bots.discord_bot.services.question_answer_types_subservices.binary_answer_subservice import BinaryQuestionSubservice
from bots.discord_bot.services.question_answer_types_subservices.dynamic_answer_subservice import DynamicQuestionSubservice
from bots.discord_bot.services.question_answer_types_subservices.list_multi_select_answer_subservice import ListMultiAnswerSelectSubservice
from bots.discord_bot.services.question_answer_types_subservices.list_single_select_answer_subservice import ListSingleSelectAnswerSubservice
from bots.discord_bot.services.question_answer_types_subservices.written_answer_subservice import WrittenAnswerSubservice
from bots.discord_bot.utils.message_handler import MessageHandler

class QuestionService:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.binary_service = BinaryQuestionSubservice(bot)
        self.dynamic_service = DynamicQuestionSubservice(bot)
        self.single_select_service = ListSingleSelectAnswerSubservice(bot)
        self.multi_select_service = ListMultiAnswerSelectSubservice(bot)
        self.written_answer_service = WrittenAnswerSubservice(bot)
        self.message_handler = MessageHandler(bot)

    async def send_yes_no_question(self, user: discord.User, question: str, sim_callback, nao_callback):
        try:
            await self.binary_service.send_yes_no_question(user, question, sim_callback, nao_callback)
        except Exception as e:
            await self.message_handler.handle_message_error(f"Error sending Yes/No question to {user.name}: {e}")

    async def send_dynamic_question(self, user: discord.User, question: str, buttons_info: list):
        try:
            await self.dynamic_service.send_dynamic_question(user, question, buttons_info)
        except Exception as e:
            await self.message_handler.handle_message_error(f"Error sending dynamic question to {user.name}: {e}")

    async def send_single_select_question(self, user: discord.User, channel: discord.TextChannel, question: str, options: list, callback):
        """
        Envia uma pergunta com uma lista de seleção única, passando o callback ao componente responsável.
        """
        try:
            await self.single_select_service.prompt_single_select(user, channel, options, question, callback)
        except Exception as e:
            await self.message_handler.handle_message_error(f"Error sending single select question to {user.name}: {e}")

    async def send_multi_select_question(self, user: discord.User, channel: discord.TextChannel, question: str, options: list):
        try:
            await self.multi_select_service.prompt_multi_toggle(user, channel, options, question)
        except Exception as e:
            await self.message_handler.handle_message_error(f"Error sending multi-select question to {user.name}: {e}")

    async def prompt_for_written_answer(self, user: discord.User, channel: discord.TextChannel, prompt: str):
        """
        Solicita ao usuário uma resposta escrita com base em um prompt dinâmico.
        """
        try:
            await self.written_answer_service.prompt_for_answer(user, channel, prompt)
        except Exception as e:
            await self.message_handler.handle_message_error(f"Error requesting written answer from {user.name}: {e}")
