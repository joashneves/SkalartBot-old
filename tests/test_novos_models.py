import pytest
from datetime import datetime, timedelta
from models.Obter_Diario import Manipular_Diario
from models.Obter_Sugestao import Manipular_Sugestao
from models.Obter_Lembrete import Manipular_Lembrete
from models.Obter_Slowmode import Manipular_Slowmode
from models.Obter_Atividade import Manipular_Atividade
from models.Obter_Noticia import Manipular_Noticia
from models.Obter_Stream import Manipular_Stream
from models.db import (
    _Sessao,
    DailyGuarda,
    Sugestao,
    SugestaoConfig,
    Lembrete,
    SlowmodeNivel,
    AtividadeGuarda,
    NoticiaConfig,
    StreamConfig,
)

TABELAS = [
    DailyGuarda,
    Sugestao,
    SugestaoConfig,
    Lembrete,
    SlowmodeNivel,
    AtividadeGuarda,
    NoticiaConfig,
    StreamConfig,
]


@pytest.fixture(autouse=True)
def limpar_banco():
    with _Sessao() as sessao:
        for tabela in TABELAS:
            sessao.query(tabela).delete()
        sessao.commit()


class TestDaily:
    def test_primeiro_daily(self):
        moedas, streak = Manipular_Diario.resgatar_daily("1")
        assert moedas == Manipular_Diario.MOEDAS_BASE
        assert streak == 1

    def test_daily_duplicado_no_mesmo_dia(self):
        Manipular_Diario.resgatar_daily("2")
        assert Manipular_Diario.resgatar_daily("2") is None

    def test_streak_incrementa_no_dia_seguinte(self):
        Manipular_Diario.resgatar_daily("3")
        with _Sessao() as sessao:
            registro = sessao.query(DailyGuarda).filter_by(id_discord="3").first()
            ontem = (datetime.now() - timedelta(days=1)).date().isoformat()
            registro.ultima_data = ontem
            sessao.commit()
        moedas, streak = Manipular_Diario.resgatar_daily("3")
        assert streak == 2
        assert moedas > Manipular_Diario.MOEDAS_BASE

    def test_streak_reseta_se_pulou_um_dia(self):
        Manipular_Diario.resgatar_daily("4")
        with _Sessao() as sessao:
            registro = sessao.query(DailyGuarda).filter_by(id_discord="4").first()
            ha_dois_dias = (datetime.now() - timedelta(days=2)).date().isoformat()
            registro.ultima_data = ha_dois_dias
            sessao.commit()
        moedas, streak = Manipular_Diario.resgatar_daily("4")
        assert streak == 1


class TestSugestao:
    def test_configurar_e_obter_canal(self):
        Manipular_Sugestao.configurar_canal("g1", "123")
        assert Manipular_Sugestao.obter_canal("g1") == "123"

    def test_obter_canal_nao_configurado(self):
        assert Manipular_Sugestao.obter_canal("g0") is None

    def test_criar_e_listar_sugestoes(self):
        Manipular_Sugestao.criar_sugestao("g1", "u1", "Ideia boa", "123")
        Manipular_Sugestao.criar_sugestao("g1", "u2", "Outra ideia", "123")
        sugestoes = Manipular_Sugestao.listar_sugestoes("g1")
        assert len(sugestoes) == 2
        assert sugestoes[0].texto == "Outra ideia"  # ordena por id desc


class TestLembrete:
    def test_criar_e_obter_pendentes(self):
        Manipular_Lembrete.criar_lembrete(
            "u1", "Beber água", datetime.now() - timedelta(minutes=1), "123", "g1"
        )
        pendentes = Manipular_Lembrete.obter_lembretes_pendentes()
        assert len(pendentes) == 1
        assert pendentes[0].texto == "Beber água"

    def test_nao_obtem_lembrete_futuro(self):
        Manipular_Lembrete.criar_lembrete(
            "u1", "Futuro", datetime.now() + timedelta(hours=1), "123", "g1"
        )
        assert Manipular_Lembrete.obter_lembretes_pendentes() == []

    def test_marcar_enviado(self):
        lembrete = Manipular_Lembrete.criar_lembrete(
            "u1", "Teste", datetime.now() - timedelta(minutes=1), "123", "g1"
        )
        assert Manipular_Lembrete.marcar_enviado(lembrete.id) is True
        assert Manipular_Lembrete.obter_lembretes_pendentes() == []

    def test_cancelar_lembrete(self):
        lembrete = Manipular_Lembrete.criar_lembrete(
            "u1", "Cancelar", datetime.now() + timedelta(hours=1), "123", "g1"
        )
        assert Manipular_Lembrete.cancelar_lembrete("u1", lembrete.id) is True
        assert Manipular_Lembrete.cancelar_lembrete("u1", lembrete.id) is False


class TestSlowmode:
    def test_configurar_e_obter_nivel(self):
        Manipular_Slowmode.configurar_nivel("g1", "123", 5)
        assert Manipular_Slowmode.obter_nivel("g1", "123") == 5

    def test_obter_nivel_nao_configurado(self):
        assert Manipular_Slowmode.obter_nivel("g1", "999") is None

    def test_remover_config(self):
        Manipular_Slowmode.configurar_nivel("g1", "123", 3)
        assert Manipular_Slowmode.remover_config("g1", "123") is True
        assert Manipular_Slowmode.obter_nivel("g1", "123") is None


class TestAtividade:
    def test_registrar_e_obter(self):
        Manipular_Atividade.registrar_mensagem("u1", "g1")
        Manipular_Atividade.registrar_mensagem("u1", "g1")
        dados = Manipular_Atividade.obter_atividade_usuario("u1", "g1")
        assert dados["hoje"] == 2
        assert dados["total"] == 2
        assert dados["dias_ativos"] == 1

    def test_top_hoje(self):
        Manipular_Atividade.registrar_mensagem("u1", "g1")
        Manipular_Atividade.registrar_mensagem("u1", "g1")
        Manipular_Atividade.registrar_mensagem("u2", "g1")
        top = Manipular_Atividade.top_hoje("g1")
        assert top[0].id_discord == "u1"
        assert top[0].mensagens == 2

    def test_top_total(self):
        Manipular_Atividade.registrar_mensagem("u1", "g1")
        Manipular_Atividade.registrar_mensagem("u1", "g1")
        Manipular_Atividade.registrar_mensagem("u2", "g1")
        top = Manipular_Atividade.top_total("g1")
        assert top[0] == ("u1", 2)


class TestNoticia:
    def test_adicionar_e_listar_feed(self):
        Manipular_Noticia.adicionar_feed("g1", "https://exemplo.com/feed", "123")
        feeds = Manipular_Noticia.listar_feeds("g1")
        assert len(feeds) == 1
        assert feeds[0].feed_url == "https://exemplo.com/feed"

    def test_atualizar_ultimo_link(self):
        config = Manipular_Noticia.adicionar_feed(
            "g1", "https://exemplo.com/feed", "123"
        )
        assert Manipular_Noticia.atualizar_ultimo_link(config.id, "link1") is True
        feeds = Manipular_Noticia.listar_feeds("g1")
        assert feeds[0].ultimo_link == "link1"


class TestStream:
    def test_adicionar_e_listar_stream(self):
        Manipular_Stream.adicionar_stream("g1", "twitch", "meucanal", "123")
        streams = Manipular_Stream.listar_streams("g1")
        assert len(streams) == 1
        assert streams[0].tipo == "twitch"
        assert streams[0].canal_identificador == "meucanal"

    def test_remover_stream(self):
        Manipular_Stream.adicionar_stream("g1", "youtube", "UC123", "123")
        assert Manipular_Stream.remover_stream("g1", "youtube", "UC123") is True
        assert Manipular_Stream.remover_stream("g1", "youtube", "UC123") is False

    def test_atualizar_ultimo_item(self):
        config = Manipular_Stream.adicionar_stream("g1", "twitch", "c", "123")
        assert Manipular_Stream.atualizar_ultimo_item(config.id, "item1") is True

    def test_adicionar_stream_com_cargos(self):
        config = Manipular_Stream.adicionar_stream(
            "g1", "twitch", "meucanal", "123", cargos=["111", "222"]
        )
        assert Manipular_Stream._cargos_para_lista(config.cargos) == ["111", "222"]

    def test_configurar_sem_cargos_preserva_existentes(self):
        Manipular_Stream.adicionar_stream(
            "g1", "twitch", "meucanal", "123", cargos=["111"]
        )
        config = Manipular_Stream.adicionar_stream("g1", "twitch", "meucanal", "456")
        assert Manipular_Stream._cargos_para_lista(config.cargos) == ["111"]

    def test_adicionar_e_remover_cargo(self):
        Manipular_Stream.adicionar_stream("g1", "twitch", "meucanal", "123")
        config = Manipular_Stream.adicionar_cargo("g1", "twitch", "meucanal", "111")
        assert config is not None
        assert Manipular_Stream._cargos_para_lista(config.cargos) == ["111"]
        config = Manipular_Stream.adicionar_cargo("g1", "twitch", "meucanal", "111")
        assert len(Manipular_Stream._cargos_para_lista(config.cargos)) == 1
        config = Manipular_Stream.adicionar_cargo("g1", "twitch", "meucanal", "222")
        assert sorted(Manipular_Stream._cargos_para_lista(config.cargos)) == [
            "111",
            "222",
        ]
        config = Manipular_Stream.remover_cargo("g1", "twitch", "meucanal", "111")
        assert Manipular_Stream._cargos_para_lista(config.cargos) == ["222"]

    def test_cargo_em_canal_nao_configurado(self):
        assert Manipular_Stream.adicionar_cargo("g1", "twitch", "outro", "111") is None
        assert Manipular_Stream.remover_cargo("g1", "twitch", "outro", "111") is None
