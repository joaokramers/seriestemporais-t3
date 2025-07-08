import os
import glob
import pandas as pd

# Caminhos
DADOS_DIR = os.path.join(os.path.dirname(__file__), '../dados')
SAIDA = os.path.join(DADOS_DIR, 'fonte-dados-estudo.csv')

# Critérios de filtro
FILTRO_PRACA = 'BR-393/RJ km 125,00'
FILTRO_TIPO = 'Passeio'

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
    # Filtra linhas
    mask = df['tipo_de_veiculo'].str.strip().str.lower() == FILTRO_TIPO.lower()
    mask &= df['praca'].str.contains(FILTRO_PRACA, case=False, na=False)
    filtrado = df[mask]
    if not filtrado.empty:
        dfs.append(filtrado)

# Concatena e salva
if dfs:
    resultado = pd.concat(dfs, ignore_index=True)
    resultado.to_csv(SAIDA, sep=';', index=False, encoding='utf-8')
    print(f'Arquivo salvo em: {SAIDA}')
else:
    print('Nenhum dado encontrado para os filtros especificados.') 