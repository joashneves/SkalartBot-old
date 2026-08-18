import pytest
from models.Obter_cargo import Manipular_Cargo


class FakeRole:
    def __init__(self, role_id, name):
        self.id = role_id
        self.name = name


class FakeMember:
    def __init__(self, member_id, roles, bot=False):
        self.id = member_id
        self.roles = roles
        self.bot = bot
        self.name = f"member_{member_id}"


class FakeGuild:
    def __init__(self, guild_id, roles, members):
        self.id = guild_id
        self.roles = roles
        self.members = members


@pytest.fixture
def cargos():
    return [FakeRole(1, "time_1"), FakeRole(2, "time_2"), FakeRole(3, "time_3")]


def test_obter_cargo_balanceado_com_populacao_equilibrada(cargos, monkeypatch):
    # 3 membros, um em cada cargo -> população equilibrada
    membros = [
        FakeMember(101, [cargos[0]]),
        FakeMember(102, [cargos[1]]),
        FakeMember(103, [cargos[2]]),
    ]
    guild = FakeGuild(10, cargos, membros)
    monkeypatch.setattr(
        Manipular_Cargo, "obter_Cargo", staticmethod(lambda gid: ["1", "2", "3"])
    )
    escolhido = Manipular_Cargo.obter_cargo_balanceado(guild)
    assert escolhido in cargos


def test_obter_cargo_balanceado_prefere_cargo_vazio(cargos, monkeypatch):
    # Dois membros com time_1 e time_2, nenhum com time_3
    membros = [
        FakeMember(101, [cargos[0]]),
        FakeMember(102, [cargos[1]]),
    ]
    guild = FakeGuild(10, cargos, membros)
    monkeypatch.setattr(
        Manipular_Cargo, "obter_Cargo", staticmethod(lambda gid: ["1", "2", "3"])
    )
    escolhido = Manipular_Cargo.obter_cargo_balanceado(guild)
    assert escolhido.id == 3  # time_3 é o menos representado


def test_obter_cargo_balanceado_ignora_membros_com_dois_cargos(cargos, monkeypatch):
    # 2 membros com time_1, 2 com time_2, 1 com time_3
    membros = [
        FakeMember(101, [cargos[0]]),
        FakeMember(102, [cargos[0]]),
        FakeMember(103, [cargos[1]]),
        FakeMember(104, [cargos[1]]),
        FakeMember(105, [cargos[2]]),
    ]
    guild = FakeGuild(10, cargos, membros)
    monkeypatch.setattr(
        Manipular_Cargo, "obter_Cargo", staticmethod(lambda gid: ["1", "2", "3"])
    )
    escolhido = Manipular_Cargo.obter_cargo_balanceado(guild)
    assert escolhido.id == 3


def test_obter_cargo_balanceado_ignora_bots(cargos, monkeypatch):
    # Só bots têm os cargos; nenhum humano -> qualquer cargo serve, empate
    membros = [
        FakeMember(201, [cargos[0]], bot=True),
        FakeMember(202, [cargos[1]], bot=True),
    ]
    guild = FakeGuild(10, cargos, membros)
    monkeypatch.setattr(
        Manipular_Cargo, "obter_Cargo", staticmethod(lambda gid: ["1", "2", "3"])
    )
    escolhido = Manipular_Cargo.obter_cargo_balanceado(guild)
    assert escolhido in cargos
