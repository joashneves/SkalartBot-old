import pytest
from models.Obter_Usuario import Manipular_Usuario
from models.db import _Sessao, Usuario


@pytest.fixture(autouse=True)
def limpar_banco():
    with _Sessao() as sessao:
        sessao.query(Usuario).delete()
        sessao.commit()


@pytest.fixture
def usuario_id():
    return "123456789"


def test_criar_usuario(usuario_id):
    Manipular_Usuario.criar_usuario(
        usuario_id, "Teste", "descricao", "https://example.com", "ele/dele"
    )
    usuario = Manipular_Usuario.obter_usuario(usuario_id)
    assert usuario.id_discord == usuario_id
    assert usuario.saldo == 0
    assert usuario.level == 0


def test_obter_usuario_inexistente(usuario_id):
    assert Manipular_Usuario.obter_usuario("999999999") is None


def test_atualizar_usuario(usuario_id):
    Manipular_Usuario.criar_usuario(usuario_id, "Antigo", "desc", "url")
    Manipular_Usuario.atualizar_usuario(usuario_id, "Novo", "nova desc", "nova-url")
    usuario = Manipular_Usuario.obter_usuario(usuario_id)
    assert usuario.apelido == "Novo"
    assert usuario.descricao == "nova desc"


def test_adicionar_moedas(usuario_id):
    Manipular_Usuario.criar_usuario(usuario_id, "Teste", "desc", "url")
    Manipular_Usuario.adicionar_moedas(usuario_id, 50)
    usuario = Manipular_Usuario.obter_usuario(usuario_id)
    assert usuario.saldo == 50


def test_adicionar_xp_sobe_nivel(usuario_id):
    Manipular_Usuario.criar_usuario(usuario_id, "Teste", "desc", "url")
    # XP necessário para o nível 1: 100 * ((0+1) * 2.5) = 250
    Manipular_Usuario.adicionar_xp(usuario_id, 250)
    usuario = Manipular_Usuario.obter_usuario(usuario_id)
    assert usuario.level == 1
    assert usuario.xp == 0


def test_adicionar_xp_nao_sobe_sem_xp_suficiente(usuario_id):
    Manipular_Usuario.criar_usuario(usuario_id, "Teste", "desc", "url")
    Manipular_Usuario.adicionar_xp(usuario_id, 100)
    usuario = Manipular_Usuario.obter_usuario(usuario_id)
    assert usuario.level == 0
    assert usuario.xp == 100
