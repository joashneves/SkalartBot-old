import discord
from discord.ext import commands
from discord import app_commands
from models.Obter_Sugestao import Manipular_Sugestao


class Sugestoes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="configurar_sugestao",
        description="Configura o canal onde as sugestões serão enviadas.",
    )
    @app_commands.describe(channel="O canal para receber sugestões.")
    @app_commands.default_permissions(manage_guild=True)
    async def configurar_sugestao(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        Manipular_Sugestao.configurar_canal(str(interaction.guild_id), str(channel.id))
        await interaction.response.send_message(
            f"Canal {channel.mention} configurado para sugestões!", ephemeral=True
        )

    @app_commands.command(
        name="sugestao",
        description="Envia uma sugestão para o canal de sugestões do servidor.",
    )
    @app_commands.describe(texto="O conteúdo da sua sugestão.")
    async def sugestao(self, interaction: discord.Interaction, texto: str):
        canal_id = Manipular_Sugestao.obter_canal(str(interaction.guild_id))
        if not canal_id:
            await interaction.response.send_message(
                "❌ Este servidor ainda não configurou um canal de sugestões. "
                "Peça a um administrador para usar `/configurar_sugestao`.",
                ephemeral=True,
            )
            return

        canal = interaction.guild.get_channel(int(canal_id))
        if not canal:
            await interaction.response.send_message(
                "❌ O canal de sugestões configurado não existe mais. "
                "Peça a um administrador para reconfigurar.",
                ephemeral=True,
            )
            return

        sugestao = Manipular_Sugestao.criar_sugestao(
            str(interaction.guild_id),
            str(interaction.user.id),
            texto,
            str(canal.id),
        )

        embed = discord.Embed(
            title="💡 Nova Sugestão",
            description=texto,
            color=discord.Color.blurple(),
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url,
        )
        embed.set_footer(text=f"Sugestão #{sugestao.id}")

        mensagem = await canal.send(embed=embed)
        Manipular_Sugestao.vincular_mensagem(sugestao.id, str(mensagem.id))
        await mensagem.add_reaction("👍")
        await mensagem.add_reaction("👎")

        await interaction.response.send_message(
            f"✅ Sugestão enviada em {canal.mention}!", ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Sugestoes(bot))
