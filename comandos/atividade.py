import discord
from discord.ext import commands
from discord import app_commands
from models.Obter_Atividade import Manipular_Atividade


class Atividade(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if not message.guild:
            return
        if message.content.startswith("$"):
            return
        try:
            Manipular_Atividade.registrar_mensagem(
                str(message.author.id), str(message.guild.id)
            )
        except Exception as e:
            print(f"Erro ao registrar atividade: {e}")

    @app_commands.command(
        name="atividade",
        description="Mostra suas estatísticas de atividade no servidor.",
    )
    async def atividade(self, interaction: discord.Interaction):
        dados = Manipular_Atividade.obter_atividade_usuario(
            str(interaction.user.id), str(interaction.guild_id)
        )
        embed = discord.Embed(
            title=f"📊 Atividade de {interaction.user.display_name}",
            color=discord.Color.teal(),
        )
        embed.add_field(name="Mensagens hoje", value=f"`{dados['hoje']}`", inline=True)
        embed.add_field(
            name="Mensagens total", value=f"`{dados['total']}`", inline=True
        )
        embed.add_field(
            name="Dias ativos", value=f"`{dados['dias_ativos']}`", inline=True
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="top_atividade",
        description="Mostra os membros mais ativos do servidor hoje.",
    )
    async def top_atividade(self, interaction: discord.Interaction):
        top_hoje = Manipular_Atividade.top_hoje(str(interaction.guild_id), 10)
        if not top_hoje:
            await interaction.response.send_message(
                "❌ Ainda não há atividade registrada hoje.", ephemeral=True
            )
            return

        embed = discord.Embed(
            title="🔥 Mais ativos hoje",
            color=discord.Color.red(),
        )
        medalhas = ["🥇", "🥈", "🥉"]
        for posicao, registro in enumerate(top_hoje, start=1):
            membro = interaction.guild.get_member(int(registro.id_discord))
            nome = membro.display_name if membro else registro.id_discord
            simbolo = medalhas[posicao - 1] if posicao <= 3 else f"`{posicao}.`"
            embed.add_field(
                name=f"{simbolo} {nome}",
                value=f"{registro.mensagens} mensagens",
                inline=False,
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="top_atividade_total",
        description="Mostra os membros mais ativos no total do servidor.",
    )
    async def top_atividade_total(self, interaction: discord.Interaction):
        top_total = Manipular_Atividade.top_total(str(interaction.guild_id), 10)
        if not top_total:
            await interaction.response.send_message(
                "❌ Ainda não há atividade registrada neste servidor.",
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title="🔥 Mais ativos no total",
            color=discord.Color.red(),
        )
        medalhas = ["🥇", "🥈", "🥉"]
        for posicao, (id_discord, total) in enumerate(top_total, start=1):
            membro = interaction.guild.get_member(int(id_discord))
            nome = membro.display_name if membro else id_discord
            simbolo = medalhas[posicao - 1] if posicao <= 3 else f"`{posicao}.`"
            embed.add_field(
                name=f"{simbolo} {nome}",
                value=f"{total} mensagens",
                inline=False,
            )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Atividade(bot))
