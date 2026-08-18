from datetime import datetime
from models.db import _Sessao, AvatarSalvo


class Manipular_Avatar:
    @staticmethod
    def salvar_avatar(
        id_discord: str, caminho_arquivo: str, hash_avatar: str, data_arquivo: datetime
    ):
        with _Sessao() as sessao:
            avatar_existente = (
                sessao.query(AvatarSalvo)
                .filter_by(id_discord=id_discord, hash_avatar=hash_avatar)
                .first()
            )
            if not avatar_existente:
                novo_avatar = AvatarSalvo(
                    id_discord=id_discord,
                    caminho_arquivo=caminho_arquivo,
                    hash_avatar=hash_avatar,
                    data_arquivo=data_arquivo,
                )
                sessao.add(novo_avatar)
                sessao.commit()
                return novo_avatar
            return avatar_existente

    @staticmethod
    def listar_avatares(id_discord: str):
        with _Sessao() as sessao:
            return (
                sessao.query(AvatarSalvo)
                .filter_by(id_discord=id_discord)
                .order_by(AvatarSalvo.data_arquivo.desc())
                .all()
            )

    @staticmethod
    def remover_avatar(id_discord: str, avatar_id: int):
        with _Sessao() as sessao:
            avatar = (
                sessao.query(AvatarSalvo)
                .filter_by(id_discord=id_discord, id=avatar_id)
                .first()
            )
            if avatar:
                sessao.delete(avatar)
                sessao.commit()
                return True
            return False
