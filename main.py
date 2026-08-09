"""
Módulo principal para inicializar o bot Discord.
"""
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from models import Obter_cargo

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")  # pylint: disable=no-member
ID_USER_MASTER = os.getenv("ID_USER_MASTER")

# Permissões e afins
permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True


# Criação do bot de forma síncrona
bot = commands.Bot(command_prefix="$", intents=permissoes)


async def carregar_comandos():
    for arquivo in os.listdir("comandos"):
        if arquivo.endswith(".py"):
            await bot.load_extension(f"comandos.{arquivo[:-3]}")


@bot.event
async def on_ready():
    print("Inciand...")
    """Atribui cargos automaticamente a todos os membros ao iniciar o bot."""
    for guild in bot.guilds:
        print(f"Processando guild: {guild.name} (ID: {guild.id})")
        for member in guild.members:
            if not member.bot:  # Ignorar bots
                print(f"Atribuindo cargos para {member.name}")
                await Obter_cargo.Manipular_Cargo.atribuir_cargo(member)
    await carregar_comandos()
    print(f"Bot {bot.user.name} está online!")

    await bot.change_presence(
        activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="Por todo tempo e espaço"))

    return "Bot Online"

@bot.command()
async def sincronizar(ctx: commands.Context):
    if ctx.author.id == int(ID_USER_MASTER):
       try:
            synced = await bot.tree.sync()  # Sincroniza os comandos de barra
            print(f"Comandos de barra sincronizados: {len(synced)} comandos")
       except Exception as e:
            print(f"Erro ao sincronizar comandos de barra: {e}")
       await ctx.reply(f"{len(synced)} comandos sicronizados")
       return
    else:
        await ctx.reply("Voce não tem permissão para esse comando")
        return


# Função main para ser chamada no script
def main():
    """
    Executa o bot utilizando o token armazenado no ambiente.
    """
    bot.run(TOKEN)


# Este bloco só é executado quando o script for rodado diretamente
if __name__ == "__main__":
    main()
