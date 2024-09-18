import discord
from bots.discord_bot.components.binary_buttons import BinaryButtons
from bots.discord_bot.components.dynamic_buttons import DynamicButtons

class QuestionService:
    def __init__(self, bot: discord.Client):
        self.bot = bot

    async def send_yes_no_question(self, user: discord.User, question: str, sim_callback, nao_callback):
        """
        Send a yes/no question to the user with 'Sim' and 'Não' buttons.
        
        Args:
            user (discord.User): The user to send the question to.
            question (str): The text of the yes/no question.
            sim_callback (function): The callback for when 'Sim' is clicked.
            nao_callback (function): The callback for when 'Não' is clicked.
        """
        view = BinaryButtons(sim_callback=sim_callback, nao_callback=nao_callback)
        await user.send(content=question, view=view)

    async def send_dynamic_question(self, user: discord.User, question: str, buttons_info: list):
        """
        Send a dynamic question to the user with custom buttons.
        
        Args:
            user (discord.User): The user to send the question to.
            question (str): The text of the question.
            buttons_info (list of dict): A list of dictionaries with 'label' and 'callback'.
        """
        view = DynamicButtons(buttons_info)
        await user.send(content=question, view=view)

    # Example flow: Handling a "No" response
    async def handle_no_response(self, interaction: discord.Interaction):
        buttons_info = [
            {"label": "Questões pessoais ou imprevistos", "callback": self.handle_personal_issues},
            {"label": "Pendências de outras partes", "callback": self.handle_external_dependencies},
        ]
        view = DynamicButtons(buttons_info)
        await interaction.response.send_message("Por quê?", view=view, ephemeral=True)

    # Example: Handling "Questões pessoais ou imprevistos" response
    async def handle_personal_issues(self, interaction: discord.Interaction):
        buttons_info = [
            {"label": "Sim", "callback": self.handle_yes_personal_reason},
            {"label": "Não", "callback": self.handle_no_personal_reason},
        ]
        view = DynamicButtons(buttons_info)
        await interaction.response.send_message(
            "Caso queira dizer o que houve, selecione 'Sim'. Não há pressão. Somente Junior e Caio saberão.",
            view=view,
            ephemeral=True
        )

    async def handle_external_dependencies(self, interaction: discord.Interaction):
        await interaction.response.send_message("Ok, entendido.", ephemeral=True)

    async def handle_yes_personal_reason(self, interaction: discord.Interaction):
        await interaction.response.send_message("Obrigado por compartilhar. Sua resposta será confidencial.", ephemeral=True)

    async def handle_no_personal_reason(self, interaction: discord.Interaction):
        await interaction.response.send_message("Espero que tudo fique bem. Até a próxima.", ephemeral=True)
