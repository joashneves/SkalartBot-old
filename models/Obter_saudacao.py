"""Modelo responsável pelas respostas de saudações do bot."""

import random
from datetime import date, datetime, timedelta


class Manipular_saudacao:
    SAUDACOES = ("bom dia", "boa tarde", "boa noite")

    TIPO_BANCO = {
        "bom dia": "bomdia",
        "boa tarde": "boatarde",
        "boa noite": "boanoite",
    }

    PERIODOS_VALIDOS = {
        "bom dia": ("manha",),
        "boa tarde": ("tarde",),
        "boa noite": ("noite", "madrugada"),
    }

    RESPOSTAS = {
        "bom dia": [
            "Bom dia, {nome}!",
            "Bom diaaaa, {nome}! Que seu dia comece com o pé direito!",
            "Bom dia, {nome}! O sol nasceu e você também!",
            "Bom dia, {nome}! Já tomei meu café virtual por você!",
            "Bom dia, {nome}! Que hoje seja melhor que ontem!",
            "Bom dia, {nome}! Acorda que tem café quentinho te esperando!",
            "Bom dia, {nome}! Aproveita que o dia tá começando!",
        ],
        "boa tarde": [
            "Boa tarde, {nome}! ☕",
            "Boa tarde, {nome}! Como tá o rolê aí?",
            "Boa tarde, {nome}! Já almoçou?",
            "Boa tarde, {nome}! Metade do dia já foi, bora pra segunda!",
            "Boa tarde, {nome}! O sol tá a pino, cuidado com o calor!",
            "Boa tarde, {nome}! A tarde é nova, as ideias também!",
        ],
        "boa noite": [
            "Boa noite, {nome}!",
            "Boa noite, {nome}! Que seus sonhos sejam doces!",
            "Boa noite, {nome}! Apaga a luz que o sono chega!",
            "Boa noite, {nome}! Amanhã tem mais!",
            "Boa noite, {nome}! Não esquece de recarregar as energias!",
            "Boa noite, {nome}! Conta mais ovelhinhas aí!",
        ],
    }

    RESPOSTAS_FORA_DO_HORARIO = {
        "bom dia": {
            "madrugada": [
                "Calma, {nome}! Ainda é madrugada, já já é bom dia!",
                "Opa, {nome}! Ainda não é hora do bom dia, vai dormir mais um pouco! ",
                "Já já é bom dia, {nome}! Espera o sol nascer!",
            ],
            "tarde": [
                "Já é tarde, {nome}! Bom dia ficou pra trás kkkk ",
                "Bom dia? O dia já tá no fim, {nome}! Kkkk",
                "Agora é boa tarde, {nome}! Você tá atrasado kkk",
            ],
            "noite": [
                "Já é noite, {nome}! Vai dormir que amanhã você tenta de novo!",
                "Bom dia a essa hora, {nome}? Kkkk boa noite!",
                "Já passou da hora do bom dia, {nome}! ",
            ],
        },
        "boa tarde": {
            "madrugada": [
                "Boa tarde na madrugada, {nome}? Tá sonhando acordado? Kkkk",
                "Calma, {nome}! Agora é madrugada, não existe boa tarde!",
            ],
            "manha": [
                "Já já é boa tarde, {nome}! Espera mais um pouquinho!",
                "Calma, {nome}! Ainda é manhã, boa tarde chega depois do almoço!",
                "Quase! Já já é boa tarde, {nome}! Kkkk",
            ],
            "noite": [
                "Já é noite, {nome}! Boa tarde foi há umas horas kkkk ",
                "Boa tarde a essa hora, {nome}? Já é noite! ",
            ],
        },
        "boa noite": {
            "manha": [
                "Boa noite? É manhã, {nome}! Acorda! ",
                "Ainda é manhã, {nome}! Boa noite é só depois das 18h! Kkkk",
            ],
            "tarde": [
                "Ainda não é noite, {nome}! Espera o sol se pôr! ",
                "Calma, {nome}! Ainda é tarde, boa noite é só depois das 18h! ",
                "Boa noite cedo, {nome}? O dia ainda nem acabou! Kkkk",
            ],
        },
    }

    DIAS_ESPECIAIS = {
        (1, 1): "Feliz Ano Novo, {nome}! Que este novo ano seja incrível!",
        (3, 8): "Feliz Dia Internacional da Mulher, {nome}!",
        (5, 1): "Feliz Dia do Trabalho, {nome}!",
        (6, 12): "Feliz Dia dos Namorados, {nome}!",
        (6, 24): "Feliz São João, {nome}! Vai ter fogueira?",
        (9, 7): "🇧Feliz Dia da Independência, {nome}!",
        (10, 12): "Feliz Dia das Crianças, {nome}!",
        (10, 31): "Feliz Halloween, {nome}! Doce ou travessura?",
        (11, 2): "Neste Dia de Finados, {nome}, uma lembrança por quem se foi.",
        (11, 15): "Feliz Dia da Proclamação da República, {nome}!",
        (11, 20): "Feliz Dia da Consciência Negra, {nome}!",
        (
            12,
            24,
        ): "Véspera de Natal, {nome}! Amanhã é Natal, dorme cedo pro Papai Noel passar! 🎅",
        (12, 25): "Feliz Natal, {nome}! Que sua noite seja mágica! 🎅",
        (12, 31): "Feliz Réveillon, {nome}! Vai celebrar a chegada do novo ano?",
    }

    @staticmethod
    def detectar_saudacao(conteudo: str):
        """Retorna qual saudação foi usada na mensagem, ou None."""
        for saudacao in Manipular_saudacao.SAUDACOES:
            if saudacao in conteudo:
                return saudacao
        return None

    @staticmethod
    def _periodo_do_dia(hora: int) -> str:
        if 5 <= hora < 12:
            return "manha"
        if 12 <= hora < 18:
            return "tarde"
        if 18 <= hora <= 23:
            return "noite"
        return "madrugada"

    @staticmethod
    def eh_periodo_valido(saudacao: str, hora: int) -> bool:
        """Verifica se a saudação condiz com o período atual do dia."""
        periodo = Manipular_saudacao._periodo_do_dia(hora)
        return periodo in Manipular_saudacao.PERIODOS_VALIDOS[saudacao]

    @staticmethod
    def obter_resposta(saudacao: str, agora: datetime, nome: str) -> str:
        """Retorna uma resposta diferente a cada vez para a saudação."""
        dia_especial = Manipular_saudacao._obter_dia_especial(agora)
        if dia_especial:
            return dia_especial.format(nome=nome)

        if Manipular_saudacao.eh_periodo_valido(saudacao, agora.hour):
            respostas = Manipular_saudacao.RESPOSTAS[saudacao]
        else:
            periodo = Manipular_saudacao._periodo_do_dia(agora.hour)
            respostas = Manipular_saudacao.RESPOSTAS_FORA_DO_HORARIO[saudacao][periodo]
        return random.choice(respostas).format(nome=nome)

    @staticmethod
    def _obter_dia_especial(agora: datetime):
        hoje = agora.date()
        mensagem = Manipular_saudacao.DIAS_ESPECIAIS.get((hoje.month, hoje.day))
        if mensagem:
            return mensagem

        ano = hoje.year
        pascoa = Manipular_saudacao._data_pascoa(ano)
        if hoje == pascoa:
            return "Feliz Páscoa, {nome}! Que o chocolate abrace seu dia! 🍫"
        if hoje == pascoa - timedelta(days=47):
            return "Feliz Carnaval, {nome}! Bora brincar antes da quaresma! 🎉"
        if hoje == Manipular_saudacao._segundo_domingo(ano, 5):
            return "Feliz Dia das Mães, {nome}! Abraça tua mãe hoje!"
        if hoje == Manipular_saudacao._segundo_domingo(ano, 8):
            return "Feliz Dia dos Pais, {nome}! Um brinde aos pais!"
        return None

    @staticmethod
    def _data_pascoa(ano: int) -> date:
        """Calcula a data da Páscoa pelo algoritmo da Computus (gregoriano)."""
        a = ano % 19
        b = ano // 100
        c = ano % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        mes = (h + l - 7 * m + 114) // 31
        dia = ((h + l - 7 * m + 114) % 31) + 1
        return date(ano, mes, dia)

    @staticmethod
    def _segundo_domingo(ano: int, mes: int) -> date:
        primeiro_domingo = date(ano, mes, 1) + timedelta(
            days=(6 - date(ano, mes, 1).weekday()) % 7
        )
        return primeiro_domingo + timedelta(days=7)
