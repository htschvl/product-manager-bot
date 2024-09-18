import discord
from discord import app_commands
from discord.ext import commands
from bots.discord_bot.flows.manager_flow import FlowManager

class SendReport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.flow_manager = FlowManager(bot)

    # This is the only command that works for now
    @app_commands.command(name="enviar_relatorio_diario", description="Envia seu relatório diário")
    async def send_daily_report(self, interaction: discord.Interaction):
        """Slash command to start the daily report flow"""
        user = interaction.user
        channel = interaction.channel

        await interaction.response.send_message(f"{user.mention}, iniciando o fluxo de envio do relatório diário.", ephemeral=True)
        await self.flow_manager.start_flow("initial", user, channel)

    # Placeholder commands
    @app_commands.command(name="enviar_planos_semanais", description="Envia seu relatório do que tem de atividades para a semana")
    async def send_weekly_start_report(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Placeholder: Relatório do início da semana enviado!", ephemeral=True)

    @app_commands.command(name="enviar_relatorio_semanal", description="Envia o que você fez na semana")
    async def send_weekly_end_report(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Placeholder: Relatório do final da semana enviado!", ephemeral=True)

    @app_commands.command(name="enviar_relatorio_mensal", description="Envia suas maiores conquistas do mês")
    async def send_monthly_report(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Placeholder: Relatório mensal enviado!", ephemeral=True)

    @app_commands.command(name="reportar_gargalo", description="Alerta Clarice, Caio e Junior de gargalo na produtividade")
    async def report_productivity_bottleneck(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Placeholder: Gargalo de produtividade reportado para Clarice, Caio e Junior.", ephemeral=True)

    @app_commands.command(name="aviso_previo_compromissos", description="Avisa o time de compromissos pessoais e quando precisará se ausentar")
    async def notify_personal_commitments(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Placeholder: Compromissos pessoais notificados.", ephemeral=True)

    async def setup(self):
        self.bot.tree.add_command(self.send_daily_report)
        self.bot.tree.add_command(self.send_weekly_start_report)
        self.bot.tree.add_command(self.send_weekly_end_report)
        self.bot.tree.add_command(self.send_monthly_report)
        self.bot.tree.add_command(self.report_productivity_bottleneck)
        self.bot.tree.add_command(self.notify_personal_commitments)
        await self.bot.tree.sync()

def setup(bot):
    bot.add_cog(SendReport(bot))
