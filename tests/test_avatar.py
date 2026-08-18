import pytest
from datetime import datetime
from models.Obter_avatar import Manipular_Avatar
from models.db import _Sessao, AvatarSalvo


@pytest.fixture(autouse=True)
def limpar_banco():
    with _Sessao() as sessao:
        sessao.query(AvatarSalvo).delete()
        sessao.commit()


def test_salvar_avatar():
    Manipular_Avatar.salvar_avatar(
        "123", "imagens_avatars/a.png", "hash1", datetime.utcnow()
    )
    avatares = Manipular_Avatar.listar_avatares("123")
    assert len(avatares) == 1
    assert avatares[0].caminho_arquivo == "imagens_avatars/a.png"


def test_salvar_avatar_nao_duplica_mesmo_hash():
    Manipular_Avatar.salvar_avatar(
        "123", "imagens_avatars/a.png", "hash1", datetime.utcnow()
    )
    Manipular_Avatar.salvar_avatar(
        "123", "imagens_avatars/a.png", "hash1", datetime.utcnow()
    )
    avatares = Manipular_Avatar.listar_avatares("123")
    assert len(avatares) == 1


def test_remover_avatar():
    Manipular_Avatar.salvar_avatar(
        "123", "imagens_avatars/a.png", "hash1", datetime.utcnow()
    )
    avatares = Manipular_Avatar.listar_avatares("123")
    removido = Manipular_Avatar.remover_avatar("123", avatares[0].id)
    assert removido is True
    assert Manipular_Avatar.listar_avatares("123") == []


def test_remover_avatar_inexistente():
    assert Manipular_Avatar.remover_avatar("999", 999) is False
