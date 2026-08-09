import discord
from discord.ext import commands
from discord import app_commands
from models.Obter_Diario import Manipular_Diario
from models.Obter_Usuario import Manipular_Usuario


class Economia(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="daily", description="Resgata sua recompensa diária de moedas."
    )
    async def daily(self, interaction: discord.Interaction):
        id_discord = str(interaction.user.id)
        usuario = Manipular_Usuario.obter_usuario(id_discord)
        if not usuario:
            await interaction.response.send_message(
                "❌ Você não está registrado! Use `/registrar` primeiro.",
                ephemeral=True,
            )
            return

        resultado = Manipular_Diario.resgatar_daily(id_discord)
        if resultado is None:
            streak = Manipular_Diario.obter_streak(id_discord)
            await interaction.response.send_message(
                f"⏰ Você já resgatou o daily hoje! Sua streak atual é **{streak}** dias.\n"
                "Volte amanhã para continuar sua sequência.",
                ephemeral=True,
            )
            return

        moedas, streak = resultado
        Manipular_Usuario.adicionar_moedas(id_discord, moedas)
        embed = discord.Embed(
            title="💰 Daily resgatado!",
            description=f"Você recebeu **{moedas} moedas**!\n🔥 Streak: **{streak}** dia(s)",
            color=discord.Color.gold(),
        )
        embed.set_footer(text="Volte amanhã para mais moedas!")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="rank", description="Mostra o ranking do servidor por moedas ou XP."
    )
    @app_commands.describe(tipo="O critério do ranking (padrão: moedas)")
    @app_commands.choices(
        tipo=[
            app_commands.Choice(name="Moedas", value="moedas"),
            app_commands.Choice(name="XP", value="xp"),
        ]
    )
    async def rank(
        self,
        interaction: discord.Interaction,
        tipo: app_commands.Choice[str] = None,
    ):
        criterio = tipo.value if tipo else "moedas"
        usuarios = Manipular_Usuario.obter_todos_usuarios()

        if not usuarios:
            await interaction.response.send_message(
                "❌ Nenhum usuário registrado para mostrar no ranking.",
                ephemeral=True,
            )
            return

        # Filtra apenas membros do servidor atual
        membros = {str(m.id) for m in interaction.guild.members if not m.bot}
        ordenados = sorted(
            usuarios,
            key=lambda u: (getattr(u, criterio) if getattr(u, criterio) is not None else 0),
            reverse=True,
        )
        top = [u for u in ordenados if str(u.id_discord) in membros][:10]

        if not top:
            await interaction.response.send_message(
                "❌ Nenhum membro deste servidor está no ranking.", ephemeral=True
            )
            return

        titulo = "🏆 Ranking de Moedas" if criterio == "moedas" else "🏆 Ranking de XP"
        cor = discord.Color.gold() if criterio == "moedas" else discord.Color.purple()
        embed = discord.Embed(title=titulo, color=cor)

        medalhas = ["🥇", "🥈", "🥉"]
        for posicao, usuario in enumerate(top, start=1):
            apelido = usuario.apelido or usuario.id_discord
            valor = getattr(usuario, criterio) or 0
            simbolo = medalhas[posicao - 1] if posicao <= 3 else f"`{posicao}.`"
            unidade = " moedas" if criterio == "moedas" else " XP"
            embed.add_field(
                name=f"{simbolo} {apelido}",
                value=f"{valor}{unidade}",
                inline=False,
            )

        # Destaque para a posição do usuário que pediu
        posicao_usuario = next(
            (p for p, u in enumerate(ordenados, start=1) if str(u.id_discord) == str(interaction.user.id)),
            None,
        )
        if posicao_usuario:
            embed.set_footer(text=f"Sua posição geral: #{posicao_usuario}")

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Economia(bot))
