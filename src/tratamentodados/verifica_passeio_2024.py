import pandas as pd
import os

# Caminho para o arquivo de 2024
arquivo_2024 = os.path.join(os.path.dirname(__file__), '../dados/volume-trafego-praca-pedagio-2024.csv')

print("=== VERIFICANDO VEÍCULOS DE PASSEIO NO ARQUIVO 2024 ===")

if os.path.exists(arquivo_2024):
    try:
        # Lê o arquivo
        df = pd.read_csv(arquivo_2024, sep=';', dtype=str, encoding='latin1', low_memory=False)
        
        # Normaliza nomes de colunas
        df.columns = [c.strip().lower() for c in df.columns]
        
        # Filtra dados da SAPUCAIA
        mask_sapucaia = df['praca'].str.strip().str.upper() == 'SAPUCAIA'
        df_sapucaia = df[mask_sapucaia]
        
        # Filtra veículos de passeio
        mask_passeio = df_sapucaia['tipo_de_veiculo'].str.strip().str.lower() == 'passeio'
        df_passeio = df_sapucaia[mask_passeio]
        
        print(f"Total de veículos de passeio da SAPUCAIA: {len(df_passeio)}")
        
        if len(df_passeio) > 0:
            # Verifica categorias dos veículos de passeio
            categorias_passeio = df_passeio['categoria_eixo'].unique()
            print(f"Categorias dos veículos de passeio: {sorted(categorias_passeio)}")
            
            # Conta veículos de passeio por categoria
            print(f"\nContagem de veículos de passeio por categoria:")
            contagem_passeio = df_passeio['categoria_eixo'].value_counts()
            for cat, count in contagem_passeio.items():
                print(f"  Categoria {cat}: {count} registros")
            
            # Mostra alguns exemplos
            print(f"\nPrimeiros 5 registros de veículos de passeio:")
            print(df_passeio[['mes_ano', 'praca', 'tipo_de_veiculo', 'sentido', 'categoria_eixo', 'volume_total']].head())
            
            # Verifica sentidos dos veículos de passeio
            sentidos_passeio = df_passeio['sentido'].unique()
            print(f"\nSentidos dos veículos de passeio: {sentidos_passeio}")
            
            # Conta por sentido
            print(f"\nContagem por sentido:")
            contagem_sentido = df_passeio['sentido'].value_counts()
            for sentido, count in contagem_sentido.items():
                print(f"  {sentido}: {count} registros")
                
    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")
        import traceback
        traceback.print_exc()
else:
    print("Arquivo de 2024 não encontrado!") 