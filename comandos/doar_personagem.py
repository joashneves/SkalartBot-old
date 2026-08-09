import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from asyncio import TaskGroup
from models.Obter_personagem import Manipular_Personagem
import os
import aiohttp
import hashlib

IMAGENS_DIR = "imagens_temp"
os.makedirs(IMAGENS_DIR, exist_ok=True)

async def carrega_imagem(url) -> str:
    """
    Salva uma imagem localmente e retorna o caminho do arquivo.
    :param url: URL da imagem.
    :param user_id: ID do usuário que enviou a imagem.
    :return: Caminho do arquivo salvo.
    """
    nome_arquivo = f"{hashlib.md5(url.encode()).hexdigest()}.png"
    caminho_arquivo = os.path.join(IMAGENS_DIR, nome_arquivo)

    # Baixa a imagem e salva localmente
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(caminho_arquivo, "wb") as f:
                    f.write(await response.read())
                return caminho_arquivo
            else:
                raise Exception(f"Erro ao baixar imagem: status {response.status}")

class PersonagensView(discord.ui.View):
    def __init__(self, guild_id, membro_id, personagem, interaction):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        self.membro_id = membro_id
        self.personagem = personagem
        self.index = 0
        self.caminho = None

    async def get_embed(self):
        caminho_arquivo = await self.imagem()
        print(f"VAR : personagens {self.personagem}")

        embed = discord.Embed(
            title=f"Personagem: {self.personagem.nome_personagem}",
            #description=f"Franquia: c \n Genero: {self.personagem.genero_personagem} \n Descrição: {self.personagem.descricao_personagem}",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Franquia",value=f"{self.personagem.franquia_personagem}",inline=False)
        embed.add_field(name="Genero",value=f"{self.personagem.genero_personagem}", inline=False)
        embed.add_field(name="Descrição",value=f"{self.personagem.descricao_personagem}", inline=False)
        embed.set_image(url=f"attachment://image.jpg")
        print(caminho_arquivo)
        embed.set_footer(text=f"Descoberto em : {self.personagem.data_de_descoberta}")
        return embed

    async def imagem(self):
        print(f"VAR: {self.personagem}")
        caminho_arquivo = await carrega_imagem(f"https://personagensaleatorios.squareweb.app/api/Personagems/DownloadPersonagemByPath?Path={self.personagem.caminho_arquivo_personagem}")
        self.caminho = caminho_arquivo
        discord_file = discord.File(caminho_arquivo, 'image.jpg')
        return discord_file

    async def deletar_arquivo(self):
        try:
            if os.path.exists(self.caminho):
                os.remove(self.caminho)
            else:
                return "caminho não encontrado!"
            return f"arquivo deletado do {self.caminho}"
        except:
            return "erro ao apagar arquivo"
            
class DoarPersonagem(commands.Cog):
    def __init__(self, bot: commands.bot):
        super().__init__()
        self.bot = bot
        self.troca = {}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.author.id in self.troca:
            print(f"VAR : {self.troca}")
            id_dono_novo = message.author.id
            if self.troca[message.author.id] != []:
                if (message.content.lower()) in ["sim", "s", "yes", "y"] :
                    await message.channel.send("A troca foi aceita")
                    Manipular_Personagem.alterar_dono_personage(self.troca[id_dono_novo][0],
                        self.troca[id_dono_novo][1],
                        self.troca[id_dono_novo][2],
                        self.troca[id_dono_novo][3],
                        self.troca[id_dono_novo][4],
                        self.troca[id_dono_novo][5])
                    del self.troca[message.author.id]
                    await message.channel.send("Personagem trocado!")
                elif (message.content.lower()) in ["não", "nao", "n", "no", "n"]:
                    await message.channel.send("A troca foi recusada")
                    del self.troca[message.author.id]
                    print(f"VAR : {self.troca}")
                else:
                    print("MSG : Mensagem não é de troca")

    async def temporizador(self, msg, id_novo_dono, interaction,  sleeptime):
        print(f"AVISO : temporizador iniciado com {sleeptime} segundos e self.mensagem {self.troca[id_novo_dono]}")
        await asyncio.sleep(sleeptime)
        if id_novo_dono in self.troca:
            if self.troca[id_novo_dono] == []:
                return
            del self.troca[id_novo_dono] 
            await interaction.response.send_message("acabou o tempo de troca")



    @app_commands.command(name="doar_personagem", description="Troca um personagem com alguem")
    @app_commands.describe(nome="Nome do personagem que voce quer enviar")
    @app_commands.describe(franquia="Nome da franquia que voce quer enviar o personagem")
    @app_commands.describe(user="usuario que voce quer enviar o personagem")
    async def doar_personagem(self, interaction: discord.Interaction,
                                  nome: str,
                                  franquia: str,
                                  user: discord.Member):
        personagem = Manipular_Personagem.Obter_um_personagem(interaction.guild.id, nome, franquia)
        id_dono_antigo = interaction.user.id
        id_dono_novo = user.id
        guild_id = interaction.guild.id
        print(f"VAR : {user.id} == {interaction.user.id}")
        if user.id == interaction.user.id:
            await interaction.response.send_message("Não é possivel enviar um personagem para voce mesmo")
            return
        if not personagem:
            return

        view = PersonagensView(guild_id, id_dono_antigo, personagem, interaction)
        embed = await view.get_embed()
        arquivo = await view.imagem()
        await view.deletar_arquivo()
        await interaction.response.send_message(f"Troca iniciada, responda com sim['s'] ou não['n', 'no', 'não'] <@{id_dono_novo}>",view=view, embed=embed, file=arquivo)    
        msg = interaction.id
        self.troca[id_dono_novo] = ([id_dono_novo, id_dono_antigo, guild_id, personagem.id_personagem, nome, franquia ])
        print(f"VAR : {self.troca[id_dono_novo]}")
        async with TaskGroup() as group:
            group.create_task(self.temporizador(msg, id_dono_novo, interaction, 26))


    @doar_personagem.autocomplete('nome')
    async def doar_personagem_autocomplete(self,interact: discord.Interaction, pesquisa:str):
        opcaoes = []
        personas = Manipular_Personagem.obter_todos_personagens_descoberto_usuario(interact.user.id, interact.guild.id)
        for sonas in personas:
            if pesquisa.lower() in sonas.nome_personagem.lower():
                sonas_option = app_commands.Choice(name=f"{sonas.nome_personagem}", value=f"{sonas.nome_personagem}")
                opcaoes.append(sonas_option)
        return opcaoes[:25]

    @doar_personagem.autocomplete('franquia')
    async def doar_personagem_autocomplete_franquia(self,interact: discord.Interaction, pesquisa:str):
        opcaoes = []
        personas = Manipular_Personagem.obter_todos_personagens_descoberto_usuario(interact.user.id, interact.guild.id)
        franquias = []
        for franquia in personas:
            if not franquia.franquia_personagem in franquias:
                franquias.append(franquia.franquia_personagem)
        for sonas in franquias:
            if pesquisa.lower() in sonas.lower():
                sonas_option = app_commands.Choice(name=f"{sonas}", value=f"{sonas}")
                opcaoes.append(sonas_option)
        return opcaoes[:25]


async def setup(bot):
    await bot.add_cog(DoarPersonagem(bot))
