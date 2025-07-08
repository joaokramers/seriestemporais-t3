import pandas as pd
import glob
import os

# Caminho para os dados
DADOS_DIR = os.path.join(os.path.dirname(__file__), '../dados')

# Verifica o arquivo de 2024
arquivo_2024 = os.path.join(DADOS_DIR, 'volume-trafego-praca-pedagio-2024.csv')

if os.path.exists(arquivo_2024):
    try:
        df_2024 = pd.read_csv(arquivo_2024, sep=';', dtype=str, encoding='latin1', low_memory=False)
        print("=== ESTRUTURA DO ARQUIVO 2024 ===")
        print("Colunas encontradas:")
        for i, col in enumerate(df_2024.columns):
            print(f"  {i+1}. '{col}'")
        
        print(f"\nTotal de colunas: {len(df_2024.columns)}")
        
        # Verifica se tem dados da SAPUCAIA
        if 'praca' in df_2024.columns:
            pracas_2024 = df_2024['praca'].unique()
            sapucaia_2024 = [p for p in pracas_2024 if 'SAPUCAIA' in str(p).upper()]
            print(f"\nPraças com 'SAPUCAIA' em 2024: {sapucaia_2024}")
        
    except Exception as e:
        print(f"Erro ao ler arquivo 2024: {e}")

# Compara com um arquivo anterior (2010)
arquivo_2010 = os.path.join(DADOS_DIR, 'volume-trafego-praca-pedagio-2010.csv')

if os.path.exists(arquivo_2010):
    try:
        df_2010 = pd.read_csv(arquivo_2010, sep=';', dtype=str, encoding='latin1', low_memory=False)
        print("\n=== ESTRUTURA DO ARQUIVO 2010 ===")
        print("Colunas encontradas:")
        for i, col in enumerate(df_2010.columns):
            print(f"  {i+1}. '{col}'")
        
        print(f"\nTotal de colunas: {len(df_2010.columns)}")
        
        # Verifica se tem dados da SAPUCAIA
        if 'praca' in df_2010.columns:
            pracas_2010 = df_2010['praca'].unique()
            sapucaia_2010 = [p for p in pracas_2010 if 'SAPUCAIA' in str(p).upper()]
            print(f"\nPraças com 'SAPUCAIA' em 2010: {sapucaia_2010}")
            
    except Exception as e:
        print(f"Erro ao ler arquivo 2010: {e}")

# Compara as colunas
if 'df_2024' in locals() and 'df_2010' in locals():
    colunas_2024 = set(df_2024.columns)
    colunas_2010 = set(df_2010.columns)
    
    print("\n=== COMPARAÇÃO DE COLUNAS ===")
    print(f"Colunas apenas em 2024: {colunas_2024 - colunas_2010}")
    print(f"Colunas apenas em 2010: {colunas_2010 - colunas_2024}")
    print(f"Colunas em comum: {len(colunas_2024 & colunas_2010)}") 