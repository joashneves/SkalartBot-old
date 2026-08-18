from models.db import _Sessao, Usuario

class Manipular_Usuario:
    def obter_usuario(id_discord: str):
        with _Sessao() as sessao:
            usuario = sessao.query(Usuario).filter_by(id_discord=id_discord).first()
            if not usuario:
                print(f"Usuário não existe.")
                return
            return usuario

    @staticmethod
    def obter_todos_usuarios():
        with _Sessao() as sessao:
            usuarios = sessao.query(Usuario).all()
            if not usuarios:
                print("Nenhum usuário encontrado.")
                return []
            return usuarios

    def atualizar_usuario(id_discord: int, apelido: str, descricao: str, rede_social:str ,pronome: str = "N/a"):
        with _Sessao() as sessao:
            usuario = sessao.query(Usuario).filter_by(id_discord=id_discord).first()
            if usuario:
                usuario.apelido = apelido
                usuario.descricao = descricao
                usuario.rede_social = rede_social or usuario.rede_social
                usuario.pronome = pronome or usuario.pronome
                sessao.commit()
                print(f"Usuário {id_discord} atualizado com sucesso.")
                return usuario
            return "Usuario não existe"

    def criar_usuario(id_discord: int, apelido: str, descricao: str, rede_social:str ,pronome: str = "N/a"):
        with _Sessao() as sessao:
            usuario = sessao.query(Usuario).filter_by(id_discord=id_discord).first()
            if not usuario:
                usuario = Usuario(
                        id_discord=id_discord,
                        apelido=apelido,
                        rede_social=rede_social,
                        descricao=descricao,
                        pronome=pronome
                )
                sessao.add(usuario)
                print(f"Usuário {id_discord} registrado com sucesso.")
                sessao.commit()
                return usuario
            return "Usuario ja existe"

    @staticmethod
    def adicionar_moedas(id_discord: str, moedas: int):
        with _Sessao() as sessao:
            usuario = sessao.query(Usuario).filter_by(id_discord=id_discord).first()
            if usuario:
                usuario.saldo += moedas
                sessao.commit()
                return usuario
            return None

    @staticmethod
    def adicionar_xp(id_discord: str, experience: int):
        with _Sessao() as sessao:
            usuario = sessao.query(Usuario).filter_by(id_discord=id_discord).first()
            if usuario:
                usuario.xp += experience
                # Verifica se o XP atingiu ou ultrapassou o limite para o próximo nível
                xp_necessario = 100 * ((usuario.level + 1)* 2.5)  # O limite de XP para o próximo nível
                if usuario.xp >= xp_necessario:
                    usuario.level += 1  # Sobe o nível
                    usuario.xp = 0  # Zera o XP
                sessao.commit()
                return usuario
            return None
