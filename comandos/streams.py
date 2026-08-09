import asyncio
import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
import requests
from models.Obter_Stream import Manipular_Stream

INTERVALO_CHECK = 5 * 60  # verifica a cada 5 minutos

TWITCH_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
TWITCH_STREAMS_URL = "https://api.twitch.tv/helix/streams"
TWITCH_USERS_URL = "https://api.twitch.tv/helix/users"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


def obter_token_twitch():
    client_id = os.getenv("TWITCH_CLIENT_ID")
    secret = os.getenv("TWITCH_SECRET")
    if not client_id or not secret:
        return None
    try:
        resposta = requests.post(
            TWITCH_TOKEN_URL,
            data={
                "client_id": client_id,
                "client_secret": secret,
                "grant_type": "client_credentials",
            },
            timeout=10,
        )
        resposta.raise_for_status()
        return resposta.json().get("access_token")
    except Exception as e:
        print(f"Erro ao obter token da Twitch: {e}")
        return None


class Streams(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.verificar_streams.start()

    def cog_unload(self):
        self.verificar_streams.cancel()

    async def verificar_twitch(self, config):
        token = obter_token_twitch()
        if not token:
            return
        headers = {
            "Client-ID": os.getenv("TWITCH_CLIENT_ID"),
            "Authorization": f"Bearer {token}",
        }
        try:
            # Converte o identificador (nome do canal) em user_id
            resposta = requests.get(
                TWITCH_USERS_URL,
                headers=headers,
                params={"login": config.canal_identificador},
                timeout=10,
            )
            resposta.raise_for_status()
            dados = resposta.json().get("data", [])
            if not dados:
                return
            user_id = dados[0]["id"]

            resposta = requests.get(
                TWITCH_STREAMS_URL,
                headers=headers,
                params={"user_id": user_id},
                timeout=10,
            )
            resposta.raise_for_status()
            streams = resposta.json().get("data", [])

            canal = self.bot.get_channel(int(config.canal_postagem))
            if not canal:
                return

            if streams and config.ultimo_item != user_id:
                stream = streams[0]
                embed = discord.Embed(
                    title=f"🔴 {stream['title']}",
                    description=f"**{config.canal_identificador} está ao vivo!**\n"
                    f"Jogando: {stream['game_name']}\n"
                    f"Viewers: {stream['viewer_count']}",
                    color=discord.Color.purple(),
                )
                embed.set_thumbnail(url=dados[0]["profile_image_url"])
                embed.set_image(url=stream["thumbnail_url"].replace("{width}", "1920").replace("{height}", "1080"))
                embed.set_footer(text="Twitch")
                await canal.send(embed=embed)
                Manipular_Stream.atualizar_ultimo_item(config.id, user_id)
                print(f"Live detectada: {config.canal_identificador}")
        except Exception as e:
            print(f"Erro ao verificar Twitch {config.canal_identificador}: {e}")

    async def verificar_youtube(self, config):
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            return
        try:
            resposta = requests.get(
                YOUTUBE_SEARCH_URL,
                params={
                    "part": "snippet",
                    "channelId": config.canal_identificador,
                    "order": "date",
                    "type": "video",
                    "maxResults": 1,
                    "key": api_key,
                },
                timeout=10,
            )
            resposta.raise_for_status()
            dados = resposta.json().get("items", [])
            if not dados:
                return

            item = dados[0]
            video_id = item["id"]["videoId"]
            if config.ultimo_item == video_id:
                return

            canal = self.bot.get_channel(int(config.canal_postagem))
            if not canal:
                return

            snippet = item["snippet"]
            embed = discord.Embed(
                title=f"🎬 {snippet['title']}",
                description=f"**Novo vídeo do canal {snippet['channelTitle']}!**",
                url=f"https://www.youtube.com/watch?v={video_id}",
                color=discord.Color.red(),
            )
            embed.set_thumbnail(url=snippet["channel"]["thumbnails"]["high"]["url"])
            try:
                embed.set_image(url=snippet["thumbnails"]["high"]["url"])
            except (KeyError, TypeError):
                pass
            embed.set_footer(text="YouTube")
            await canal.send(embed=embed)
            Manipular_Stream.atualizar_ultimo_item(config.id, video_id)
            print(f"Vídeo novo detectado: {snippet['title']}")
        except Exception as e:
            print(f"Erro ao verificar YouTube {config.canal_identificador}: {e}")

    @tasks.loop(seconds=INTERVALO_CHECK)
    async def verificar_streams(self):
        try:
            configs = Manipular_Stream.obter_todas_streams()
            for config in configs:
                if config.tipo == "twitch":
                    await self.verificar_twitch(config)
                elif config.tipo == "youtube":
                    await self.verificar_youtube(config)
                await asyncio.sleep(2)  # evita flood de requisições
        except Exception as e:
            print(f"Erro no loop de streams: {e}")

    @app_commands.command(
        name="streams_configurar",
        description="Configura um canal Twitch ou YouTube para avisar de lives/vídeos novos.",
    )
    @app_commands.describe(
        tipo="O tipo de canal",
        canal_identificador="Nome do canal Twitch ou ID do canal YouTube",
        canal_postagem="Canal do Discord onde o aviso será enviado",
    )
    @app_commands.choices(
        tipo=[
            app_commands.Choice(name="Twitch", value="twitch"),
            app_commands.Choice(name="YouTube", value="youtube"),
        ]
    )
    @app_commands.default_permissions(manage_guild=True)
    async def configurar_stream(
        self,
        interaction: discord.Interaction,
        tipo: app_commands.Choice[str],
        canal_identificador: str,
        canal_postagem: discord.TextChannel,
    ):
        Manipular_Stream.adicionar_stream(
            str(interaction.guild_id),
            tipo.value,
            canal_identificador,
            str(canal_postagem.id),
        )
        await interaction.response.send_message(
            f"✅ **{tipo.value.capitalize()}** `{canal_identificador}` configurado!\n"
            f"Avisos serão enviados em {canal_postagem.mention}.",
            ephemeral=True,
        )

    @app_commands.command(
        name="streams_listar",
        description="Lista os canais Twitch/YouTube configurados no servidor.",
    )
    @app_commands.default_permissions(manage_guild=True)
    async def listar_streams(self, interaction: discord.Interaction):
        configs = Manipular_Stream.listar_streams(str(interaction.guild_id))
        if not configs:
            await interaction.response.send_message(
                "❌ Nenhum canal Twitch/YouTube configurado.", ephemeral=True
            )
            return
        linhas = [
            f"- **{config.tipo.capitalize()}**: `{config.canal_identificador}` → <#{config.canal_postagem}>"
            for config in configs
        ]
        embed = discord.Embed(
            title="📺 Canais monitorados",
            description="\n".join(linhas),
            color=discord.Color.purple(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="streams_remover",
        description="Remove um canal Twitch/YouTube do monitoramento.",
    )
    @app_commands.describe(
        tipo="O tipo do canal",
        canal_identificador="Nome do canal Twitch ou ID do canal YouTube",
    )
    @app_commands.choices(
        tipo=[
            app_commands.Choice(name="Twitch", value="twitch"),
            app_commands.Choice(name="YouTube", value="youtube"),
        ]
    )
    @app_commands.default_permissions(manage_guild=True)
    async def remover_stream(
        self,
        interaction: discord.Interaction,
        tipo: app_commands.Choice[str],
        canal_identificador: str,
    ):
        removido = Manipular_Stream.remover_stream(
            str(interaction.guild_id), tipo.value, canal_identificador
        )
        if removido:
            await interaction.response.send_message(
                f"✅ **{tipo.value.capitalize()}** `{canal_identificador}` removido!",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                f"❌ **{tipo.value.capitalize()}** `{canal_identificador}` não estava configurado.",
                ephemeral=True,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Streams(bot))
