import pandas as pd
import glob
import os

# Caminho para os dados
DADOS_DIR = os.path.join(os.path.dirname(__file__), '../dados')
csvs = glob.glob(os.path.join(DADOS_DIR, '*.csv'))

# Set para armazenar todas as praças únicas
todas_pracas = set()

# Processa todos os arquivos
for csvfile in csvs:
    try:
        df = pd.read_csv(csvfile, sep=';', dtype=str, encoding='latin1', low_memory=False)
        # Normaliza nomes de colunas
        df.columns = [c.strip().lower() for c in df.columns]
        # Adiciona praças únicas
        todas_pracas.update(df['praca'].unique())
    except Exception as e:
        print(f"Erro ao ler {csvfile}: {e}")

# Filtra praças que contêm "SAPUCAIA"
pracas_sapucaia = [p for p in todas_pracas if 'SAPUCAIA' in str(p).upper()]

print("Praças encontradas com 'SAPUCAIA':")
for praca in sorted(pracas_sapucaia):
    print(f"  - {praca}")

print(f"\nTotal de praças únicas encontradas: {len(todas_pracas)}")
print(f"Praças com 'SAPUCAIA': {len(pracas_sapucaia)}")

# Se não encontrar "SAPUCAIA", mostra algumas praças para referência
if not pracas_sapucaia:
    print("\nPrimeiras 10 praças encontradas:")
    for praca in sorted(list(todas_pracas))[:10]:
        print(f"  - {praca}") 