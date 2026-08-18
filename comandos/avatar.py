import discord
from discord.ext import commands
from discord import app_commands
import os
import aiohttp
import hashlib
from datetime import datetime
from models.Obter_avatar import Manipular_Avatar

AVATAR_DIR = "imagens_avatars"
os.makedirs(AVATAR_DIR, exist_ok=True)


async def save_avatar_locally(url: str, user_id: str) -> str:
    avatar_filename = f"{user_id}_{hashlib.md5(url.encode()).hexdigest()}.png"
    avatar_path = os.path.join(AVATAR_DIR, avatar_filename)
    if os.path.exists(avatar_path):
        return avatar_path
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(avatar_path, "wb") as f:
                    f.write(await response.read())
                return avatar_path
            else:
                raise Exception(f"Erro ao baixar imagem: status {response.status}")


class AvatarView(discord.ui.View):
    def __init__(self, avatares, membro):
        super().__init__(timeout=60)
        self.avatares = avatares
        self.membro = membro
        self.index = 0

    async def update_message(self, interaction):
        avatar = self.avatares[self.index]
        embed = discord.Embed(
            title=f"Avatar de {self.membro.name}",
            description=f"Data: {avatar.data_arquivo.strftime('%d/%m/%Y')}",
        )
        embed.set_image(url=f"attachment://{os.path.basename(avatar.caminho_arquivo)}")
        avatar_file = discord.File(avatar.caminho_arquivo)
        await interaction.response.edit_message(
            embed=embed, attachments=[avatar_file], view=self
        )

    @discord.ui.button(label="Anterior", style=discord.ButtonStyle.primary)
    async def anterior(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.index = (self.index - 1) % len(self.avatares)
        await self.update_message(interaction)

    @discord.ui.button(label="Próximo", style=discord.ButtonStyle.primary)
    async def proximo(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.index = (self.index + 1) % len(self.avatares)
        await self.update_message(interaction)


class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx: commands.Context, membro: discord.Member = None):
        membro = membro or ctx.author
        user_id = str(membro.id)
        avatar_url = membro.display_avatar.url
        avatar_hash = hashlib.md5(avatar_url.encode()).hexdigest()

        ultimo_avatar = (
            Manipular_Avatar.listar_avatares(user_id)[0]
            if Manipular_Avatar.listar_avatares(user_id)
            else None
        )

        if ultimo_avatar and ultimo_avatar.hash_avatar == avatar_hash:
            avatares = Manipular_Avatar.listar_avatares(user_id)
            if not avatares:
                await ctx.send("Nenhum avatar salvo encontrado.")
                return

            if not os.path.exists(avatares[0].caminho_arquivo):
                await ctx.send("Arquivo de avatar não encontrado.")
                return

            embed = discord.Embed(
                title=f"Avatar de {membro.name}",
                description=f"Data: {avatares[0].data_arquivo.strftime('%d/%m/%Y')}",
            )
            embed.set_image(
                url=f"attachment://{os.path.basename(avatares[0].caminho_arquivo)}"
            )
            avatar_file = discord.File(avatares[0].caminho_arquivo)
            view = AvatarView(avatares, membro)
            await ctx.send(embed=embed, file=avatar_file, view=view)
        else:
            try:
                avatar_path = await save_avatar_locally(avatar_url, user_id)
                Manipular_Avatar.salvar_avatar(
                    user_id, avatar_path, avatar_hash, datetime.utcnow()
                )
                avatares = Manipular_Avatar.listar_avatares(user_id)
                embed = discord.Embed(
                    title=f"Avatar de {membro.name}",
                    description="Avatar atualizado e salvo com sucesso!",
                )
                embed.set_image(url=f"attachment://{os.path.basename(avatar_path)}")
                avatar_file = discord.File(avatar_path)
                view = AvatarView(avatares, membro)
                await ctx.send(embed=embed, file=avatar_file, view=view)
            except Exception as e:
                await ctx.send(f"Erro ao salvar o avatar: {e}")

    @app_commands.command(name="avatar", description="Exibe o avatar de um usuário.")
    @app_commands.describe(membro="O usuário cujo avatar será exibido.")
    async def avatar_slash(
        self, interaction: discord.Interaction, membro: discord.Member = None
    ):
        membro = membro or interaction.user
        user_id = str(membro.id)
        avatar_url = membro.display_avatar.url
        avatar_hash = hashlib.md5(avatar_url.encode()).hexdigest()

        ultimo_avatar = (
            Manipular_Avatar.listar_avatares(user_id)[0]
            if Manipular_Avatar.listar_avatares(user_id)
            else None
        )

        if ultimo_avatar and ultimo_avatar.hash_avatar == avatar_hash:
            avatares = Manipular_Avatar.listar_avatares(user_id)
            if not avatares:
                await interaction.response.send_message(
                    "Nenhum avatar salvo encontrado.", ephemeral=True
                )
                return

            if not os.path.exists(avatares[0].caminho_arquivo):
                await interaction.response.send_message(
                    "Arquivo de avatar não encontrado.", ephemeral=True
                )
                return

            embed = discord.Embed(
                title=f"Avatar de {membro.name}",
                description=f"Data: {avatares[0].data_arquivo.strftime('%d/%m/%Y')}",
            )
            embed.set_image(
                url=f"attachment://{os.path.basename(avatares[0].caminho_arquivo)}"
            )
            avatar_file = discord.File(avatares[0].caminho_arquivo)
            view = AvatarView(avatares, membro)
            await interaction.response.send_message(
                embed=embed, file=avatar_file, view=view
            )
        else:
            try:
                avatar_path = await save_avatar_locally(avatar_url, user_id)
                Manipular_Avatar.salvar_avatar(
                    user_id, avatar_path, avatar_hash, datetime.utcnow()
                )
                avatares = Manipular_Avatar.listar_avatares(user_id)
                embed = discord.Embed(
                    title=f"Avatar de {membro.name}",
                    description="Avatar atualizado e salvo com sucesso!",
                )
                embed.set_image(url=f"attachment://{os.path.basename(avatar_path)}")
                avatar_file = discord.File(avatar_path)
                view = AvatarView(avatares, membro)
                await interaction.response.send_message(
                    embed=embed, file=avatar_file, view=view
                )
            except Exception as e:
                await interaction.response.send_message(
                    f"Erro ao salvar o avatar: {e}", ephemeral=True
                )


async def setup(bot):
    await bot.add_cog(Avatar(bot))
