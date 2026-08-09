import discord
from discord.ext import commands
from discord import app_commands
from models.Obter_Slowmode import Manipular_Slowmode
from models.Obter_Usuario import Manipular_Usuario


class SlowmodeNivel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if not message.guild:
            return
        # Ignora comandos do bot
        if message.content.startswith("$"):
            return

        nivel_minimo = Manipular_Slowmode.obter_nivel(
            str(message.guild.id), str(message.channel.id)
        )
        if nivel_minimo is None:
            return

        # Admins e quem gerencia o servidor não são afetados
        perms = message.channel.permissions_for(message.author)
        if perms.manage_messages or perms.manage_guild:
            return

        usuario = Manipular_Usuario.obter_usuario(str(message.author.id))
        nivel_usuario = usuario.level if usuario else 0
        if nivel_usuario >= nivel_minimo:
            return

        try:
            await message.delete()
        except discord.Forbidden:
            return

        aviso = (
            f"🔒 {message.author.mention}, você precisa ser **nível {nivel_minimo}** "
            f"para falar em {message.channel.mention}."
        )
        if not usuario:
            aviso += "\nUse `/registrar` para começar a ganhar XP!"
        try:
            mensagem_aviso = await message.channel.send(aviso)
            await mensagem_aviso.delete(delay=8)
        except discord.Forbidden:
            pass

    @app_commands.command(
        name="configurar_slowmode",
        description="Define o nível mínimo para falar em um canal.",
    )
    @app_commands.describe(
        channel="O canal que terá a restrição.",
        nivel="Nível mínimo necessário (0 para remover a restrição).",
    )
    @app_commands.default_permissions(manage_guild=True)
    async def configurar_slowmode(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        nivel: int,
    ):
        if nivel < 0:
            await interaction.response.send_message(
                "❌ O nível mínimo não pode ser negativo.", ephemeral=True
            )
            return
        if nivel == 0:
            Manipular_Slowmode.remover_config(
                str(interaction.guild_id), str(channel.id)
            )
            await interaction.response.send_message(
                f"✅ Restrição de nível removida de {channel.mention}.",
                ephemeral=True,
            )
            return

        Manipular_Slowmode.configurar_nivel(
            str(interaction.guild_id), str(channel.id), nivel
        )
        await interaction.response.send_message(
            f"✅ {channel.mention} agora exige **nível {nivel}** para falar.",
            ephemeral=True,
        )

    @app_commands.command(
        name="listar_slowmodes",
        description="Lista os canais com nível mínimo configurado.",
    )
    @app_commands.default_permissions(manage_guild=True)
    async def listar_slowmodes(self, interaction: discord.Interaction):
        configs = Manipular_Slowmode.listar_configs(str(interaction.guild_id))
        if not configs:
            await interaction.response.send_message(
                "❌ Nenhum canal com restrição de nível neste servidor.",
                ephemeral=True,
            )
            return
        linhas = [
            f"<#{config.channel_id}> → nível **{config.nivel_minimo}**"
            for config in configs
        ]
        embed = discord.Embed(
            title="🔒 Slowmodes por nível",
            description="\n".join(linhas),
            color=discord.Color.orange(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(SlowmodeNivel(bot))
