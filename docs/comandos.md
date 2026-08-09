# Comandos

Aqui estão todos os comandos do bot, separados por categoria. Os comandos de barra (`/`) são registrados automaticamente; os comandos com prefixo (`$`) são escritos no chat.

- [Gerais](#gerais)
- [Perfil e Imagens](#perfil-e-imagens)
- [Economia](#economia)
- [Diversão](#diversão)
- [Utilidades](#utilidades)
- [Notícias e Streams](#notícias-e-streams)
- [Jogo de Personagens](#jogo-de-personagens)
- [Administração](#administração)

---

# Gerais

## /ajuda
É o comando inicial, pensado para quem acabou de adicionar o bot. Ele mostra um menu com informações sobre:

- Sobre o bot
- Comandos gerais
- Comandos de perfil
- Comandos de imagens
- Comandos de moderação
- Comandos de ticket
- Cargos
- Feed
- Links
- Jogo de personagens

![sobre-bor](./img/sobre.png)

## /ping
Verifica a latência do bot, respondendo com o tempo de resposta em milissegundos.

## /avatar
Mostra todos os avatares da pessoa já registrados em um histórico. Ao usar o comando, o bot salva o avatar atual (seu ou da pessoa mencionada) no histórico e exibe os avatares salvos.

![avatar](./img/avatar.png)

---

# Perfil e Imagens

## /registrar
Cadastra um perfil no bot. Com o perfil criado, você pode enviar imagens para o banco de dados do bot.

> Se você já estiver registrado, o comando **atualiza** seu perfil.

Para se registrar, informe:

- **Nome:** nome que vai aparecer no seu perfil
- **Descrição:** descrição do perfil, com no máximo 255 caracteres
- **Social:** URL ou `@` de uma rede social para as pessoas entrarem em contato
- **Pronomes:** pronomes para se referir a você (opcional)

![registrar](./img/registrar.png)

## /perfil
Mostra o perfil (seu ou da pessoa mencionada), junto com todas as imagens que a pessoa já enviou.

> Só é possível ver o perfil de uma pessoa registrada.

![perfil](./img/perfil.png)

## /usuarios_registrados
Exibe uma lista dos usuários registrados no sistema do bot, com navegação entre os perfis.

## /adicionar_imagem
> Requer registro e anexo de uma imagem com descrição.

Envia uma imagem para todos os chats configurados como `feed` nos servidores em que o bot está. Ganhe moedas e XP a cada imagem enviada (limite de uma imagem por dia).

## /imagem_aleatoria
Retorna uma imagem aleatória salva no banco de dados do bot.

> Se quiser saber mais sobre o conceito, [clique aqui](./extras.md).

## /minhas_imagens
Lista todas as imagens que você já enviou, com o `ID` de cada uma.

## /remover_imagem
> Requer o `ID` da imagem.

Remove uma imagem que você enviou. O `ID` pode ser obtido com `/minhas_imagens`.

## /remover_imagens
> Apenas o dono do bot (User Master).

Remove **todas** as imagens enviadas por um usuário específico.

---

# Economia

## /daily
Resgata sua recompensa diária de moedas. Quanto mais dias seguidos você resgatar, mais moedas ganha (streak de até 7 dias).

## /rank
Mostra o ranking do servidor por **moedas** ou **XP**. Escolha o critério com `/rank tipo:xp` (padrão é moedas).

## /xp
Mostra seu nível, saldo, XP atual, XP necessário e barra de progresso até o próximo nível.

---

# Diversão

## /meme
Envia um meme aleatório do Reddit.

## /piada
Envia uma piada aleatória em português.

## /clima
> Requer `OPENWEATHER_API_KEY` no `.env` (chave gratuita em [openweathermap.org](https://openweathermap.org/api)).

Mostra o clima atual de uma cidade, com temperatura, sensação térmica, umidade e vento.

---

# Utilidades

## /lembrete
Cria um lembrete que será enviado no seu **privado** (DM). Formato da duração: `30s`, `10m`, `2h`, `1d`, `1h30m`.

#### Exemplo
```
/lembrete duracao:30m texto:Beber água
```

## /lembretes
Lista seus lembretes pendentes, com o ID de cada um.

## /cancelar_lembrete
Cancela um lembrete pendente usando o ID (veja com `/lembretes`).

## /sugestao
> Requer que o servidor tenha configurado um canal de sugestões.

Envia uma sugestão para o canal configurado, com votos de 👍 e 👎.

## /configurar_sugestao
> Apenas administração.

Define o canal onde as sugestões serão enviadas.

## /atividade
Mostra suas estatísticas de mensagens no servidor (hoje, total e dias ativos).

## /top_atividade
Mostra os membros mais ativos do servidor **hoje**.

## /top_atividade_total
Mostra os membros mais ativos do servidor no **total**.

## /configurar_slowmode
> Apenas administração.

Define um **nível mínimo** para falar em um canal. Mensagens de quem não tem o nível são apagadas automaticamente. Use `nivel:0` para remover a restrição.

## /listar_slowmodes
> Apenas administração.

Lista os canais com restrição de nível configurados.

---

# Notícias e Streams

## Notícias geek (RSS)

## /noticias_feeds_fixos
Mostra feeds geek prontos para usar (Jovem Nerd, TecMundo, IGN Brasil, Tecnoblog, Meio Bit).

## /noticias_configurar_feed
> Apenas administração. Requer um canal de feed configurado com `/configurar_feed`.

Adiciona um feed RSS geek ao servidor. As notícias novas são postadas automaticamente no canal de feed (a cada 15 minutos).

## /noticias_listar_feeds
> Apenas administração.

Lista os feeds RSS configurados no servidor.

## /noticias_remover_feed
> Apenas administração.

Remove um feed RSS configurado.

## Twitch e YouTube

## /streams_configurar
> Apenas administração. Requer `TWITCH_CLIENT_ID`, `TWITCH_SECRET` e `YOUTUBE_API_KEY` no `.env`.

Configura um canal Twitch (pelo nome) ou YouTube (pelo ID do canal) para avisar automaticamente quando o streamer **entrar em live** ou **publicar um vídeo novo**. O aviso é enviado no canal de postagem escolhido.

## /streams_listar
> Apenas administração.

Lista os canais Twitch/YouTube monitorados no servidor.

## /streams_remover
> Apenas administração.

Remove um canal Twitch/YouTube do monitoramento.

---

# Jogo de Personagens

O bot sorteia um personagem misterioso de uma API externa, e você precisa adivinhar o nome no chat. Acertando, o personagem é adicionado à sua coleção.

## $jogar
Inicia uma partida de adivinhação. Você tem um número limitado de tentativas por servidor, que são resetadas após 30 minutos. Durante a partida, responda no chat com o nome do personagem, `ff` ou `desisto!` para desistir.

> Comandos de chat (`$`), não de barra.

## /listar_personagens
Lista todos os personagens que você capturou no servidor, com opção de editar a descrição de cada um.

## /verificar_personagem
> Requer `nome` e `franquia`.

Verifica se um personagem já foi descoberto no servidor e mostra quem o capturou.

## /doar_personagem
> Requer `nome`, `franquia` e `user`.

Envia um personagem seu para outro jogador. O destinatário responde no chat com `sim` (ou `s`) para aceitar, ou `não` (ou `n`) para recusar. A troca expira em 26 segundos.

---

# Administração
Comandos executados somente pela administração do servidor (permissão de gerenciar servidor).

## /configurar_cargo
> Requer um [cargo].

Adiciona um cargo à lista de cargos atribuídos automaticamente a novos membros.

#### Exemplo
Com 3 cargos configurados (`time_1`, `time_2`, `time_3`), quando alguém novo entrar no servidor o bot sorteia um deles e aplica ao recém-chegado.

## /listar_cargos
Lista todos os cargos configurados no servidor.

## /remover_cargo
> Requer um [cargo].

Remove um cargo da lista de cargos configurados.

## /roletar_cargo
Rerola (sorteia novamente) os cargos de **todos** os membros do servidor. Essa ação é **irreversível** e pede confirmação antes de executar.

## /configurar_chat
> Requer um [canal].

Configura um canal para reagir com emojis em imagens. Textos comuns não recebem reação, mas mensagens com imagem (anexos ou URLs) recebem os emojis automáticos.

### Exemplo
![reacoes](./img/reacaoes.png)

## /listar_chats
Lista todos os canais configurados para reações.

## /remover_chat
> Requer um [canal].

Remove um canal da lista de canais de reação.

## /configurar_feed
> Requer um [canal].

Configura um canal para receber as imagens enviadas pelo comando [/adicionar_imagem](#adicionar_imagem). Assim, imagens enviadas em qualquer servidor aparecem em todos os feeds configurados.

### Exemplo
![feed](./img/imagem-exemplofeed.png)

## /listar_feeds
Lista todos os canais configurados para feeds.

## /remover_feed
> Requer um [canal].

Remove um canal da lista de feeds.

## /enviar_ticket
Abre um novo ticket, uma conversa privada com a administração do servidor.

> Requer que o sistema de tickets esteja configurado com `/configurar_ticket`.

## /apagar_ticket
Fecha o ticket atual. Só pode ser usado em um canal de ticket, pelo criador ou por quem tem o cargo configurado. O canal é apagado 5 segundos após a confirmação.

## /configurar_ticket
> Requer uma [categoria] e um [cargo].

Configura a categoria onde os tickets serão criados e o cargo com permissão para gerenciá-los. Também aplica as permissões na categoria.

## /remover_config_ticket
Remove a configuração de ticket do servidor.

## /ver_config_ticket
Mostra a categoria e o cargo atualmente configurados para tickets.

---

# Extras

## $r
Rola dados no formato `XdY`, onde `X` é a quantidade e `Y` o número de lados.

#### Exemplo
```
$r 2d20
```
Resultado: `Resultados do dado de 2d20: [14, 7]`
