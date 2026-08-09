from datetime import datetime
from models.db import _Sessao, Sugestao, SugestaoConfig


class Manipular_Sugestao:
    @staticmethod
    def obter_canal(guild_id: str):
        with _Sessao() as sessao:
            config = sessao.query(SugestaoConfig).filter_by(guild_id=str(guild_id)).first()
            return config.channel_id if config else None

    @staticmethod
    def configurar_canal(guild_id: str, channel_id: str):
        with _Sessao() as sessao:
            config = sessao.query(SugestaoConfig).filter_by(guild_id=str(guild_id)).first()
            if config:
                config.channel_id = str(channel_id)
                sessao.commit()
                return config
            novo = SugestaoConfig(guild_id=str(guild_id), channel_id=str(channel_id))
            sessao.add(novo)
            sessao.commit()
            return novo

    @staticmethod
    def criar_sugestao(guild_id: str, id_discord: str, texto: str, canal_id: str):
        with _Sessao() as sessao:
            nova = Sugestao(
                guild_id=str(guild_id),
                id_discord=str(id_discord),
                texto=texto,
                canal_id=str(canal_id),
                mensagem_id=None,
                data_criacao=datetime.now(),
            )
            sessao.add(nova)
            sessao.commit()
            return nova

    @staticmethod
    def vincular_mensagem(sugestao_id: int, mensagem_id: str):
        with _Sessao() as sessao:
            sugestao = sessao.query(Sugestao).filter_by(id=sugestao_id).first()
            if sugestao:
                sugestao.mensagem_id = str(mensagem_id)
                sessao.commit()
                return True
            return False

    @staticmethod
    def listar_sugestoes(guild_id: str):
        with _Sessao() as sessao:
            return (
                sessao.query(Sugestao)
                .filter_by(guild_id=str(guild_id))
                .order_by(Sugestao.id.desc())
                .all()
            )
