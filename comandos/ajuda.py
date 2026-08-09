import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Select, View


class AjudaSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Sobre o Bot",
                description="Informações gerais sobre o bot.",
                emoji="🤖",
            ),
            discord.SelectOption(
                label="Comandos Gerais",
                description="Comandos disponíveis para todos.",
                emoji="📜",
            ),
            discord.SelectOption(
                label="Comandos de Perfil",
                description="Comandos relacionados a perfis.",
                emoji="👤",
            ),
            discord.SelectOption(
                label="Comandos de Imagens",
                description="Comandos relacionados a imagens.",
                emoji="🖼️",
            ),
            discord.SelectOption(
                label="Comandos de Moderação",
                description="Comandos para administradores.",
                emoji="🛠️",
            ),
            discord.SelectOption(  # Nova opção para comandos de ticket
                label="Comandos de Ticket",
                description="Comandos relacionados ao sistema de tickets.",
                emoji="🎫",
            ),
            discord.SelectOption(
                label="Cargos",
                description="Sobre o sistema de cargos automáticos.",
                emoji="🎖️",
            ),
            discord.SelectOption(
                label="Feed", description="Sobre o sistema de feed.", emoji="📢"
            ),
            discord.SelectOption(
                label="Links", description="Convite e repositório do bot.", emoji="🔗"
            ),
            discord.SelectOption(
                label="Jogo de Personagens",
                description="Capture e adivinhe personagens com $jogar.",
                emoji="🎮",
            ),
            discord.SelectOption(
                label="Economia",
                description="Daily, moedas e rankings.",
                emoji="💰",
            ),
            discord.SelectOption(
                label="Diversão",
                description="Memes, piadas e clima.",
                emoji="😂",
            ),
            discord.SelectOption(
                label="Utilidades",
                description="Lembretes, sugestões, atividade e slowmode.",
                emoji="🧰",
            ),
            discord.SelectOption(
                label="Notícias e Streams",
                description="Feeds geek e avisos de live/vídeo.",
                emoji="📡",
            ),
        ]
        super().__init__(placeholder="Escolha uma opção...", options=options)

    async def callback(self, interaction: discord.Interaction):
        # Responde à interação com a seção escolhida
        escolha = self.values[0]
        embed = discord.Embed(title="Ajuda da Skalart", color=discord.Color.blue())

        if escolha == "Sobre o Bot":
            embed.description = (
                "🤖 **Sobre o Bot:**\n"
                "A @($)Skalart é um bot diverso que está em constante evolução e tem o principal objetivo de diversificar o DISCORD como um todo.\n"
                "Ela é feita em Python e está com seu repositório aberto e disponível, junto com suas futuras atualizações [aqui](https://github.com/joashneves/SkalartBot/issues).\n\n"
                "A Skalart oferece uma variedade de funcionalidades, incluindo:\n"
                "- **Sistema de Perfis:** Crie um perfil personalizado e compartilhe suas imagens.\n"
                "- **Feed de Imagens:** Compartilhe e visualize imagens em um feed configurável.\n"
                "- **Cargos Automáticos:** Atribua cargos automaticamente aos membros do servidor.\n"
                "- **Moderação:** Ferramentas para administradores gerenciarem o servidor.\n"
                "- **Interações:** Reações automáticas em mensagens e muito mais.\n\n"
                "A Skalart é projetada para ser fácil de usar e altamente personalizável, trazendo diversão e utilidade para o seu servidor!"
            )
        elif escolha == "Comandos Gerais":
            embed.description = (
                "📜 **Comandos Gerais:**\n"
                "- `/ping`: Verifica a latência do bot.\n"
                "- `/ajuda`: Mostra esta mensagem de ajuda.\n"
                "- `/avatar`: Salva o avatar atual de um usuário e cria um histórico de fotos de perfil.\n"
            )
        elif escolha == "Comandos de Perfil":
            embed.description = (
                "👤 **Comandos de Perfil:**\n"
                "- `/registrar`: Cria um perfil para usar os comandos do bot.\n"
                "- `/perfil`: Mostra o perfil de um usuário (o seu ou de alguém mencionado).\n"
                "- `/usuarios_registrados`: Lista todos os usuários registrados no bot.\n"
            )
        elif escolha == "Comandos de Imagens":
            embed.description = (
                "🖼️ **Comandos de Imagens:**\n"
                "- `/imagem_aleatoria`: Resgata uma imagem aleatória enviada por usuários.\n"
                "- `/adicionar_imagem`: Adiciona uma imagem ao bot (requer registro).\n"
                "- `/minhas_imagens`: Mostra as imagens que você enviou, com seus IDs.\n"
                "- `/remover_imagem`: Remove uma imagem que você enviou (usando o ID).\n"
            )
        elif escolha == "Comandos de Moderação":
            embed.description = (
                "🛠️ **Comandos de Moderação:**\n"
                "- `/configurar_chat`: Configura um canal para reagir com emojis em mensagens.\n"
                "- `/listar_chats`: Lista todos os canais configurados para reações.\n"
                "- `/remover_chat`: Remove um canal da lista de reações.\n"
                "- `/configurar_cargo`: Configura cargos para serem atribuídos automaticamente.\n"
                "- `/listar_cargos`: Lista todos os cargos configurados.\n"
                "- `/remover_cargo`: Remove um cargo da lista de cargos automáticos.\n"
            )
        elif escolha == "Cargos":
            embed.description = (
                "🎖️ **Cargos:**\n"
                "O sistema de cargos da Skalart permite que administradores configurem cargos para serem atribuídos automaticamente aos membros do servidor.\n\n"
                "**Como funciona:**\n"
                "- Os administradores podem configurar uma lista de cargos usando `/configurar_cargo`.\n"
                "- Quando um novo membro entra no servidor, o bot atribui aleatoriamente um dos cargos configurados.\n"
                "- Isso é útil para criar sistemas de roles aleatórios ou categorizar membros de forma dinâmica.\n"
            )
        elif escolha == "Feed":
            embed.description = (
                "📢 **Feed:**\n"
                "O sistema de feed da Skalart permite que os usuários compartilhem imagens e visualizem as imagens enviadas por outros em um canal dedicado.\n\n"
                "**Como funciona:**\n"
                "- Os usuários podem enviar imagens com `/adicionar_imagem` (requer registro).\n"
                "- As imagens enviadas podem aparecer no feed do servidor, se configurado.\n"
                "- Administradores podem configurar um canal para receber feeds usando `/configurar_feed`.\n"
                "- O feed é uma ótima maneira de compartilhar conteúdo visual e interagir com a comunidade.\n"
            )
        elif escolha == "Links":
            embed.description = (
                "🔗 **Links:**\n"
                "- [Convite para o servidor da Skalart](https://discord.gg/h7mP7aZuY4)\n"
                "- [Repositório do código no GitHub](https://github.com/joashneves/SkalartBot)\n"
                "- [Clique aqui para colocar no seu servidor](https://discord.com/oauth2/authorize?client_id=1025176642236203118&scope=bot&permissions=8)\n"
            )
        elif escolha == "Comandos de Ticket":  # Nova seção para comandos de ticket
            embed.description = (
                "🎫 **Comandos de Ticket:**\n"
                "O sistema de tickets da Skalart permite que os usuários abram tickets para suporte ou questões específicas.\n\n"
                "**Comandos disponíveis:**\n"
                "- `/enviar_ticket`: Abre um novo ticket para suporte.\n"
                "- `/apagar_ticket`: Fecha o ticket atual (apenas para criadores do ticket ou administradores).\n"
                "- `/configurar_ticket`: Configura a categoria e o cargo para gerenciar tickets (apenas para administradores).\n"
                "- `/remover_config_ticket`: Remove a configuração de ticket do servidor (apenas para administradores).\n"
                "- `/ver_config_ticket`: Mostra a configuração atual de ticket do servidor (apenas para administradores).\n\n"
                "**Como funciona:**\n"
                "- Os usuários podem abrir tickets usando `/enviar_ticket`.\n"
                "- Os tickets são criados em uma categoria específica, configurada pelos administradores.\n"
                "- Apenas o criador do ticket e os administradores podem visualizar e interagir com o ticket.\n"
                "- Os tickets podem ser fechados com `/apagar_ticket`.\n"
            )
        elif escolha == "Jogo de Personagens":
            embed.description = (
                "🎮 **Jogo de Personagens:**\n"
                "Participe do jogo de adivinhação e captura de personagens com o comando `$jogar`!\n\n"
                "**Como funciona:**\n"
                "- Ao usar `$jogar`, o bot sorteia um personagem misterioso.\n"
                "- Tente adivinhar quem é digitando o nome do personagem no chat.\n"
                "- Se acertar, o personagem será **capturado e adicionado à sua coleção**.\n\n"
                "**O que você pode fazer com seus personagens:**\n"
                "- Ver sua coleção e editar as descrições com `/listar_personagens`.\n"
                "- Doar personagens para outros jogadores com `/doar_personagem`.\n\n"
                 "**Dica:** Quanto mais você jogar, maior será sua coleção!\n"
            )
        elif escolha == "Economia":
            embed.description = (
                "💰 **Economia:**\n"
                "- `/daily`: Resgata sua recompensa diária de moedas (quanto mais dias seguidos, mais moedas).\n"
                "- `/rank`: Mostra o ranking do servidor por moedas ou XP.\n"
                "- `/xp`: Mostra seu nível, XP e progresso.\n\n"
                "**Como ganhar moedas/XP:**\n"
                "- Resgatar o daily todos os dias.\n"
                "- Acertar personagens no `$jogar`.\n"
                "- Falar no servidor para ganhar XP e subir de nível."
            )
        elif escolha == "Diversão":
            embed.description = (
                "😂 **Diversão:**\n"
                "- `/meme`: Envia um meme aleatório do Reddit.\n"
                "- `/piada`: Envia uma piada aleatória em português.\n"
                "- `/clima`: Mostra o clima de uma cidade (requer `OPENWEATHER_API_KEY` no .env)."
            )
        elif escolha == "Utilidades":
            embed.description = (
                "🧰 **Utilidades:**\n"
                "- `/lembrete 30m Beber água`: Agenda um lembrete que chega no seu **privado**.\n"
                "- `/lembretes`: Lista seus lembretes pendentes.\n"
                "- `/cancelar_lembrete <id>`: Cancela um lembrete.\n"
                "- `/sugestao <texto>`: Envia uma sugestão para o canal de sugestões.\n"
                "- `/configurar_sugestao <canal>`: Define o canal de sugestões (admin).\n"
                "- `/atividade`: Suas estatísticas de mensagens.\n"
                "- `/top_atividade` e `/top_atividade_total`: Membros mais ativos.\n"
                "- `/configurar_slowmode <canal> <nivel>`: Exige nível mínimo para falar num canal (admin).\n"
                "- `/listar_slowmodes`: Lista canais com restrição de nível (admin)."
            )
        elif escolha == "Notícias e Streams":
            embed.description = (
                "📡 **Notícias e Streams:**\n\n"
                "**Notícias geek (RSS):**\n"
                "- `/noticias_feeds_fixos`: Vê feeds prontos (Jovem Nerd, TecMundo, IGN, etc.).\n"
                "- `/noticias_configurar_feed <url>`: Adiciona um feed RSS (admin).\n"
                "- `/noticias_listar_feeds` e `/noticias_remover_feed`: Gerencia os feeds (admin).\n"
                "- As notícias são postadas no canal de feed configurado com `/configurar_feed`.\n\n"
                "**Twitch/YouTube:**\n"
                "- `/streams_configurar`: Configura um canal Twitch ou YouTube para avisar de lives e vídeos novos.\n"
                "- `/streams_listar` e `/streams_remover`: Gerenciam os canais monitorados (admin).\n"
                "- Requer `TWITCH_CLIENT_ID`, `TWITCH_SECRET` e `YOUTUBE_API_KEY` no .env."
            )


        await interaction.response.edit_message(embed=embed)


class Ajuda(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ajuda", description="Mostra informações sobre o bot e seus comandos."
    )
    async def ajuda(self, interaction: discord.Interaction):
        # Cria o embed inicial
        embed = discord.Embed(
            title="Ajuda da Skalart",
            description="Escolha uma opção no menu abaixo para ver mais informações sobre o bot.",
            color=discord.Color.blue(),
        )

        # Cria a view com o menu de seleção
        view = View()
        view.add_item(AjudaSelect())

        # Envia a mensagem com o embed e o menu
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Ajuda(bot))
