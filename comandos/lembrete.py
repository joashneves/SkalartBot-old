from datetime import datetime, timedelta
from discord.ext import tasks
import discord
from discord.ext import commands
from discord import app_commands
from models.Obter_Lembrete import Manipular_Lembrete

INTERVALO_CHECK = 15  # segundos


def parsear_duracao(texto: str):
    """Converte '30s', '10m', '2h', '1d', '1h30m' em timedelta."""
    texto = texto.strip().lower()
    if not texto:
        return None
    unidades = {"s": "seconds", "m": "minutes", "h": "hours", "d": "days"}
    total = timedelta()
    numero_atual = ""
    for char in texto:
        if char.isdigit():
            numero_atual += char
        elif char in unidades and numero_atual:
            total += timedelta(**{unidades[char]: int(numero_atual)})
            numero_atual = ""
        else:
            return None
    if numero_atual:
        return None
    return total if total.total_seconds() > 0 else None


class Lembretes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.verificar_lembretes.start()

    def cog_unload(self):
        self.verificar_lembretes.cancel()

    @tasks.loop(seconds=INTERVALO_CHECK)
    async def verificar_lembretes(self):
        try:
            pendentes = Manipular_Lembrete.obter_lembretes_pendentes()
            for lembrete in pendentes:
                try:
                    usuario = self.bot.get_user(int(lembrete.id_discord))
                    if not usuario:
                        usuario = await self.bot.fetch_user(int(lembrete.id_discord))
                    embed = discord.Embed(
                        title="⏰ Lembrete!",
                        description=lembrete.texto,
                        color=discord.Color.orange(),
                    )
                    embed.set_footer(text=f"Você agendou este lembrete em {lembrete.criado_em:%d/%m/%Y %H:%M}")
                    await usuario.send(embed=embed)
                except discord.Forbidden:
                    print(f"Lembrete {lembrete.id}: DM bloqueada pelo usuário.")
                except Exception as e:
                    print(f"Erro ao enviar lembrete {lembrete.id}: {e}")
                finally:
                    Manipular_Lembrete.marcar_enviado(lembrete.id)
        except Exception as e:
            print(f"Erro no loop de lembretes: {e}")

    @app_commands.command(
        name="lembrete",
        description="Cria um lembrete que será enviado no seu privado. Ex: /lembrete 30m Beber água",
    )
    @app_commands.describe(
        duracao="Tempo até o lembrete (ex: 30s, 10m, 2h, 1d, 1h30m)",
        texto="O que deseja lembrar",
    )
    async def lembrete(
        self, interaction: discord.Interaction, duracao: str, texto: str
    ):
        delta = parsear_duracao(duracao)
        if not delta:
            await interaction.response.send_message(
                "❌ Formato inválido. Use por exemplo: `30s`, `10m`, `2h`, `1d`, `1h30m`.",
                ephemeral=True,
            )
            return
        if delta.total_seconds() > 60 * 60 * 24 * 30:
            await interaction.response.send_message(
                "❌ O lembrete não pode passar de 30 dias.", ephemeral=True
            )
            return

        agora = datetime.now()
        data_agendada = agora + delta
        Manipular_Lembrete.criar_lembrete(
            str(interaction.user.id),
            texto,
            data_agendada,
            str(interaction.channel_id),
            str(interaction.guild_id),
        )

        embed = discord.Embed(
            title="✅ Lembrete agendado!",
            description=f"🔔 **{texto}**\n\n⏳ Será enviado no seu privado em **{duracao}** "
            f"(~{data_agendada:%H:%M}).",
            color=discord.Color.green(),
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="lembretes", description="Lista seus lembretes pendentes."
    )
    async def listar_lembretes(self, interaction: discord.Interaction):
        lembretes = Manipular_Lembrete.listar_lembretes(str(interaction.user.id))
        if not lembretes:
            await interaction.response.send_message(
                "❌ Você não tem lembretes pendentes.", ephemeral=True
            )
            return

        linhas = []
        for lembrete in lembretes:
            linhas.append(
                f"`#{lembrete.id}` **{lembrete.texto}**\n"
                f"   ↳ em {lembrete.data_agendada:%d/%m/%Y %H:%M}"
            )
        embed = discord.Embed(
            title="📋 Seus lembretes",
            description="\n".join(linhas),
            color=discord.Color.blue(),
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="cancelar_lembrete",
        description="Cancela um lembrete pendente pelo ID (veja em /lembretes).",
    )
    @app_commands.describe(id_lembrete="O ID do lembrete a cancelar.")
    async def cancelar_lembrete(
        self, interaction: discord.Interaction, id_lembrete: int
    ):
        removido = Manipular_Lembrete.cancelar_lembrete(
            str(interaction.user.id), id_lembrete
        )
        if removido:
            await interaction.response.send_message(
                f"✅ Lembrete #{id_lembrete} cancelado!", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"❌ Lembrete #{id_lembrete} não encontrado ou já enviado.",
                ephemeral=True,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Lembretes(bot))
