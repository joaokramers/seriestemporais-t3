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

# Lista todos os CSVs (exceto 2024)
csvs = glob.glob(os.path.join(DADOS_DIR, '*.csv'))
# Remove o arquivo de 2024 da lista
csvs = [csv for csv in csvs if '2024' not in csv]

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
    colunas_necessarias = ['tipo_de_veiculo', 'praca', 'sentido', 'categoria']
    if not all(col in df.columns for col in colunas_necessarias):
        print(f"Arquivo {os.path.basename(csvfile)} não tem todas as colunas necessárias. Pulando...")
        continue
    
    # Filtra linhas
    mask = df['tipo_de_veiculo'].str.strip().str.lower() == FILTRO_TIPO.lower()
    mask &= df['praca'].str.strip().str.upper() == FILTRO_PRACA.upper()
    mask &= df['sentido'].str.strip().str.lower() == FILTRO_SENTIDO.lower()
    mask &= df['categoria'].str.strip().str.lower() == FILTRO_CATEGORIA.lower()
    
    filtrado = df[mask]
    if not filtrado.empty:
        dfs.append(filtrado)
        print(f"Encontrados {len(filtrado)} registros em {os.path.basename(csvfile)}")

# Concatena e salva
if dfs:
    resultado = pd.concat(dfs, ignore_index=True)
    # Remove a coluna 'categoria_eixo' se existir
    if 'categoria_eixo' in resultado.columns:
        resultado = resultado.drop(columns=['categoria_eixo'])
    resultado.to_csv(SAIDA, sep=';', index=False, encoding='latin1')
    print(f'\nArquivo salvo em: {SAIDA}')
    print(f'Total de registros encontrados: {len(resultado)}')
    print(f'Filtros aplicados:')
    print(f'  - Praça: {FILTRO_PRACA}')
    print(f'  - Tipo de veículo: {FILTRO_TIPO}')
    print(f'  - Sentido: {FILTRO_SENTIDO}')
    print(f'  - Categoria: {FILTRO_CATEGORIA}')
    print(f'  - Período: até 2023 (excluindo 2024)')
else:
    print('Nenhum dado encontrado para os filtros especificados.') 