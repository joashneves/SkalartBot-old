from models.db import _Sessao, DiaGuarda
from datetime import datetime


class Manipular_dia:
    SAUDACOES = ("bomdia", "boatarde", "boanoite")

    @staticmethod
    def registrar_saudacao(id_discord: str, tipo: str):
        if tipo not in Manipular_dia.SAUDACOES:
            raise ValueError(f"Saudação inválida: {tipo}")
        agora = datetime.now()
        with _Sessao() as sessao:
            usuario = sessao.query(DiaGuarda).filter_by(id_discord=id_discord).first()
            if usuario:
                setattr(usuario, tipo, getattr(usuario, tipo) + 1)
                setattr(usuario, f"{tipo}_data", agora)
                sessao.commit()
                return
            dados = {"id_discord": id_discord}
            for t in Manipular_dia.SAUDACOES:
                dados[t] = 1 if t == tipo else 0
                dados[f"{t}_data"] = agora
            sessao.add(DiaGuarda(**dados))
            sessao.commit()

    @staticmethod
    def obter_saudacao(id_discord: str, tipo: str):
        if tipo not in Manipular_dia.SAUDACOES:
            raise ValueError(f"Saudação inválida: {tipo}")
        with _Sessao() as sessao:
            usuario = sessao.query(DiaGuarda).filter_by(id_discord=id_discord).first()
            if usuario:
                return {
                    "numero": getattr(usuario, tipo),
                    "data": getattr(usuario, f"{tipo}_data"),
                }
            return None

    @staticmethod
    def registrar_bomdia(id_discord: str):
        return Manipular_dia.registrar_saudacao(id_discord, "bomdia")

    @staticmethod
    def registrar_boatarde(id_discord: str):
        return Manipular_dia.registrar_saudacao(id_discord, "boatarde")

    @staticmethod
    def registrar_boanoite(id_discord: str):
        return Manipular_dia.registrar_saudacao(id_discord, "boanoite")

    @staticmethod
    def obter_bomdia(id_discord: str):
        return Manipular_dia.obter_saudacao(id_discord, "bomdia")

    @staticmethod
    def obter_boatarde(id_discord: str):
        return Manipular_dia.obter_saudacao(id_discord, "boatarde")

    @staticmethod
    def obter_boanoite(id_discord: str):
        return Manipular_dia.obter_saudacao(id_discord, "boanoite")
