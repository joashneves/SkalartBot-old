from datetime import datetime
from models.db import _Sessao, Lembrete


class Manipular_Lembrete:
    @staticmethod
    def criar_lembrete(id_discord: str, texto: str, data_agendada: datetime, canal_id: str, guild_id: str):
        with _Sessao() as sessao:
            novo = Lembrete(
                id_discord=str(id_discord),
                texto=texto,
                data_agendada=data_agendada,
                criado_em=datetime.now(),
                canal_id=str(canal_id),
                guild_id=str(guild_id),
                enviado=False,
            )
            sessao.add(novo)
            sessao.commit()
            return novo

    @staticmethod
    def obter_lembretes_pendentes():
        """Lembretes vencidos que ainda não foram enviados."""
        with _Sessao() as sessao:
            agora = datetime.now()
            return (
                sessao.query(Lembrete)
                .filter(Lembrete.enviado == False)  # noqa: E712
                .filter(Lembrete.data_agendada <= agora)
                .all()
            )

    @staticmethod
    def marcar_enviado(lembrete_id: int):
        with _Sessao() as sessao:
            lembrete = sessao.query(Lembrete).filter_by(id=lembrete_id).first()
            if lembrete:
                lembrete.enviado = True
                sessao.commit()
                return True
            return False

    @staticmethod
    def listar_lembretes(id_discord: str):
        with _Sessao() as sessao:
            return (
                sessao.query(Lembrete)
                .filter_by(id_discord=str(id_discord), enviado=False)
                .order_by(Lembrete.data_agendada.asc())
                .all()
            )

    @staticmethod
    def cancelar_lembrete(id_discord: str, lembrete_id: int):
        with _Sessao() as sessao:
            lembrete = (
                sessao.query(Lembrete)
                .filter_by(id=lembrete_id, id_discord=str(id_discord), enviado=False)
                .first()
            )
            if lembrete:
                sessao.delete(lembrete)
                sessao.commit()
                return True
            return False
