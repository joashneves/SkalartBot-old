import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Modal, TextInput
from models.Obter_ticket import Manipular_Ticket
import asyncio


class TicketModal(Modal, title="Abrir Ticket"):
    """Modal para o usuário descrever o ticket."""

    titulo = TextInput(
        label="Resuma seu ticket", placeholder="Ex: Problema com pagamento"
    )
    descricao = TextInput(
        label="Descreva o ticket",
        style=discord.TextStyle.long,
        placeholder="Descreva detalhadamente o problema ou dúvida.",
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Obtém a configuração de ticket do servidor
        config = Manipular_Ticket.obter_config(str(interaction.guild_id))
        if not config:
            await interaction.response.send_message(
                "O sistema de tickets não está configurado. Contate um administrador.",
                ephemeral=True,
            )
            return

        # Obtém a categoria e o cargo configurados
        categoria = interaction.guild.get_channel(int(config.categoria_id))
        cargo = interaction.guild.get_role(int(config.cargo_id))

        if not categoria or not cargo:
            await interaction.response.send_message(
                "Categoria ou cargo de tickets não encontrados. Contate um administrador.",
                ephemeral=True,
            )
            return

        # Cria o canal de ticket
        ticket_canal = await interaction.guild.create_text_channel(
            name=f"ticket-{interaction.user.name}", category=categoria
        )

        # Configura as permissões do canal
        await ticket_canal.set_permissions(
            interaction.guild.default_role,  # Permissões para @everyone
            view_channel=False,  # Todos os membros não podem ver o canal
        )
        await ticket_canal.set_permissions(
            interaction.user,  # Permissões para o criador do ticket
            view_channel=True,
            send_messages=True,
            read_message_history=True,
        )
        await ticket_canal.set_permissions(
            cargo,  # Permissões para o cargo configurado
            view_channel=True,
            send_messages=True,
            read_message_history=True,
            manage_channels=True,  # Permissão para gerenciar o canal
        )

        # Envia uma mensagem inicial no canal de ticket
        embed = discord.Embed(
            title=f"Ticket de {interaction.user.name}",
            description=f"**Título:** {self.titulo.value}\n**Descrição:** {self.descricao.value}",
            color=discord.Color.blue(),
        )
        embed.set_footer(text="Use /apagar_ticket para fechar este ticket.")
        await ticket_canal.send(
            content=f"{cargo.mention}, um novo ticket foi criado por {interaction.user.mention}.",
            embed=embed,
        )

        # Responde ao usuário
        await interaction.response.send_message(
            f"Seu ticket foi criado em {ticket_canal.mention}.", ephemeral=True
        )


class Ticket(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="apagar_ticket", description="Fecha o ticket atual.")
    @app_commands.default_permissions(manage_channels=True)
    async def apagar_ticket(self, interaction: discord.Interaction):
        # Obtém a configuração de ticket do servidor
        config = Manipular_Ticket.obter_config(str(interaction.guild_id))
        if not config:
            await interaction.response.send_message(
                "O sistema de tickets não está configurado. Contate um administrador.",
                ephemeral=True,
            )
            return

        # Verifica se o canal atual é um ticket
        categoria = interaction.guild.get_channel(int(config.categoria_id))
        if not categoria or interaction.channel.category_id != categoria.id:
            await interaction.response.send_message(
                "Este comando só pode ser usado em um canal de ticket.", ephemeral=True
            )
            return

        # Verifica se o usuário tem permissão para fechar o ticket
        cargo = interaction.guild.get_role(int(config.cargo_id))
        if (
            interaction.user != interaction.channel.topic  # Criador do ticket
            and cargo not in interaction.user.roles  # Cargo configurado
        ):
            await interaction.response.send_message(
                "Você não tem permissão para fechar este ticket.", ephemeral=True
            )
            return

        # Exclui o canal de ticket
        await interaction.response.send_message(
            "O ticket será fechado em 5 segundos...", ephemeral=True
        )
        await asyncio.sleep(5)  # Aguarda 5 segundos
        await interaction.channel.delete(reason="Ticket fechado.")

    @app_commands.command(name="enviar_ticket", description="Abre um novo ticket.")
    async def enviar_ticket(self, interaction: discord.Interaction):
        # Abre o modal para o usuário descrever o ticket
        await interaction.response.send_modal(TicketModal())

    @app_commands.command(
        name="configurar_ticket",
        description="Configura a categoria e o cargo para gerenciar tickets.",
    )
    @app_commands.describe(
        categoria="A categoria onde os tickets serão criados.",
        cargo="O cargo que terá permissão para gerenciar os tickets.",
    )
    @app_commands.default_permissions(manage_guild=True)
    async def configurar_ticket(
        self,
        interaction: discord.Interaction,
        categoria: discord.CategoryChannel,
        cargo: discord.Role,
    ):
        guild_id = str(interaction.guild_id)
        categoria_id = str(categoria.id)
        cargo_id = str(cargo.id)

        # Configura as permissões da categoria
        try:
            # Define as permissões da categoria para que apenas o cargo configurado tenha acesso
            await categoria.set_permissions(
                interaction.guild.default_role,  # Permissões para @everyone
                view_channel=False,  # Todos os membros não podem ver a categoria
                send_messages=False,  # Todos os membros não podem enviar mensagens
                read_message_history=False,  # Todos os membros não podem ver o histórico
            )
            await categoria.set_permissions(
                cargo,  # Permissões para o cargo configurado
                view_channel=True,  # O cargo pode ver a categoria
                send_messages=True,  # O cargo pode enviar mensagens
                read_message_history=True,  # O cargo pode ver o histórico
                manage_channels=True,  # O cargo pode gerenciar os canais
            )

            # Adiciona ou atualiza a configuração de ticket
            config = Manipular_Ticket.adicionar_config(guild_id, categoria_id, cargo_id)
            if config:
                await interaction.response.send_message(
                    f"Configuração de ticket atualizada com sucesso!\n"
                    f"**Categoria:** {categoria.name}\n"
                    f"**Cargo:** {cargo.name}",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    "Erro ao configurar o ticket. Tente novamente.", ephemeral=True
                )
        except discord.Forbidden:
            await interaction.response.send_message(
                "Eu não tenho permissão para configurar as permissões da categoria.",
                ephemeral=True,
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(
                f"Erro ao configurar as permissões: {e}", ephemeral=True
            )

    @app_commands.command(
        name="remover_config_ticket",
        description="Remove a configuração de ticket do servidor.",
    )
    @app_commands.default_permissions(manage_guild=True)
    async def remover_config_ticket(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild_id)

        # Remove a configuração de ticket
        removido = Manipular_Ticket.remover_config(guild_id)
        if removido:
            await interaction.response.send_message(
                "Configuração de ticket removida com sucesso!", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "Nenhuma configuração de ticket encontrada.", ephemeral=True
            )

    @app_commands.command(
        name="ver_config_ticket",
        description="Mostra a configuração atual de ticket do servidor.",
    )
    @app_commands.default_permissions(manage_guild=True)
    async def ver_config_ticket(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild_id)

        # Obtém a configuração de ticket
        config = Manipular_Ticket.obter_config(guild_id)
        if config:
            categoria = interaction.guild.get_channel(int(config.categoria_id))
            cargo = interaction.guild.get_role(int(config.cargo_id))
            if categoria and cargo:
                await interaction.response.send_message(
                    f"**Configuração de Ticket:**\n"
                    f"**Categoria:** {categoria.name}\n"
                    f"**Cargo:** {cargo.name}",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    "Categoria ou cargo não encontrados. A configuração pode estar desatualizada.",
                    ephemeral=True,
                )
        else:
            await interaction.response.send_message(
                "Nenhuma configuração de ticket encontrada.", ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Ticket(bot))
