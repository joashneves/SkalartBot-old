from models.db import _Sessao, Personagem
from sqlalchemy import func

class Manipular_Personagem:
    def obter_todos_personages(id_discord, guild_id):
        with _Sessao() as sessao:
            personagens = sessao.query(Personagem).filter_by(id_discord=id_discord, guild_id=guild_id).all()
            return personagens

    def Obter_um_personagem(guild_id, nome_personagem, franquia_personagem):
        with _Sessao() as sessao:
            personagem = sessao.query(Personagem).filter_by(guild_id=guild_id, nome_personagem=nome_personagem, franquia_personagem=franquia_personagem).first()
            return personagem

    def obter_todos_personagens_descoberto_servidor(guild_id):
        with _Sessao() as sessao:
            personagens = sessao.query(Personagem).filter_by(guild_id=guild_id).all()
            return personagens

    def obter_todos_personagens_descoberto_usuario(id_discord, guild_id):
        print()
        with _Sessao() as sessao:
            personagens = sessao.query(Personagem).filter_by(id_discord=id_discord, guild_id=guild_id).all()
            return personagens

    def salvar_personagem(id_discord,
                          guild_id,
                          channel_id,
                          id_personagem,
                          nome_personagem,
                          genero_personagem,
                          franquia_personagem,
                          caminho_arquivo_personagem,
                          data_de_descoberta
                    ):
        with _Sessao() as sessao:
            novo_personagem = Personagem(id_discord=id_discord,
                                         guild_id=guild_id,
                                         channel_id=channel_id,
                                         id_personagem=id_personagem,
                                         nome_personagem=nome_personagem,
                                         genero_personagem=genero_personagem,
                                         franquia_personagem=franquia_personagem,
                                         caminho_arquivo_personagem=caminho_arquivo_personagem,
                                         data_de_descoberta=data_de_descoberta)
            sessao.add(novo_personagem)
            sessao.commit()

    def Obter_um_personagem(guild_id, nome_personagem, franquia_personagem):
        with _Sessao() as sessao:
            personagem = sessao.query(Personagem).filter(
                Personagem.guild_id == guild_id,
                func.lower(Personagem.nome_personagem) == nome_personagem.lower(),
                func.lower(Personagem.franquia_personagem) == franquia_personagem.lower()
            ).first()
            return personagem

    def alterar_dono_personage(id_novo_discord,
                               id_discord,
                                guild_id,
                                id_personagem,
                                nome_personagem,
                                franquia_personagem):
        with _Sessao() as sessao:
            personagem_alterado = sessao.query(Personagem).filter_by(id_discord=id_discord,
                                                                    guild_id=guild_id,
                                                                    id_personagem=id_personagem,
                                                                    nome_personagem=nome_personagem,
                                                                    franquia_personagem=franquia_personagem
                                                                    ).first()
            print(f"VAR : {nome_personagem}, {franquia_personagem},{id_personagem}, {id_discord}, {guild_id}, {id_novo_discord},{personagem_alterado}")
            if personagem_alterado:
                print(f"AÇÃO: Personagem encontrado")
                personagem_alterado.id_discord = id_novo_discord
                sessao.commit()

    def alterar_descricao_personage(id_discord, guild_id, nome_personagem, franquia_personagem, descricao_personagem):
        with _Sessao() as sessao:
            personagem_alterado = sessao.query(Personagem).filter_by(id_discord=id_discord,
                                                                     guild_id=guild_id,
                                                                     nome_personagem=nome_personagem,
                                                                     franquia_personagem=franquia_personagem).first()
            personagem_alterado.descricao_personagem = descricao_personagem
            sessao.commit()


    def deletar_personagem(id_discord,
                          guild_id,
                          channel_id,
                          id_personagem,
                          nome_personagem,
                          descricao_personagem,
                          genero_personagem,
                          franquia_personagem,
                          caminho_arquivo_personagem,
                          data_de_descoberta
                    ):
        with _Sessao() as sessao:
            personagem = sessao.query(Personagem).filter_by(id_discord=id_discord,
                                         guild_id=guild_id,
                                         channel_id=channel_id,
                                         id_personagem=id_personagem,
                                         nome_personagem=nome_personagem,
                                         descricao_personagem=descricao_personagem,
                                         genero_personagem=genero_personagem,
                                         franquia_personagem=franquia_personagem,
                                         caminho_arquivo_personagem=caminho_arquivo_personagem,
                                         data_de_descoberta=data_de_descoberta).first()
            sessao.delete(personagem)
            sessao.commit()
