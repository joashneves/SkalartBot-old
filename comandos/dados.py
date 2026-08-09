import random
from discord.ext import commands

r = random
class Dados(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.command()
    async def r(self, ctx:commands.Context ):
        # Dividir a mensagem nos espaços para obter os parâmetros
        parametros = ctx.message.content.split()
        
        # Se não houver parâmetros suficientes, sair
        if len(parametros) < 2:
            await ctx.reply("Por favor, forneça parâmetros válidos. Exemplo: r 2d20")
            return

        # Obter a quantidade e a quantidade de lados do dado
        quantidade, lados = map(int, parametros[1].split('d'))

        # Simular os lançamentos dos dados
        resultados = [r.randint(1, lados) for _ in range(quantidade)]

        await ctx.reply(f"Resultados do dado de {quantidade}d{lados}: {resultados}")
        

async def setup(bot):
    await bot.add_cog(Dados(bot))