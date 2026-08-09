from datetime import date
from models.db import _Sessao, AtividadeGuarda


class Manipular_Atividade:
    @staticmethod
    def registrar_mensagem(id_discord: str, guild_id: str):
        """Incrementa a contagem de mensagens do usuário no dia atual."""
        hoje = date.today().isoformat()
        with _Sessao() as sessao:
            registro = (
                sessao.query(AtividadeGuarda)
                .filter_by(id_discord=str(id_discord), guild_id=str(guild_id), data=hoje)
                .first()
            )
            if registro:
                registro.mensagens += 1
            else:
                registro = AtividadeGuarda(
                    id_discord=str(id_discord), guild_id=str(guild_id), data=hoje, mensagens=1
                )
                sessao.add(registro)
            sessao.commit()

    @staticmethod
    def obter_atividade_usuario(id_discord: str, guild_id: str):
        hoje = date.today().isoformat()
        with _Sessao() as sessao:
            hoje_reg = (
                sessao.query(AtividadeGuarda)
                .filter_by(id_discord=str(id_discord), guild_id=str(guild_id), data=hoje)
                .first()
            )
            total = (
                sessao.query(AtividadeGuarda)
                .filter_by(id_discord=str(id_discord), guild_id=str(guild_id))
                .all()
            )
            return {
                "hoje": hoje_reg.mensagens if hoje_reg else 0,
                "total": sum(reg.mensagens for reg in total),
                "dias_ativos": sum(1 for reg in total if reg.mensagens > 0),
            }

    @staticmethod
    def top_hoje(guild_id: str, limite: int = 10):
        hoje = date.today().isoformat()
        with _Sessao() as sessao:
            return (
                sessao.query(AtividadeGuarda)
                .filter_by(guild_id=str(guild_id), data=hoje)
                .order_by(AtividadeGuarda.mensagens.desc())
                .limit(limite)
                .all()
            )

    @staticmethod
    def top_total(guild_id: str, limite: int = 10):
        """Top usuários por total de mensagens na guild."""
        with _Sessao() as sessao:
            registros = (
                sessao.query(AtividadeGuarda)
                .filter_by(guild_id=str(guild_id))
                .all()
            )
            agregado = {}
            for reg in registros:
                agregado[reg.id_discord] = agregado.get(reg.id_discord, 0) + reg.mensagens
            top = sorted(agregado.items(), key=lambda x: x[1], reverse=True)[:limite]
            return top
