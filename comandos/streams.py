import asyncio
import os
import time
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
YOUTUBE_CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels"


def _mencionar_cargos(canal: discord.TextChannel, config) -> str:
    """Monta a menção dos cargos configurados que ainda existem no servidor."""
    cargos_ids = Manipular_Stream._cargos_para_lista(config.cargos)
    mencoes = []
    for cargo_id in cargos_ids:
        try:
            cargo = canal.guild.get_role(int(cargo_id))
        except (ValueError, TypeError):
            cargo = None
        if cargo:
            mencoes.append(cargo.mention)
    return " ".join(mencoes)


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


_youtube_channel_id_cache: dict[str, str] = {}
_youtube_quota_cooldown_until: float = 0


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

            if streams and config.ultimo_item != streams[0]["id"]:
                stream = streams[0]
                embed = discord.Embed(
                    title=f"🔴 {stream['title']}",
                    description=f"**{config.canal_identificador} está ao vivo!**\n"
                    f"Jogando: {stream['game_name']}\n"
                    f"Viewers: {stream['viewer_count']}",
                    url=f"https://www.twitch.tv/{config.canal_identificador}",
                    color=discord.Color.purple(),
                )
                embed.set_thumbnail(url=dados[0]["profile_image_url"])
                embed.set_image(
                    url=stream["thumbnail_url"]
                    .replace("{width}", "1920")
                    .replace("{height}", "1080")
                )
                embed.set_footer(text="Twitch")
                mencao = _mencionar_cargos(canal, config)
                await canal.send(content=mencao, embed=embed)
                Manipular_Stream.atualizar_ultimo_item(config.id, stream["id"])
                print(f"Live detectada: {config.canal_identificador}")
        except Exception as e:
            print(f"Erro ao verificar Twitch {config.canal_identificador}: {e}")

    async def verificar_youtube(self, config):
        global _youtube_quota_cooldown_until
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            return

        now = time.time()
        if now < _youtube_quota_cooldown_until:
            return

        try:
            canal_identificador = config.canal_identificador
            channel_id = canal_identificador

            if not canal_identificador.startswith("UC"):
                if canal_identificador in _youtube_channel_id_cache:
                    channel_id = _youtube_channel_id_cache[canal_identificador]
                else:
                    handle = canal_identificador
                    if not handle.startswith("@"):
                        handle = f"@{handle}"
                    resposta = requests.get(
                        YOUTUBE_CHANNELS_URL,
                        params={
                            "part": "id",
                            "forHandle": handle,
                            "key": api_key,
                        },
                        timeout=10,
                    )
                    if resposta.status_code == 429:
                        _youtube_quota_cooldown_until = time.time() + 3600
                        print("YouTube quota excedida (channels). Cooldown de 1h.")
                        return
                    resposta.raise_for_status()
                    canais = resposta.json().get("items", [])
                    if not canais:
                        return
                    channel_id = canais[0]["id"]
                    _youtube_channel_id_cache[canal_identificador] = channel_id

            max_tentativas = 3
            resposta = None
            for tentativa in range(max_tentativas):
                resposta = requests.get(
                    YOUTUBE_SEARCH_URL,
                    params={
                        "part": "snippet",
                        "channelId": channel_id,
                        "order": "date",
                        "type": "video",
                        "maxResults": 1,
                        "key": api_key,
                    },
                    timeout=10,
                )
                if resposta.status_code == 429:
                    if tentativa < max_tentativas - 1:
                        await asyncio.sleep(30 * (tentativa + 1))
                        continue
                    else:
                        _youtube_quota_cooldown_until = time.time() + 3600
                        print("YouTube quota excedida (search). Cooldown de 1h.")
                        return
                break
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
            mencao = _mencionar_cargos(canal, config)
            await canal.send(content=mencao, embed=embed)
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
        canal_identificador="Nome do canal Twitch ou ID/handle do canal YouTube",
        canal_postagem="Canal do Discord onde o aviso será enviado",
        cargo="(Opcional) Cargo que será mencionado quando houver live/vídeo",
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
        cargo: discord.Role = None,
    ):
        cargos = [str(cargo.id)] if cargo else None
        Manipular_Stream.adicionar_stream(
            str(interaction.guild_id),
            tipo.value,
            canal_identificador,
            str(canal_postagem.id),
            cargos=cargos,
        )
        msg = (
            f"✅ **{tipo.value.capitalize()}** `{canal_identificador}` configurado!\n"
            f"Avisos serão enviados em {canal_postagem.mention}."
        )
        if cargo:
            msg += f"\nCargo que será mencionado: {cargo.mention}"
        await interaction.response.send_message(msg, ephemeral=True)

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
        linhas = []
        for config in configs:
            cargos = Manipular_Stream._cargos_para_lista(config.cargos)
            if cargos:
                nomes = []
                for cargo_id in cargos:
                    cargo = interaction.guild.get_role(int(cargo_id))
                    nomes.append(f"@{cargo.name}" if cargo else f"`{cargo_id}`")
                cargos_txt = "Cargos: " + ", ".join(nomes)
            else:
                cargos_txt = "Cargos: nenhum"
            linhas.append(
                f"- **{config.tipo.capitalize()}**: `{config.canal_identificador}` → <#{config.canal_postagem}>\n  {cargos_txt}"
            )
        embed = discord.Embed(
            title="📺 Canais monitorados",
            description="\n".join(linhas),
            color=discord.Color.purple(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="streams_cargo_adicionar",
        description="Adiciona um cargo que será mencionado quando o canal iniciar live/vídeo.",
    )
    @app_commands.describe(
        tipo="O tipo de canal",
        canal_identificador="Nome do canal Twitch ou ID do canal YouTube",
        cargo="Cargo que será mencionado",
    )
    @app_commands.choices(
        tipo=[
            app_commands.Choice(name="Twitch", value="twitch"),
            app_commands.Choice(name="YouTube", value="youtube"),
        ]
    )
    @app_commands.default_permissions(manage_guild=True)
    async def cargo_adicionar(
        self,
        interaction: discord.Interaction,
        tipo: app_commands.Choice[str],
        canal_identificador: str,
        cargo: discord.Role,
    ):
        config = Manipular_Stream.adicionar_cargo(
            str(interaction.guild_id), tipo.value, canal_identificador, str(cargo.id)
        )
        if config is None:
            await interaction.response.send_message(
                f"❌ **{tipo.value.capitalize()}** `{canal_identificador}` não está configurado. Use `/streams_configurar` primeiro.",
                ephemeral=True,
            )
            return
        await interaction.response.send_message(
            f"✅ Cargo {cargo.mention} será mencionado quando **{canal_identificador}** iniciar live/vídeo!",
            ephemeral=True,
        )

    @app_commands.command(
        name="streams_cargo_remover",
        description="Remove um cargo da lista de menções de um canal.",
    )
    @app_commands.describe(
        tipo="O tipo de canal",
        canal_identificador="Nome do canal Twitch ou ID do canal YouTube",
        cargo="Cargo que não deve mais ser mencionado",
    )
    @app_commands.choices(
        tipo=[
            app_commands.Choice(name="Twitch", value="twitch"),
            app_commands.Choice(name="YouTube", value="youtube"),
        ]
    )
    @app_commands.default_permissions(manage_guild=True)
    async def cargo_remover(
        self,
        interaction: discord.Interaction,
        tipo: app_commands.Choice[str],
        canal_identificador: str,
        cargo: discord.Role,
    ):
        config = Manipular_Stream.remover_cargo(
            str(interaction.guild_id), tipo.value, canal_identificador, str(cargo.id)
        )
        if config is None:
            await interaction.response.send_message(
                f"❌ **{tipo.value.capitalize()}** `{canal_identificador}` não está configurado.",
                ephemeral=True,
            )
            return
        await interaction.response.send_message(
            f"✅ Cargo {cargo.mention} não será mais mencionado para **{canal_identificador}**.",
            ephemeral=True,
        )

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
