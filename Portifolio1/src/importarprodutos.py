import pandas as pd
from sqlalchemy import create_engine, text
import os
from datetime import datetime

#configuracoes
EXCEL_FILE = "data/produtos.xlsx"
DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_NAME = "loja_customizacao"

# funcao para conectar no banco sql
def conectar_banco():
    try:
        connection_string = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
        engine = create_engine(connection_string)
        print("Conexao com sql estabelecida!")
        return engine
    except Exception as e:
        print(f"Erro ao conectar ao banco:{e}")
        return None
    
# funcao para ler o excel
def ler_excel():
    try:
        if not os.path.exists(EXCEL_FILE):
            print(f"Arquivo nao encontrado:{EXCEL_FILE}")
            return None
        df = pd.read_excel(EXCEL_FILE)
        print(f"{len(df)} Produtos lidos do excel")
        return df
    except Exception as e:
        print(f"Erro ao ler excel {e}")
        return None
    
#funcao para limpar e validar dados
def validar_dados(df):
    try:
        #remove linhas completamente vazias
        df = df.dropna(how='all')
        #remove duplicados
        tamanho_antes = len(df)
        df = df.drop_duplicates()
        duplicados_removidos = tamanho_antes - len(df)

        if duplicados_removidos > 0:
            print(f"{duplicados_removidos} Duplicados removidos do Excel")
        
        #garantir tipos corretos
        df["preco"] = df["preco"].astype(float)
        df["estoque"] = df["estoque"].astype(int)

        print("Dados validados com sucesso")
        return df
    except Exception as e:
        print(f"Erro na validacao:{e}")
        return None

#funcao para sincronizar o banco
def sincronizar_dados(df, engine):
    try:
        #ler o que ja existe no banco
        querry = "SELECT * FROM produtos"
        df_banco = pd.read_sql(querry, engine)
        print(f"{len(df_banco)} produtos ja existem no banco")

        #separa novos produtos e produtos para atualizar podendo usar 'id', 'nome' ou 'codigo' se for o caso
        produtos_novos = df[~df['nome'].isin(df_banco['nome'])]
        produtos_atualizar = df[df['nome'].isin(df_banco['nome'])]

        #insere novos produtos
        if len(produtos_novos) > 0:
            produtos_novos.to_sql(
                name="produtos",
                con=engine,
                if_exists="append",
                index=False
            )
            print(f"{len(produtos_novos)} produtos novos adicionados!")
        else:
            print("Nenhum produto novo para adicionar")
        
        #atualizar produtos existentes
        if len(produtos_atualizar) > 0:
            with engine.connect() as connection:
                for _, produto in produtos_atualizar.iterrows():
                    update_querry = text("""
                        UPDATE produtos
                        SET preco = :preco, estoque = :estoque
                        WHERE nome = :nome
                    """)
                    connection.execute(
                        update_querry,
                        {
                            "preco": produto['preco'],
                            "estoque": produto['estoque'],
                            "nome": produto['nome']
                        }
                    )
                connection.commit()
            print(f"{len(produtos_atualizar)} produtos ATUALIZADOS!")
        else:
            print("Nenhum produto para atualizar")
        return True
    except Exception as e:
        print(f"Erro na sincronizacao:{e}")
        return False
    
#funcao principal
def main():
    print("\n" + "="*50)
    print(f" INICIANDO SINCRONIZAÇÃO - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*50 + "\n")

    #conectar no banco
    engine = conectar_banco()
    if not engine:
        return
    
    #ler o excel
    df = ler_excel()
    if df is None:
        return
    
    #validar dados
    df = validar_dados(df)
    if df is None:
        return
    
    #sincronizar com banco
    sucesso = sincronizar_dados(df, engine)
    if sucesso:
        print("\n" + "="*30)
        print("SINCRONIZAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*30 + "\n")
    else:
        print("\n X Sincronização falhou. Verifique os erros acima.\n")
    
#executa o programa
if __name__ == "__main__":
    main()