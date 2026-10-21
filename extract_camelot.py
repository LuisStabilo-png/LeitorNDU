import camelot
import pandas as pd # Essencial para manipular os dados após a extração

arquivo_pdf = "Boletim1415Março.pdf"

paginas_alvo = range(141,146)

lista_de_dataframes = []

#loop que vai rodar uma vez por pagina
for pagina in paginas_alvo:
    print(f"lendo página {pagina}")

    try:
        # A sua configuração original de extração está ótima
        tabelas = camelot.read_pdf(
            arquivo_pdf, 
            pages=str(pagina), 
            flavor="stream", 
            split_text=False, 
            strip_text="\n", 
            edge_tol=50
        )

        # MELHORIA 1: Verificar quantas tabelas foram encontradas antes de tentar acessar uma
        print(f"Total de tabelas encontradas na página 141: {tabelas.n}")

        if tabelas.n > 0:
            # MELHORIA 2: Proteção de índice. 
            # Tenta pegar a 3ª tabela (índice 2), mas se achar menos, pega a última disponível.
            indice = 2 if tabelas.n >= 3 else tabelas.n - 1 
            
            tabela_alvo = tabelas[indice]
            
            # Passando para o formato DataFrame do Pandas
            df = tabela_alvo.df
            
            # MELHORIA 4: Limpeza rápida com Pandas
            # No Camelot 'stream', é comum a primeira linha virar o dado e as colunas ficarem como 0, 1, 2...
            # O bloco abaixo (comentado) é um truque clássico para arrumar isso caso aconteça:
            
            df.columns = df.iloc[0] # Define a primeira linha como cabeçalho
            df = df[1:].reset_index(drop=True) # Remove a primeira linha repetida e reseta o índice
            df = df.replace(r'(?i)parciais\s*?:?', '', regex = True) # O r'(?i)' faz o código ignorar se está escrito com maiúscula ou minúscula.
            
            lista_de_dataframes.append(df)
            print(f" -> Sucesso! Tabela da página {pagina} extraída.")
        else:
            print(f" -> Aviso: Nenhuma tabela encontrada na página {pagina}.")
            
    except Exception as erro:
        print(f" -> Erro crítico na página {pagina}: {erro}")

    if lista_de_dataframes:      

        df_final = pd.concat(lista_de_dataframes, ignore_index=True)

        # MELHORIA 5: Exportação pronta para organização
        nome_arquivo_saida = "tabelaNDU.xlsx"
        df_final.to_excel(nome_arquivo_saida, index=False)            
        print(f"\nSucesso! Dados salvos em '{nome_arquivo_saida}'.")

    else:
        print("O Camelot não conseguiu detectar nenhuma tabela com os parâmetros atuais.")