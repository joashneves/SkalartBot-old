import pytest
from models.Obter_dia import Manipular_dia
from models.db import _Sessao, DiaGuarda


@pytest.fixture(autouse=True)
def limpar_banco():
    with _Sessao() as sessao:
        sessao.query(DiaGuarda).delete()
        sessao.commit()


def test_registrar_saudacao_invalida_levanta_erro():
    with pytest.raises(ValueError):
        Manipular_dia.registrar_saudacao("123", "invalida")


def test_registrar_e_obter_bomdia():
    Manipular_dia.registrar_bomdia("123")
    registro = Manipular_dia.obter_bomdia("123")
    assert registro is not None
    assert registro["numero"] == 1


def test_registrar_saudacao_duas_vezes_incrementa():
    Manipular_dia.registrar_boatarde("456")
    Manipular_dia.registrar_boatarde("456")
    registro = Manipular_dia.obter_boatarde("456")
    assert registro["numero"] == 2


def test_obter_saudacao_usuario_inexistente():
    assert Manipular_dia.obter_bomdia("000") is None
