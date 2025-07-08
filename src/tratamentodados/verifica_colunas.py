import pandas as pd
import glob
import os

# Caminho para os dados
DADOS_DIR = os.path.join(os.path.dirname(__file__), '../dados')
csvs = glob.glob(os.path.join(DADOS_DIR, '*.csv'))

# Verifica as colunas do primeiro arquivo
if csvs:
    try:
        df = pd.read_csv(csvs[0], sep=';', dtype=str, encoding='latin1', low_memory=False)
        print("Colunas encontradas no primeiro arquivo:")
        for i, col in enumerate(df.columns):
            print(f"  {i+1}. '{col}'")
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
else:
    print("Nenhum arquivo CSV encontrado.") 