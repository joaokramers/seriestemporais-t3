import os
import glob
import pandas as pd

# Caminhos
DADOS_DIR = os.path.join(os.path.dirname(__file__), '../dados')
SAIDA = os.path.join(DADOS_DIR, 'fonte-dados-estudo.csv')

# Critérios de filtro
FILTRO_PRACA = 'SAPUCAIA'
FILTRO_TIPO = 'Passeio'
FILTRO_SENTIDO = 'Crescente'
FILTRO_CATEGORIA = 'Categoria 1'

# Lista todos os CSVs
csvs = glob.glob(os.path.join(DADOS_DIR, '*.csv'))

# Lista para armazenar DataFrames filtrados
dfs = []

for csvfile in csvs:
    try:
        df = pd.read_csv(csvfile, sep=';', dtype=str, encoding='utf-8', low_memory=False)
    except Exception:
        # Tenta com encoding diferente se falhar
        df = pd.read_csv(csvfile, sep=';', dtype=str, encoding='latin1', low_memory=False)
    
    # Normaliza nomes de colunas
    df.columns = [c.strip().lower() for c in df.columns]
    
    # Verifica se todas as colunas necessárias existem
    colunas_necessarias = ['tipo_de_veiculo', 'praca', 'sentido']
    if not all(col in df.columns for col in colunas_necessarias):
        print(f"Arquivo {os.path.basename(csvfile)} não tem todas as colunas necessárias. Pulando...")
        continue
    
    # Determina qual coluna de categoria usar e como filtrar
    coluna_categoria = None
    valores_categoria = None
    
    if 'categoria' in df.columns:
        coluna_categoria = 'categoria'
        valores_categoria = [FILTRO_CATEGORIA.lower()]
    elif 'categoria_eixo' in df.columns:
        coluna_categoria = 'categoria_eixo'
        # Para categoria_eixo, filtra categorias 2, 3 e 4 (equivalentes à Categoria 1)
        valores_categoria = ["2", "3", "4"]
    else:
        print(f"Arquivo {os.path.basename(csvfile)} não tem coluna de categoria. Pulando...")
        continue
    
    # Filtra linhas
    mask = df['tipo_de_veiculo'].str.strip().str.lower() == FILTRO_TIPO.lower()
    mask &= df['praca'].str.strip().str.upper() == FILTRO_PRACA.upper()
    mask &= df['sentido'].str.strip().str.lower() == FILTRO_SENTIDO.lower()
    mask &= df[coluna_categoria].str.strip().str.lower().isin(valores_categoria)
    
    filtrado = df[mask]
    if not filtrado.empty:
        dfs.append(filtrado)
        print(f"Encontrados {len(filtrado)} registros em {os.path.basename(csvfile)} (usando coluna: {coluna_categoria}, valores: {valores_categoria})")

# Concatena e salva
if dfs:
    resultado = pd.concat(dfs, ignore_index=True)
    resultado.to_csv(SAIDA, sep=';', index=False, encoding='utf-8')
    print(f'\nArquivo salvo em: {SAIDA}')
    print(f'Total de registros encontrados: {len(resultado)}')
    print(f'Filtros aplicados:')
    print(f'  - Praça: {FILTRO_PRACA}')
    print(f'  - Tipo de veículo: {FILTRO_TIPO}')
    print(f'  - Sentido: {FILTRO_SENTIDO}')
    print(f'  - Categoria: {FILTRO_CATEGORIA} (ou categorias 2,3,4 para 2024)')
else:
    print('Nenhum dado encontrado para os filtros especificados.') 