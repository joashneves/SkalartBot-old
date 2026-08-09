from datetime import date, datetime
from models.Obter_saudacao import Manipular_saudacao


def test_detectar_saudacao_reconhece_bom_dia():
    assert Manipular_saudacao.detectar_saudacao("bom dia pessoal") == "bom dia"


def test_detectar_saudacao_reconhece_boa_tarde():
    assert Manipular_saudacao.detectar_saudacao("boa tarde, como vai?") == "boa tarde"


def test_detectar_saudacao_reconhece_boa_noite():
    assert Manipular_saudacao.detectar_saudacao("boa noite galera") == "boa noite"


def test_detectar_saudacao_ignora_texto_sem_saudacao():
    assert Manipular_saudacao.detectar_saudacao("oi pessoal") is None


def test_periodo_manha():
    assert Manipular_saudacao._periodo_do_dia(8) == "manha"


def test_periodo_tarde():
    assert Manipular_saudacao._periodo_do_dia(14) == "tarde"


def test_periodo_noite():
    assert Manipular_saudacao._periodo_do_dia(20) == "noite"


def test_periodo_madrugada():
    assert Manipular_saudacao._periodo_do_dia(3) == "madrugada"


def test_bom_dia_valido_pela_manha():
    assert Manipular_saudacao.eh_periodo_valido("bom dia", 9)


def test_bom_dia_invalido_a_noite():
    assert not Manipular_saudacao.eh_periodo_valido("bom dia", 22)


def test_boa_noite_valida_de_madrugada():
    assert Manipular_saudacao.eh_periodo_valido("boa noite", 1)


def test_data_pascoa_conhecida():
    # Domingo de Páscoa de 2024 foi 31/03
    assert Manipular_saudacao._data_pascoa(2024) == date(2024, 3, 31)


def test_segundo_domingo_de_maio_2024():
    # Segundo domingo de maio de 2024 foi 12/05
    assert Manipular_saudacao._segundo_domingo(2024, 5) == date(2024, 5, 12)


def test_dia_especial_natal():
    agora = datetime(2025, 12, 25, 10, 0)
    resposta = Manipular_saudacao.obter_resposta("bom dia", agora, "Joao")
    assert "Natal" in resposta


def test_dia_especial_ano_novo():
    agora = datetime(2025, 1, 1, 10, 0)
    resposta = Manipular_saudacao.obter_resposta("bom dia", agora, "Joao")
    assert "Ano Novo" in resposta


def test_resposta_comum_inclui_nome():
    agora = datetime(2025, 6, 1, 9, 0)
    resposta = Manipular_saudacao.obter_resposta("bom dia", agora, "Maria")
    assert "Maria" in resposta
