import discord
from discord.ext import commands, tasks
from discord import app_commands
import feedparser
from models.Obter_Noticia import Manipular_Noticia
from models.Obter_Feed import Manipular_Feed

INTERVALO_CHECK = 15 * 60  # verifica a cada 15 minutos

FEEDS_FIXOS = {
    "Jovem Nerd": "https://jovemnerd.com.br/feed/",
    "TecMundo": "https://www.tecmundo.com.br/feed",
    "IGN Brasil": "https://br.ign.com/feed.xml",
    "Tecnoblog": "https://tecnoblog.net/feed/",
    "Meio Bit": "https://meiobit.com/feed/",
}


class Noticias(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.verificar_noticias.start()

    def cog_unload(self):
        self.verificar_noticias.cancel()

    async def postar_feed(self, config):
        """Busca o feed configurado e posta notícias novas no canal do servidor."""
        try:
            feed = feedparser.parse(config.feed_url)
            if not feed.entries:
                return

            # Ordena da mais antiga para a mais nova para postar em sequência
            entrada = feed.entries[0]
            link = entrada.get("link") or entrada.get("id")
            if not link:
                return

            if config.ultimo_link == link:
                return  # já postada

            canal = self.bot.get_channel(int(config.canal_id))
            if not canal:
                return

            titulo = entrada.get("title", "Notícia")
            descricao = entrada.get("summary", "")
            # Limpa o HTML básico da descrição
            import re

            texto = re.sub(r"<[^>]+>", "", descricao).strip()
            if len(texto) > 300:
                texto = texto[:297] + "..."

            embed = discord.Embed(
                title=titulo,
                description=texto or None,
                url=link,
                color=discord.Color.blue(),
            )
            try:
                embed.set_thumbnail(
                    url=feed.feed.image.href
                )
            except AttributeError:
                pass
            try:
                media = entrada.media_content[0]["url"]
                embed.set_image(url=media)
            except (AttributeError, IndexError, KeyError):
                pass

            await canal.send(embed=embed)
            Manipular_Noticia.atualizar_ultimo_link(config.id, link)
            print(f"Notícia postada de {config.feed_url}: {titulo}")
        except Exception as e:
            print(f"Erro ao postar feed {config.feed_url}: {e}")

    @tasks.loop(seconds=INTERVALO_CHECK)
    async def verificar_noticias(self):
        try:
            configs = Manipular_Noticia.obter_todos_feeds()
            for config in configs:
                await self.postar_feed(config)
        except Exception as e:
            print(f"Erro no loop de notícias: {e}")

    @app_commands.command(
        name="noticias_configurar_feed",
        description="Adiciona um feed RSS geek para o servidor postar notícias no canal de feed.",
    )
    @app_commands.describe(feed_url="A URL do feed RSS (ex: https://jovemnerd.com.br/feed/)")
    @app_commands.default_permissions(manage_guild=True)
    async def configurar_feed(
        self, interaction: discord.Interaction, feed_url: str
    ):
        # Precisa de um canal de feed configurado (/configurar_feed do sistema de feed)
        canais_feed = Manipular_Feed.listar_chats(str(interaction.guild_id))
        if not canais_feed:
            await interaction.response.send_message(
                "❌ Primeiro configure um canal de feed com `/configurar_feed` "
                "(o canal onde as notícias serão postadas).",
                ephemeral=True,
            )
            return

        config = Manipular_Noticia.adicionar_feed(
            str(interaction.guild_id), feed_url, str(canais_feed[0].channel_id)
        )
        await interaction.response.send_message(
            f"✅ Feed **{feed_url}** configurado para o canal <#{config.canal_id}>!\n"
            "As notícias serão postadas automaticamente.",
            ephemeral=True,
        )

    @app_commands.command(
        name="noticias_listar_feeds",
        description="Lista os feeds RSS configurados no servidor.",
    )
    @app_commands.default_permissions(manage_guild=True)
    async def listar_feeds(self, interaction: discord.Interaction):
        configs = Manipular_Noticia.listar_feeds(str(interaction.guild_id))
        if not configs:
            await interaction.response.send_message(
                "❌ Nenhum feed configurado neste servidor.", ephemeral=True
            )
            return
        linhas = [f"- `{config.feed_url}` → <#{config.canal_id}>" for config in configs]
        embed = discord.Embed(
            title="📰 Feeds de notícias",
            description="\n".join(linhas),
            color=discord.Color.blue(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="noticias_remover_feed",
        description="Remove um feed RSS configurado.",
    )
    @app_commands.describe(feed_url="A URL do feed RSS a remover.")
    @app_commands.default_permissions(manage_guild=True)
    async def remover_feed(
        self, interaction: discord.Interaction, feed_url: str
    ):
        removido = Manipular_Noticia.remover_feed(str(interaction.guild_id), feed_url)
        if removido:
            await interaction.response.send_message(
                f"✅ Feed **{feed_url}** removido!", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"❌ Feed **{feed_url}** não estava configurado.", ephemeral=True
            )

    @app_commands.command(
        name="noticias_feeds_fixos",
        description="Mostra feeds geek prontos para adicionar com /noticias_configurar_feed.",
    )
    async def feeds_fixos(self, interaction: discord.Interaction):
        linhas = [f"- **{nome}**: `{url}`" for nome, url in FEEDS_FIXOS.items()]
        embed = discord.Embed(
            title="📚 Feeds geek recomendados",
            description="\n".join(linhas),
            color=discord.Color.blue(),
        )
        embed.set_footer(text="Copie a URL e use /noticias_configurar_feed")
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Noticias(bot))
