from models.db import _Sessao, StreamConfig


class Manipular_Stream:
    @staticmethod
    def _cargos_para_lista(cargos):
        """Converte a string de cargos do banco em uma lista de IDs."""
        if not cargos:
            return []
        return [c.strip() for c in str(cargos).split(",") if c.strip()]

    @staticmethod
    def adicionar_stream(
        guild_id: str,
        tipo: str,
        canal_identificador: str,
        canal_postagem: str,
        cargos=None,
    ):
        cargos_str = ",".join(str(c) for c in cargos) if cargos else ""
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
                if cargos is not None:
                    config.cargos = cargos_str
                sessao.commit()
                return config
            novo = StreamConfig(
                guild_id=str(guild_id),
                tipo=tipo,
                canal_identificador=canal_identificador,
                canal_postagem=str(canal_postagem),
                cargos=cargos_str,
            )
            sessao.add(novo)
            sessao.commit()
            return novo

    @staticmethod
    def adicionar_cargo(
        guild_id: str, tipo: str, canal_identificador: str, cargo_id: str
    ):
        """Adiciona um cargo à lista de menções de um canal configurado."""
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
            if not config:
                return None
            cargos = Manipular_Stream._cargos_para_lista(config.cargos)
            if str(cargo_id) not in cargos:
                cargos.append(str(cargo_id))
                config.cargos = ",".join(cargos)
                sessao.commit()
            return config

    @staticmethod
    def remover_cargo(
        guild_id: str, tipo: str, canal_identificador: str, cargo_id: str
    ):
        """Remove um cargo da lista de menções de um canal configurado."""
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
            if not config:
                return None
            cargos = Manipular_Stream._cargos_para_lista(config.cargos)
            if str(cargo_id) in cargos:
                cargos.remove(str(cargo_id))
                config.cargos = ",".join(cargos)
                sessao.commit()
            return config

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
