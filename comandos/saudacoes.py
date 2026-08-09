from discord.ext import commands
from datetime import datetime
import random
import pytz
from models import Obter_Usuario
from models.Obter_dia import Manipular_dia
from models.Obter_saudacao import Manipular_saudacao


class MonitorarSaudacoes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fuso_brasilia = pytz.timezone("America/Sao_Paulo")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignora mensagens de bots

        conteudo = message.content.lower()
        saudacao = Manipular_saudacao.detectar_saudacao(conteudo)
        if not saudacao:
            return

        id_discord = str(message.author.id)
        agora = datetime.now(self.fuso_brasilia)
        nome = message.author.display_name

        resposta = Manipular_saudacao.obter_resposta(saudacao, agora, nome)
        await message.channel.send(resposta)

        # Só registra e recompensa se a saudação for do período certo do dia
        if not Manipular_saudacao.eh_periodo_valido(saudacao, agora.hour):
            return

        tipo = Manipular_saudacao.TIPO_BANCO[saudacao]
        registro = Manipular_dia.obter_saudacao(id_discord, tipo)
        if registro and registro["data"].date() == agora.date():
            return  # Já saudou hoje

        Manipular_dia.registrar_saudacao(id_discord, tipo)

        usuario_registrado = Obter_Usuario.Manipular_Usuario.obter_usuario(id_discord)
        if not usuario_registrado:
            return

        moedas_ganhas = random.randint(1, 5)
        xp_ganho = random.randint(10, 50)
        Obter_Usuario.Manipular_Usuario.adicionar_moedas(id_discord, moedas_ganhas)
        Obter_Usuario.Manipular_Usuario.adicionar_xp(id_discord, xp_ganho)


async def setup(bot: commands.Bot):
    await bot.add_cog(MonitorarSaudacoes(bot))
