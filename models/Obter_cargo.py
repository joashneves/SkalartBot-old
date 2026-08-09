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
    async def atribuir_cargo(member: discord.Member):
        """Atribui um único cargo automaticamente a novos membros, caso o membro não tenha nenhum dos cargos."""
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
        # Escolher um cargo aleatório da lista de cargos
        if cargos_ids:
            cargo_id = random.choice(cargos_ids)  # Escolher um cargo aleatoriamente
            cargo = discord.utils.get(member.guild.roles, id=int(cargo_id))
            if cargo and cargo not in member.roles:
                await member.add_roles(cargo)
                print(f"Cargo {cargo.name} atribuído a {member.name}.")
