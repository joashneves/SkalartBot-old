import random
import discord
from discord.ext import commands


RESPOSTAS_MENCAO = (
    "O que foi?",
    "Oi?",
    "Precisando de alguma coisa?",
    "Fala!",
    "Achei que era sobre o feed de imagens.",
    "Me marca pra quê?",
    "Bah."
)


class ResponderMencao(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Responde quando o bot é mencionado diretamente."""
        if message.author.bot or message.author.id == self.bot.user.id:
            return
        if self.bot.user.mentioned_in(message):
            resposta = random.choice(RESPOSTAS_MENCAO)
            await message.channel.send(resposta)


async def setup(bot: commands.Bot):
    await bot.add_cog(ResponderMencao(bot))
