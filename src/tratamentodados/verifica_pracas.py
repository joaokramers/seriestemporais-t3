import pandas as pd
import glob
import os

# Caminho para os dados
DADOS_DIR = os.path.join(os.path.dirname(__file__), '../dados')
csvs = glob.glob(os.path.join(DADOS_DIR, '*.csv'))

# Set para armazenar todas as praças únicas
todas_pracas = set()

# Processa os primeiros 3 arquivos para verificar
for csvfile in csvs[:3]:
    try:
        df = pd.read_csv(csvfile, sep=';', dtype=str, encoding='latin1', low_memory=False)
        # Normaliza nomes de colunas
        df.columns = [c.strip().lower() for c in df.columns]
        # Adiciona praças únicas
        todas_pracas.update(df['praca'].unique())
    except Exception as e:
        print(f"Erro ao ler {csvfile}: {e}")

# Filtra praças que contêm "393" ou "RJ"
pracas_393_rj = [p for p in todas_pracas if '393' in str(p) or 'RJ' in str(p)]

print("Praças encontradas com '393' ou 'RJ':")
for praca in sorted(pracas_393_rj):
    print(f"  - {praca}")

print(f"\nTotal de praças únicas encontradas: {len(todas_pracas)}")
print(f"Praças com '393' ou 'RJ': {len(pracas_393_rj)}") 