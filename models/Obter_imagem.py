from datetime import datetime
from models.db import _Sessao, ImagemGuarda
import os
import random

class Manipular_Imagem:
    @staticmethod
    def criar_Imagem(id_discord: str, caminho_arquivo: str, descricao: str) -> bool:
        with _Sessao() as sessao:
            nova_imagem = ImagemGuarda(
                id_discord=id_discord,
                caminho_arquivo=caminho_arquivo,
                descricao=descricao,
                data_arquivo=datetime.utcnow(),
            )
            sessao.add(nova_imagem)
            sessao.commit()
            return True

    @staticmethod
    def obter_imagens_por_usuario(id_discord: str):
        """Obtém a última imagem enviada pelo usuário."""
        with _Sessao() as sessao:
            return (
                sessao.query(ImagemGuarda)
                .filter_by(id_discord=id_discord)
                .order_by(ImagemGuarda.data_arquivo.desc())
                .all()
            )
    @staticmethod
    def remover_imagem(id_discord: str, imagem_id: int) -> bool:
        """Remove uma imagem específica enviada pelo usuário."""
        with _Sessao() as sessao:
            imagem = sessao.query(ImagemGuarda).filter_by(id=imagem_id, id_discord=id_discord).first()
            if imagem:
                os.remove(imagem.caminho_arquivo)
                sessao.delete(imagem)
                sessao.commit()
                return True
            return False
    @staticmethod
    def listar_imagens_usuario(id_discord: str):
        """Lista todas as imagens enviadas por um usuário."""
        with _Sessao() as sessao:
            return sessao.query(ImagemGuarda).filter_by(id_discord=id_discord).all()

    @staticmethod
    def atualizar_Imagem(id_discord: str, novo_caminho: str, nova_descricao: str) -> bool:
        """Atualiza a imagem do usuário se for no mesmo dia."""
        with _Sessao() as sessao:
            hoje = datetime.utcnow().date()
            imagem = sessao.query(ImagemGuarda).filter_by(id_discord=id_discord).first()

            if imagem and imagem.data_arquivo.date() == hoje:
                imagem.caminho_arquivo = novo_caminho
                imagem.descricao = nova_descricao
                imagem.data_arquivo = datetime.utcnow()
                sessao.commit()
                return True

            return False  # O usuário não tem imagem hoje para atualizar

    @staticmethod
    def imagem_hoje(id_discord: str) -> bool:
        """Verifica se o usuário já enviou uma imagem hoje."""
        with _Sessao() as sessao:
            hoje = datetime.utcnow().date()
            imagem = sessao.query(ImagemGuarda).filter_by(id_discord=id_discord).first()
            return imagem and imagem.data_arquivo.date() == hoje

    @staticmethod
    def obter_imagem_aleatoria():
        with _Sessao() as sessao:
            imagens = sessao.query(ImagemGuarda).all()
            return random.choice(imagens) if imagens else None

    def remover_todas_imagens(id_discord: str) -> bool:
        with _Sessao() as sessao:
            imagens = sessao.query(ImagemGuarda).filter_by(id_discord=id_discord).all()

            if not imagens:
                return False  # Nenhuma imagem encontrada

            for img in imagens:
                sessao.delete(img)  # Deletar cada imagem

            sessao.commit()  # Confirmar remoção
            return True
