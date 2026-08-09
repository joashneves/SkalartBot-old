from models.db import _Sessao, NoticiaConfig


class Manipular_Noticia:
    @staticmethod
    def adicionar_feed(guild_id: str, feed_url: str, canal_id: str):
        with _Sessao() as sessao:
            config = (
                sessao.query(NoticiaConfig)
                .filter_by(guild_id=str(guild_id), feed_url=feed_url)
                .first()
            )
            if config:
                config.canal_id = str(canal_id)
                sessao.commit()
                return config
            novo = NoticiaConfig(
                guild_id=str(guild_id), feed_url=feed_url, canal_id=str(canal_id)
            )
            sessao.add(novo)
            sessao.commit()
            return novo

    @staticmethod
    def remover_feed(guild_id: str, feed_url: str):
        with _Sessao() as sessao:
            config = (
                sessao.query(NoticiaConfig)
                .filter_by(guild_id=str(guild_id), feed_url=feed_url)
                .first()
            )
            if config:
                sessao.delete(config)
                sessao.commit()
                return True
            return False

    @staticmethod
    def listar_feeds(guild_id: str):
        with _Sessao() as sessao:
            return sessao.query(NoticiaConfig).filter_by(guild_id=str(guild_id)).all()

    @staticmethod
    def obter_todos_feeds():
        with _Sessao() as sessao:
            return sessao.query(NoticiaConfig).all()

    @staticmethod
    def atualizar_ultimo_link(config_id: int, ultimo_link: str):
        with _Sessao() as sessao:
            config = sessao.query(NoticiaConfig).filter_by(id=config_id).first()
            if config:
                config.ultimo_link = ultimo_link
                sessao.commit()
                return True
            return False
