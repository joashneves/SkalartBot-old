# Introdução

- Guia
   - [Guia](#guia)
   - [Funcionalidades](#funcionalidades)
   - [Estrutura do Projeto](#estrutura-do-projeto)
   - [Saudações](#saudações)
   - [Clonando](#clonando)
   - [Rodando com Docker](#rodando-com-docker)
   - [Pré-commit Hook](#pré-commit-hook)
   - [As Issues](#as-issues)
   - [Objetivo](#objetivo)

# Guia

Esse é o começo do bot, sua explicação, seu funcionamento, comandos e como foi construido.

- [Comandos](./docs/comandos.md)
- [Funcionamento](./docs/funcionamento.md)
- [Extras](./docs/extras.md)

# Funcionalidades

O bot já conta com uma série de funcionalidades, separadas por **comandos** (a camada de interação com o Discord) e **models** (a camada de regras e acesso ao banco de dados):

- **Saudações inteligentes:** reconhece `bom dia`, `boa tarde` e `boa noite`, responde de forma diferente a cada vez e lembra de dias especiais.
- **Sistema de Perfis:** crie um perfil com `/registrar`, veja o seu ou o de outros com `/perfil` e liste os registrados com `/usuarios_registrados`.
- **Feed de Imagens:** envie imagens com `/adicionar_imagem`, veja as suas com `/minhas_imagens` e resgate uma aleatória com `/imagem_aleatoria`.
- **Cargos Automáticos:** configure cargos com `/configurar_cargo` para serem atribuídos aleatoriamente a novos membros.
- **Reações Automáticas:** configure canais com `/configurar_chat` para reagir a imagens enviadas.
- **Sistema de Tickets:** abra, feche e configure tickets com `/enviar_ticket`, `/apagar_ticket` e `/configurar_ticket`.
- **Jogo de Personagens:** capture e adivinhe personagens com `$jogar`, colecione e doe com `/listar_personagens` e `/doar_personagem`.
- **Economia:** acumule moedas e XP interagindo com o bot e suba de nível.
- **Comandos diversos:** `/ping` para latência e `$r 2d20` para rolar dados.

# Estrutura do Projeto

O projeto é organizado em duas grandes camadas, separando a regra de negócio da interação com o Discord:

```
.
├── main.py              # Inicializa o bot, eventos e carregamento de comandos
├── comandos/            # Cogs de interação com o Discord
│   ├── saudacoes.py     # Escuta mensagens de bom dia / boa tarde / boa noite
│   ├── register.py      # Perfis de usuários
│   ├── imagem.py        # Feed de imagens
│   ├── avatar.py        # Histórico de avatares
│   ├── cargos.py        # Cargos automáticos
│   ├── ticket.py        # Sistema de tickets
│   ├── game.py          # Jogo de personagens
│   └── ...
├── models/              # Regras de negócio e acesso ao banco de dados
│   ├── db.py            # Modelos do banco (SQLAlchemy) e migrações
│   ├── Obter_saudacao.py# Respostas e horários das saudações
│   ├── Obter_dia.py     # Registro diário das saudações
│   ├── Obter_Usuario.py # Operações de usuário (moedas, XP, nível)
│   └── ...
└── docs/                # Documentação dos comandos e funcionamento
```

### Por que separar `comandos` de `models`?

- **`comandos/`** cuida apenas da interação: escutar mensagens, responder no chat, montar embeds e views.
- **`models/`** concentra a lógica: horários, respostas, cálculos e todo o acesso ao banco de dados.

Isso deixa o código mais fácil de testar e de manter, já que cada parte tem uma responsabilidade única.

# Saudações

O bot escuta mensagens no chat e identifica `bom dia`, `boa tarde` e `boa noite` para responder.

### Horários certos

Cada saudação só vale no período correto do dia (fuso de Brasília):

| Saudação     | Período válido        |
| ------------ | --------------------- |
| `bom dia`    | 05h – 11h59           |
| `boa tarde`  | 12h – 17h59           |
| `boa noite`  | 18h – 23h59 (e madrugada) |

Se a pessoa saudar fora do horário, o bot responde com uma zoação, como:

- "Já é tarde, {nome}! Bom dia ficou pra trás kkkk"
- "Ainda não é noite, {nome}! Espera o sol se pôr!"
- "Já já é boa tarde, {nome}! Espera mais um pouquinho!"

### Respostas diferentes a cada vez

Toda mensagem de saudação tem uma resposta sorteada de uma lista, então raramente o bot repete a mesma frase. Usuários registrados ainda ganham moedas e XP uma vez por dia por saudação válida.

### Dias especiais

Em datas comemorativas o bot responde com uma mensagem temática, como Natal, Ano Novo, Carnaval, Páscoa, Dia das Mães e Dia dos Pais:

- **Datas fixas:** Ano Novo, Dia da Mulher, Dia do Trabalho, Dia dos Namorados, São João, Independência, Dia das Crianças, Halloween, Finados, Proclamação da República, Consciência Negra, Natal e Réveillon.
- **Datas móveis:** Carnaval e Páscoa (calculados pela Computus) e Dia das Mães e Dia dos Pais (segundo domingo de maio e agosto).

Toda a lógica fica em `models/Obter_saudacao.py`, e o registro diário em `models/Obter_dia.py`.

# Clonando
## Comando para baixar as dependências e iniciar o bot

### Ao clonar o repositório com Python já instalado

1. Copie o arquivo de exemplo e preencha as variáveis:
   ```bash
   cp .env.example .env
   ```
   - `DISCORD_TOKEN`: token do seu bot gerado no [Portal de Desenvolvedores](https://discord.com/developers/applications).
   - `ID_USER_MASTER`: seu ID de usuário do Discord (para comandos administrativos do bot).

2. O primeiro comando para instalar as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. O segundo comando para iniciar o bot:
   ```bash
   python main.py
   ```

---

# Rodando com Docker

O bot também pode ser executado com **Docker Compose**, sem precisar configurar o Python na sua máquina.

### Pré-requisitos

- [Docker](https://docs.docker.com/engine/install/) e [Docker Compose](https://docs.docker.com/compose/install/) instalados.

### Passo a passo

1. Copie o arquivo de exemplo e preencha as variáveis:
   ```bash
   cp .env.example .env
   ```

2. Suba o bot:
   ```bash
   docker compose up -d
   ```

3. Acompanhe os logs:
   ```bash
   docker compose logs -f
   ```

4. Para parar o bot:
   ```bash
   docker compose down
   ```

### Onde ficam os dados?

Os volumes do `docker-compose.yml` garantem que o banco de dados e as imagens enviadas pelos usuários sejam mantidos fora do container:

| Diretório do host | Diretório no container | Conteúdo          |
| ----------------- | ---------------------- | ----------------- |
| `./data`          | `/app/data`            | banco de dados (SQLite) |
| `./imagens_avatars` | `/app/imagens_avatars` | avatares salvos   |
| `./imagens_usuarios` | `/app/imagens_usuarios` | imagens dos usuários |
| `./imagens_temp`  | `/app/imagens_temp`    | imagens temporárias |

> A variável `DATABASE_URL` aponta para `sqlite:////app/data/dados.db` dentro do container (caminho absoluto do SQLite requer quatro barras).

---

## Pré-commit Hook

Para garantir que o código esteja formatado corretamente e sem erros de estilo, é recomendado usar o **pre-commit**. Isso ajuda a automatizar o processo de formatação e linting.

### Passos para configurar o pre-commit:

1. Instalar o `pre-commit`:
   ```bash
   pip install pre-commit
   ```

2. Instalar os hooks configurados no projeto:
   ```bash
   pre-commit install
   ```

3. Para atualizar os hooks:
   ```bash
   pre-commit autoupdate
   ```

Isso instalará o hook do `black` para formatação de código e o `pylint` para análise estática, garantindo que o código esteja limpo antes de cada commit.

---

# As Issues

As issues são as tarefas a serem feitas e estão organizadas dentro de milestones. Você pode conferir as tarefas [aqui](https://github.com/joashneves/SkalartBot/issues).

---

# Objetivo

O objetivo deste projeto é desenvolver um bot de Discord em conjunto, enquanto se aprimora o uso do GitHub para colaboração e controle de versões.

# O objetivo do bot
A existencia do bot vem ao caso de torna o discord uma rede mais que ela ja é, com funcionalidades que tentam tornar o servidor de quem o adicinou unico e com sua propria cara, para diferenciar dos demais.

Caso voce queria adicionar o bot atualmente online [Clique aqui](https://discord.com/oauth2/authorize?client_id=1025176642236203118&scope=bot&permissions=8)
> OBS: O bot tera administrador!
Caso queria testar o bot no nosso [Servidor](https://discord.gg/h7mP7aZuY4)
