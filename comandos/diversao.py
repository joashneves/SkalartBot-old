import discord
from discord.ext import commands
from discord import app_commands
import requests


MEME_API = "https://meme-api.com/gimme"
PIADA_API = "https://v2.jokeapi.dev/joke/Any?lang=pt&format=json"


class Diversao(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="meme", description="Envia um meme aleatório do Reddit."
    )
    async def meme(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            resposta = requests.get(MEME_API, timeout=10)
            resposta.raise_for_status()
            dados = resposta.json()
            titulo = dados.get("title", "Meme aleatório")
            url_imagem = dados.get("url")
            link_post = dados.get("postLink", "")
            subreddit = dados.get("subreddit", "memes")

            embed = discord.Embed(
                title=f"😂 {titulo}",
                color=discord.Color.blue(),
                url=link_post,
            )
            embed.set_image(url=url_imagem)
            embed.set_footer(text=f"r/{subreddit}")
            await interaction.followup.send(embed=embed)
        except Exception as e:
            print(f"Erro no /meme: {e}")
            await interaction.followup.send(
                "❌ Não consegui buscar um meme agora. Tente novamente mais tarde.",
                ephemeral=True,
            )

    @app_commands.command(
        name="piada", description="Envia uma piada aleatória em português."
    )
    async def piada(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            resposta = requests.get(PIADA_API, timeout=10)
            resposta.raise_for_status()
            dados = resposta.json()

            embed = discord.Embed(
                title="😄 Piada",
                color=discord.Color.green(),
            )
            if dados.get("type") == "twopart":
                embed.description = f"**{dados['setup']}**\n\n{dados['delivery']}"
            else:
                embed.description = dados.get("joke", "Sem piada.")

            categoria = dados.get("category", "")
            if categoria:
                embed.set_footer(text=f"Categoria: {categoria}")
            await interaction.followup.send(embed=embed)
        except Exception as e:
            print(f"Erro no /piada: {e}")
            await interaction.followup.send(
                "❌ Não consegui buscar uma piada agora. Tente novamente mais tarde.",
                ephemeral=True,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Diversao(bot))
