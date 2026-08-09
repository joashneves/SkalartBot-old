from models.db import _Sessao, StreamConfig


class Manipular_Stream:
    @staticmethod
    def adicionar_stream(
        guild_id: str, tipo: str, canal_identificador: str, canal_postagem: str
    ):
        with _Sessao() as sessao:
            config = (
                sessao.query(StreamConfig)
                .filter_by(
                    guild_id=str(guild_id),
                    tipo=tipo,
                    canal_identificador=canal_identificador,
                )
                .first()
            )
            if config:
                config.canal_postagem = str(canal_postagem)
                sessao.commit()
                return config
            novo = StreamConfig(
                guild_id=str(guild_id),
                tipo=tipo,
                canal_identificador=canal_identificador,
                canal_postagem=str(canal_postagem),
            )
            sessao.add(novo)
            sessao.commit()
            return novo

    @staticmethod
    def remover_stream(guild_id: str, tipo: str, canal_identificador: str):
        with _Sessao() as sessao:
            config = (
                sessao.query(StreamConfig)
                .filter_by(
                    guild_id=str(guild_id),
                    tipo=tipo,
                    canal_identificador=canal_identificador,
                )
                .first()
            )
            if config:
                sessao.delete(config)
                sessao.commit()
                return True
            return False

    @staticmethod
    def listar_streams(guild_id: str):
        with _Sessao() as sessao:
            return sessao.query(StreamConfig).filter_by(guild_id=str(guild_id)).all()

    @staticmethod
    def obter_todas_streams():
        with _Sessao() as sessao:
            return sessao.query(StreamConfig).all()

    @staticmethod
    def atualizar_ultimo_item(config_id: int, ultimo_item: str):
        with _Sessao() as sessao:
            config = sessao.query(StreamConfig).filter_by(id=config_id).first()
            if config:
                config.ultimo_item = ultimo_item
                sessao.commit()
                return True
            return False
