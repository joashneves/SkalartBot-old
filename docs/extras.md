# Um bot social?

A Skalart existe para tornar o Discord uma rede ainda mais completa, com funcionalidades que deixam o servidor de quem a adicionou único, com cara própria, diferente dos demais.

# Ideia

Na essência, o bot é um **compartilhamento de imagens aleatórias entre servidores** de um jeito prático e rápido. Você cria seu perfil e envia coisas; se alguém curtir seu perfil, suas ideias, imagens ou descrições, você pode mostrar seus projetos no campo `Social` do perfil, indicando outros jeitos de entrar em contato.

# Como funciona?

Quando você envia uma imagem com `/adicionar_imagem`, ela aparece em **todos os servidores** que registraram um canal de feed (`/configurar_feed`). Assim, a comunidade é sempre atualizada com imagens novas vindo de outros servidores.

## O ciclo

1. **Cadastro:** use `/registrar` para criar seu perfil.
2. **Envio:** use `/adicionar_imagem` com uma imagem e uma descrição.
3. **Distribuição:** a imagem é enviada para todos os feeds configurados nos servidores.
4. **Consumo:** qualquer pessoa pode ver imagens com `/imagem_aleatoria` ou visitar o seu perfil com `/perfil`.

## Gamificação

Interagir com o bot recompensa com **moedas** e **XP**:

- Enviar uma imagem (`/adicionar_imagem`) dá moedas e XP.
- Saudar o bot ("bom dia", "boa tarde", "boa noite") no período correto também dá moedas e XP.
- Acertar personagens no jogo (`$jogar`) dá moedas e XP.

O XP acumulado sobe o **nível** do seu perfil.

## Menção ao bot

Ao mencionar o bot diretamente (com `@Skalart`), ele responde com frases como "O que foi?", "Oi?" ou "Precisando de alguma coisa?" — sem emojis, de um jeito mais natural.

# Convite e repositório

- [Convite para o servidor da Skalart](https://discord.gg/h7mP7aZuY4)
- [Repositório do código no GitHub](https://github.com/joashneves/SkalartBot)
- [Adicionar o bot ao seu servidor](https://discord.com/oauth2/authorize?client_id=1025176642236203118&scope=bot&permissions=8)

> **OBS:** o bot é adicionado com permissões de administrador.
