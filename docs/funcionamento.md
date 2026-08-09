# Funcionamento do bot

Este documento explica como o bot é inicializado, como ele atribui cargos, como o banco de dados é criado e como o projeto está estruturado.

## Inicialização

Tudo começa no `main.py`. Ele carrega as variáveis de ambiente, cria o objeto `Bot`, registra os eventos e carrega todos os comandos (cogs) presentes na pasta `comandos/`.

```python
@bot.event
async def on_ready():
    print("Inciand...")
    """Atribui cargos automaticamente a todos os membros ao iniciar o bot."""
    for guild in bot.guilds:
        print(f"Processando guild: {guild.name} (ID: {guild.id})")
        for member in guild.members:
            if not member.bot:  # Ignorar bots
                print(f"Atribuindo cargos para {member.name}")
                await atribuir_cargos(member)
    await carregar_comandos()
    print(f"Bot {bot.user.name} está online!")

    await bot.change_presence(
        activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="Por todo tempo e espaço"))

    return "Bot Online"
```

O `on_ready` executa três tarefas assim que o bot conecta ao Discord:

1. Percorre todos os servidores e atribui os cargos automáticos a quem ainda não os tem.
2. Carrega os cogs (comandos) da pasta `comandos/`.
3. Define a presença do bot.

```python
async def carregar_comandos():
    for arquivo in os.listdir("comandos"):
        if arquivo.endswith(".py"):
            await bot.load_extension(f"comandos.{arquivo[:-3]}")
```

## Atribuição de cargos

Quando alguém entra no servidor, o evento `on_member_join` do cog `comandos/cargos.py` chama `Manipular_Cargo.atribuir_cargo`, que sorteia um dos cargos configurados (via `/configurar_cargo`) e aplica ao novo membro, caso ele ainda não tenha nenhum.

```python
# models/Obter_cargo.py
@staticmethod
async def atribuir_cargo(member: discord.Member):
    """Atribui um único cargo automaticamente a novos membros, caso o membro não tenha nenhum dos cargos."""
    id_guild = str(member.guild.id)
    cargos_ids = Manipular_Cargo.obter_Cargo(id_guild)
    print(f"Verificando cargos para o guild_id: {id_guild}")
    # Verifica se o membro já possui algum dos cargos
    cargos_do_membro = [
        cargo for cargo in member.roles if cargo.id in map(int, cargos_ids)
    ]
    if cargos_do_membro:
        print(f"{member.name} já tem um dos cargos, ignorando atribuição.")
        return  # Ignora se o membro já tem um dos cargos
    # Escolher um cargo aleatório da lista de cargos
    if cargos_ids:
        cargo_id = random.choice(cargos_ids)  # Escolher um cargo aleatoriamente
        cargo = discord.utils.get(member.guild.roles, id=int(cargo_id))
        if cargo and cargo not in member.roles:
            await member.add_roles(cargo)
            print(f"Cargo {cargo.name} atribuído a {member.name}.")

# comandos/cargos.py
@commands.Cog.listener()
async def on_member_join(self, member: discord.Member):
    """Atribui um cargo automaticamente quando um membro entra no servidor."""
    await Obter_cargo.Manipular_Cargo.atribuir_cargo(member)
```

No `on_ready` do `main.py`, o mesmo `atribuir_cargo` é aplicado a todos os membros de todos os servidores no momento em que o bot inicia.

## Menção ao bot

Quando o bot é mencionado em uma mensagem, ele responde com uma frase aleatória (como "O que foi?", "Oi?" ou "Precisando de alguma coisa?"). A implementação fica no cog `comandos/mencao.py`:

```python
# comandos/mencao.py
RESPOSTAS_MENCAO = (
    "O que foi?",
    "Oi?",
    "Precisando de alguma coisa?",
    "Fala!",
    "Achei que era sobre o feed de imagens.",
    "Me marca pra quê?",
)

class ResponderMencao(commands.Cog):
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Responde quando o bot é mencionado diretamente."""
        if message.author.bot or message.author.id == self.bot.user.id:
            return
        if self.bot.user.mentioned_in(message):
            resposta = random.choice(RESPOSTAS_MENCAO)
            await message.channel.send(resposta)
```

> Por ser um listener de cog, ele não interfere no processamento normal dos comandos de prefixo (`$`).

## Inicialização do banco de dados

O banco de dados usa o SQLAlchemy e fica no `/models/db.py`. A URL do banco é lida da variável de ambiente `DATABASE_URL` (por padrão, `sqlite:///dados.db`):

```python
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dados.db")

engine = create_engine(DATABASE_URL)
Base = declarative_base()
_Sessao = sessionmaker(engine)
```

Ao importar o módulo, `Base.metadata.create_all(engine)` cria todas as tabelas definidas (Usuário, Avatar, Cargos, Imagens, Feed, Personagens, Tickets, etc.). Depois, `_migrar_colunas()` adiciona colunas novas a tabelas existentes sem apagar os dados.

## Estrutura do projeto

```
.
├── main.py              # Inicialização, on_ready e carregamento dos cogs
├── comandos/            # Cogs de interação com o Discord
│   ├── ajuda.py         # /ajuda
│   ├── avatar.py        # /avatar (histórico de avatares)
│   ├── cargos.py        # Cargos automáticos + evento on_member_join
│   ├── dados.py         # $r (rolagem de dados)
│   ├── doar_personagem.py  # /doar_personagem
│   ├── feed.py          # /configurar_feed, /listar_feeds, /remover_feed
│   ├── game.py          # $jogar (jogo de personagens)
│   ├── imagem.py        # /adicionar_imagem, /imagem_aleatoria, /minhas_imagens, /remover_imagem
│   ├── mencao.py        # Responde quando o bot é mencionado
│   ├── personagens.py   # /listar_personagens, /verificar_personagem
│   ├── ping.py          # /ping
│   ├── reacao.py        # /configurar_chat, /listar_chats, /remover_chat
│   ├── register.py      # /registrar, /perfil, /usuarios_registrados
│   ├── saudacoes.py     # Escuta bom dia / boa tarde / boa noite
│   └── ticket.py        # Sistema de tickets
├── models/              # Regras de negócio e acesso ao banco de dados
│   ├── db.py            # Modelos do banco (SQLAlchemy) e migrações
│   ├── Obter_cargo.py   # Operações de cargos + atribuição automática
│   ├── Obter_saudacao.py    # Respostas e horários das saudações
│   ├── Obter_dia.py         # Registro diário das saudações
│   ├── Obter_Usuario.py     # Operações de usuário (moedas, XP, nível)
│   └── ...
└── docs/                # Documentação dos comandos e funcionamento
```

### Por que separar `comandos` de `models`?

- **`comandos/`** cuida apenas da interação: escutar mensagens, responder no chat, montar embeds e views.
- **`models/`** concentra a lógica: horários, respostas, cálculos e todo o acesso ao banco de dados.

Isso deixa o código mais fácil de testar e manter, já que cada parte tem uma responsabilidade única.
