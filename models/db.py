import os
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import inspect, text

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dados.db")

engine = create_engine(DATABASE_URL)
Base = declarative_base()
_Sessao = sessionmaker(engine, expire_on_commit=False)


class Usuario(Base):
    __tablename__ = "Usuario"
    id = Column(Integer, primary_key=True)
    id_discord = Column(String)
    apelido = Column(String, default="apelido")
    usuario = Column(String, default="usuario")
    rede_social = Column(String, default="url")
    descricao = Column(String, default="descrição")
    pronome = Column(String, default="N/a")
    caminho_arquivo = Column(String, nullable=True)
    level = Column(Integer, default=0)
    xp = Column(Integer, default=0)
    saldo = Column(Integer, default=0)
    data_criacao = Column(Integer, default=0)


class ServidorConfig(Base):
    __tablename__ = "servidorConfig"
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, nullable=False, index=True)
    channel_id = Column(String, nullable=False, index=True)


class AvatarSalvo(Base):
    __tablename__ = "AvataresDiscord"
    id = Column(Integer, primary_key=True)
    id_discord = Column(String, nullable=False)
    caminho_arquivo = Column(String, nullable=False)
    hash_avatar = Column(String, nullable=False)
    data_arquivo = Column(DateTime, nullable=False)


class CargosSalvos(Base):
    __tablename__ = "cargosSalvos"
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, nullable=True)
    cargo_id = Column(String, nullable=True)


class ImagemGuarda(Base):
    __tablename__ = "imagemGuarda"
    id = Column(Integer, primary_key=True, index=True)
    id_discord = Column(String, nullable=True)
    caminho_arquivo = Column(String, nullable=True)
    descricao = Column(String, nullable=True)
    data_arquivo = Column(DateTime, nullable=False)


class DiaGuarda(Base):
    __tablename__ = "diaGuarda"
    id = Column(Integer, primary_key=True, index=True)
    id_discord = Column(String, nullable=True)
    bomdia = Column(Integer, default=0, nullable=False)
    boatarde = Column(Integer, default=0, nullable=False)
    boanoite = Column(Integer, default=0, nullable=False)
    bomdia_data = Column(DateTime, nullable=False)
    boatarde_data = Column(DateTime, nullable=False)
    boanoite_data = Column(DateTime, nullable=False)


class FeedConfig(Base):
    __tablename__ = "feedConfig"
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, nullable=False, index=True)
    channel_id = Column(String, nullable=False, index=True)


class Personagem(Base):
    __tablename__ = "personagem"
    id = Column(Integer, primary_key=True, index=True)
    id_discord = Column(String, nullable=False, index=True)
    guild_id = Column(String, nullable=False, index=True)
    channel_id = Column(String, nullable=False, index=True)
    id_personagem = Column(Integer, nullable=False, index=False)
    nome_personagem = Column(String, nullable=False, index=False)
    descricao_personagem = Column(String, nullable=False, default="Faça sua descrição")
    genero_personagem = Column(String, nullable=False, index=False)
    franquia_personagem = Column(String, nullable=False, index=False)
    caminho_arquivo_personagem = Column(String, nullable=False, index=False)
    data_de_descoberta = Column(DateTime, nullable=False)


class TicketConfig(Base):
    __tablename__ = "ticket_Config"
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, nullable=True)
    categoria_id = Column(String, nullable=True)
    cargo_id = Column(String, nullable=True)


class DailyGuarda(Base):
    __tablename__ = "dailyGuarda"
    id = Column(Integer, primary_key=True, index=True)
    id_discord = Column(String, nullable=True, index=True)
    ultima_data = Column(String, nullable=True)  # yyyy-mm-dd
    streak = Column(Integer, default=0)


class Sugestao(Base):
    __tablename__ = "sugestoes"
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, nullable=True, index=True)
    id_discord = Column(String, nullable=True)
    texto = Column(String, nullable=True)
    canal_id = Column(String, nullable=True)
    mensagem_id = Column(String, nullable=True)
    data_criacao = Column(DateTime, nullable=True)


class SugestaoConfig(Base):
    __tablename__ = "sugestao_config"
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, nullable=True, index=True)
    channel_id = Column(String, nullable=True)


class Lembrete(Base):
    __tablename__ = "lembretes"
    id = Column(Integer, primary_key=True, index=True)
    id_discord = Column(String, nullable=True, index=True)
    texto = Column(String, nullable=True)
    data_agendada = Column(DateTime, nullable=True)
    criado_em = Column(DateTime, nullable=True)
    canal_id = Column(String, nullable=True)
    guild_id = Column(String, nullable=True)
    enviado = Column(Boolean, default=False)


class SlowmodeNivel(Base):
    __tablename__ = "slowmode_nivel"
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, nullable=True, index=True)
    channel_id = Column(String, nullable=True, index=True)
    nivel_minimo = Column(Integer, default=0)


class AtividadeGuarda(Base):
    __tablename__ = "atividadeGuarda"
    id = Column(Integer, primary_key=True, index=True)
    id_discord = Column(String, nullable=True, index=True)
    guild_id = Column(String, nullable=True, index=True)
    data = Column(String, nullable=True)  # yyyy-mm-dd
    mensagens = Column(Integer, default=0)


class NoticiaConfig(Base):
    __tablename__ = "noticia_config"
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, nullable=True, index=True)
    feed_url = Column(String, nullable=True)
    canal_id = Column(String, nullable=True)
    ultimo_link = Column(String, nullable=True)


class StreamConfig(Base):
    __tablename__ = "stream_config"
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, nullable=True, index=True)
    tipo = Column(String, nullable=True)  # "twitch" ou "youtube"
    canal_identificador = Column(String, nullable=True)
    canal_postagem = Column(String, nullable=True)
    ultimo_item = Column(String, nullable=True)
    cargos = Column(
        String, nullable=True, default=""
    )  # IDs de cargos separados por vírgula


Base.metadata.create_all(engine)


def _migrar_colunas():
    """Adiciona colunas novas a tabelas existentes sem apagar os dados."""
    with engine.connect() as conn:
        if inspect(conn).has_table("diaGuarda"):
            colunas = {
                coluna["name"] for coluna in inspect(conn).get_columns("diaGuarda")
            }
            novas_colunas = {
                "boatarde": (
                    "ALTER TABLE diaGuarda ADD COLUMN boatarde INTEGER DEFAULT 0 NOT NULL"
                ),
                "boatarde_data": (
                    "ALTER TABLE diaGuarda ADD COLUMN boatarde_data DATETIME DEFAULT '1900-01-01 00:00:00'"
                ),
            }
            for nome, comando in novas_colunas.items():
                if nome not in colunas:
                    conn.execute(text(comando))
        if inspect(conn).has_table("stream_config"):
            colunas = {
                coluna["name"] for coluna in inspect(conn).get_columns("stream_config")
            }
            if "cargos" not in colunas:
                conn.execute(
                    text(
                        "ALTER TABLE stream_config ADD COLUMN cargos VARCHAR DEFAULT ''"
                    )
                )
        conn.commit()


_migrar_colunas()
