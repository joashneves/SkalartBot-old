from datetime import date, timedelta
from models.db import _Sessao, DailyGuarda


class Manipular_Diario:
    MOEDAS_BASE = 50
    MOEDAS_POR_STREAK = 10
    STREAK_MAX = 7

    @staticmethod
    def resgatar_daily(id_discord: str):
        """Resgata a recompensa diária. Retorna (moedas, streak) ou None se já resgatou hoje."""
        hoje = date.today().isoformat()
        ontem = (date.today() - timedelta(days=1)).isoformat()
        with _Sessao() as sessao:
            registro = (
                sessao.query(DailyGuarda)
                .filter_by(id_discord=str(id_discord))
                .first()
            )
            if not registro:
                registro = DailyGuarda(
                    id_discord=str(id_discord), ultima_data=hoje, streak=1
                )
                sessao.add(registro)
                sessao.commit()
                return Manipular_Diario.MOEDAS_BASE, 1

            if registro.ultima_data == hoje:
                return None

            if registro.ultima_data == ontem:
                registro.streak += 1
            else:
                registro.streak = 1
            registro.ultima_data = hoje
            sessao.commit()

            streak = min(registro.streak, Manipular_Diario.STREAK_MAX)
            moedas = (
                Manipular_Diario.MOEDAS_BASE
                + Manipular_Diario.MOEDAS_POR_STREAK * (streak - 1)
            )
            return moedas, streak

    @staticmethod
    def obter_streak(id_discord: str):
        with _Sessao() as sessao:
            registro = (
                sessao.query(DailyGuarda)
                .filter_by(id_discord=str(id_discord))
                .first()
            )
            if not registro:
                return 0
            return registro.streak

    @staticmethod
    def resgatou_hoje(id_discord: str) -> bool:
        with _Sessao() as sessao:
            registro = (
                sessao.query(DailyGuarda)
                .filter_by(id_discord=str(id_discord))
                .first()
            )
            if not registro:
                return False
            return registro.ultima_data == date.today().isoformat()
