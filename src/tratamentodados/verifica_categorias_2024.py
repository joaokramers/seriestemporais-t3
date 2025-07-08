import pandas as pd
import os

# Caminho para o arquivo de 2024
arquivo_2024 = os.path.join(os.path.dirname(__file__), '../dados/volume-trafego-praca-pedagio-2024.csv')

print("=== VERIFICANDO CATEGORIAS DO ARQUIVO 2024 ===")

if os.path.exists(arquivo_2024):
    try:
        # Lê o arquivo
        df = pd.read_csv(arquivo_2024, sep=';', dtype=str, encoding='latin1', low_memory=False)
        
        # Normaliza nomes de colunas
        df.columns = [c.strip().lower() for c in df.columns]
        
        # Filtra dados da SAPUCAIA
        mask_sapucaia = df['praca'].str.strip().str.upper() == 'SAPUCAIA'
        df_sapucaia = df[mask_sapucaia]
        
        print(f"Total de registros da SAPUCAIA: {len(df_sapucaia)}")
        
        if len(df_sapucaia) > 0:
            # Verifica categorias únicas
            categorias = df_sapucaia['categoria_eixo'].unique()
            print(f"\nCategorias únicas encontradas: {sorted(categorias)}")
            
            # Verifica tipos de veículo únicos
            tipos_veiculo = df_sapucaia['tipo_de_veiculo'].unique()
            print(f"Tipos de veículo únicos: {sorted(tipos_veiculo)}")
            
            # Verifica sentidos únicos
            sentidos = df_sapucaia['sentido'].unique()
            print(f"Sentidos únicos: {sorted(sentidos)}")
            
            # Mostra alguns exemplos de registros
            print(f"\nPrimeiros 5 registros da SAPUCAIA:")
            print(df_sapucaia[['mes_ano', 'praca', 'tipo_de_veiculo', 'sentido', 'categoria_eixo', 'volume_total']].head())
            
            # Conta registros por categoria
            print(f"\nContagem por categoria:")
            contagem_categoria = df_sapucaia['categoria_eixo'].value_counts()
            for cat, count in contagem_categoria.items():
                print(f"  Categoria {cat}: {count} registros")
                
    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")
        import traceback
        traceback.print_exc()
else:
    print("Arquivo de 2024 não encontrado!") 