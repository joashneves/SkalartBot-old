from models.db import _Sessao, SlowmodeNivel


class Manipular_Slowmode:
    @staticmethod
    def configurar_nivel(guild_id: str, channel_id: str, nivel_minimo: int):
        with _Sessao() as sessao:
            config = (
                sessao.query(SlowmodeNivel)
                .filter_by(guild_id=str(guild_id), channel_id=str(channel_id))
                .first()
            )
            if config:
                config.nivel_minimo = nivel_minimo
                sessao.commit()
                return config
            novo = SlowmodeNivel(
                guild_id=str(guild_id), channel_id=str(channel_id), nivel_minimo=nivel_minimo
            )
            sessao.add(novo)
            sessao.commit()
            return novo

    @staticmethod
    def obter_nivel(guild_id: str, channel_id: str):
        with _Sessao() as sessao:
            config = (
                sessao.query(SlowmodeNivel)
                .filter_by(guild_id=str(guild_id), channel_id=str(channel_id))
                .first()
            )
            return config.nivel_minimo if config else None

    @staticmethod
    def remover_config(guild_id: str, channel_id: str):
        with _Sessao() as sessao:
            config = (
                sessao.query(SlowmodeNivel)
                .filter_by(guild_id=str(guild_id), channel_id=str(channel_id))
                .first()
            )
            if config:
                sessao.delete(config)
                sessao.commit()
                return True
            return False

    @staticmethod
    def listar_configs(guild_id: str):
        with _Sessao() as sessao:
            return sessao.query(SlowmodeNivel).filter_by(guild_id=str(guild_id)).all()
