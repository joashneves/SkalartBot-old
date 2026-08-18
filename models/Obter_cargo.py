import random
import discord
from models.db import _Sessao, CargosSalvos

class Manipular_Cargo():
    def obter_Cargo(guild_id:str):
        with _Sessao() as sessao:
            cargos_db = sessao.query(CargosSalvos.cargo_id).filter_by(guild_id=guild_id).all()
            return [cargo.cargo_id for cargo in cargos_db] if cargos_db else []

    def criar_Cargo(guild_id: str, cargo_id: str):
        with _Sessao() as sessao:
            new_cargo = CargosSalvos(guild_id=guild_id, cargo_id=cargo_id)
            sessao.add(new_cargo)
            sessao.commit()

    def remover_Cargo(guild_id: str, cargo_id: str) -> bool:
        with _Sessao() as sessao:
            cargo = sessao.query(CargosSalvos).filter_by(
                guild_id=guild_id, cargo_id=cargo_id
            ).first()

            if cargo:
                sessao.delete(cargo)
                sessao.commit()
                return True
            return False

    @staticmethod
    def _obter_cargo_ids_validos(guild: discord.Guild, cargos_ids):
        """Retorna os cargos configurados que ainda existem no servidor."""
        return [
            cargo for cargo_id in cargos_ids
            if (cargo := discord.utils.get(guild.roles, id=int(cargo_id)))
        ]

    @staticmethod
    def obter_cargo_balanceado(guild: discord.Guild) -> discord.Role:
        """Escolhe o cargo menos representado na população, para manter a distribuição balanceada."""
        id_guild = str(guild.id)
        cargos_ids = Manipular_Cargo.obter_Cargo(id_guild)
        cargos_validos = Manipular_Cargo._obter_cargo_ids_validos(guild, cargos_ids)
        if not cargos_validos:
            return None

        # Conta quantos membros já possuem cada cargo
        contagem = {cargo.id: 0 for cargo in cargos_validos}
        for member in guild.members:
            if member.bot:
                continue
            for cargo in member.roles:
                if cargo.id in contagem:
                    contagem[cargo.id] += 1

        menor_contagem = min(contagem.values())
        menos_representados = [
            cargo for cargo in cargos_validos if contagem[cargo.id] == menor_contagem
        ]
        return random.choice(menos_representados)

    @staticmethod
    async def atribuir_cargo(member: discord.Member):
        """Atribui um cargo automaticamente a novos membros, priorizando o menos representado da população."""
        id_guild = str(member.guild.id)
        cargos_ids = Manipular_Cargo.obter_Cargo(id_guild)
        print(f"Verificando cargos para o guild_id: {id_guild}")
        # Verifica se o membro já possui algum dos cargos
        cargos_do_membro = [
            cargo for cargo in member.roles if cargo.id in map(int, cargos_ids)
        ]
        if cargos_do_membro:
            print(f"{member.name} já tem um dos cargos, ignorando atribuição.")
            return  # Ignora se o membro já tem um dos cargos
        # Escolhe o cargo menos representado para manter o balanceamento
        cargo = Manipular_Cargo.obter_cargo_balanceado(member.guild)
        if cargo and cargo not in member.roles:
            await member.add_roles(cargo)
            print(f"Cargo {cargo.name} atribuído a {member.name}.")
