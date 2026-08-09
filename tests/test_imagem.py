import pytest
from models.Obter_imagem import Manipular_Imagem
from models.db import _Sessao, ImagemGuarda


@pytest.fixture(autouse=True)
def limpar_banco():
    with _Sessao() as sessao:
        sessao.query(ImagemGuarda).delete()
        sessao.commit()


def test_criar_imagem():
    sucesso = Manipular_Imagem.criar_Imagem("123", "imagens_usuarios/x.png", "desc")
    assert sucesso is True


def test_listar_imagens_por_usuario():
    Manipular_Imagem.criar_Imagem("123", "imagens_usuarios/a.png", "desc1")
    Manipular_Imagem.criar_Imagem("123", "imagens_usuarios/b.png", "desc2")
    imagens = Manipular_Imagem.listar_imagens_usuario("123")
    assert len(imagens) == 2


def test_obter_imagem_aleatoria():
    Manipular_Imagem.criar_Imagem("123", "imagens_usuarios/a.png", "desc1")
    imagem = Manipular_Imagem.obter_imagem_aleatoria()
    assert imagem is not None
    assert imagem.id_discord == "123"


def test_obter_imagem_aleatoria_vazio():
    assert Manipular_Imagem.obter_imagem_aleatoria() is None


def test_imagem_hoje():
    Manipular_Imagem.criar_Imagem("123", "imagens_usuarios/a.png", "desc1")
    assert Manipular_Imagem.imagem_hoje("123") is True


def test_imagem_hoje_usuario_sem_imagem():
    assert not Manipular_Imagem.imagem_hoje("999")
