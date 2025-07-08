import pandas as pd
import os

# Caminho para o arquivo de 2024
arquivo_2024 = os.path.join(os.path.dirname(__file__), '../dados/volume-trafego-praca-pedagio-2024.csv')

print("=== TESTANDO ARQUIVO 2024 ===")

if os.path.exists(arquivo_2024):
    try:
        # Tenta ler o arquivo
        df = pd.read_csv(arquivo_2024, sep=';', dtype=str, encoding='latin1', low_memory=False)
        print(f"Arquivo lido com sucesso. Linhas: {len(df)}")
        
        # Mostra as colunas
        print(f"Colunas: {list(df.columns)}")
        
        # Normaliza nomes de colunas
        df.columns = [c.strip().lower() for c in df.columns]
        print(f"Colunas normalizadas: {list(df.columns)}")
        
        # Verifica se tem dados da SAPUCAIA
        if 'praca' in df.columns:
            pracas = df['praca'].unique()
            sapucaia = [p for p in pracas if 'SAPUCAIA' in str(p).upper()]
            print(f"Praças com SAPUCAIA: {sapucaia}")
            
            # Filtra dados da SAPUCAIA
            mask_sapucaia = df['praca'].str.strip().str.upper() == 'SAPUCAIA'
            df_sapucaia = df[mask_sapucaia]
            print(f"Dados da SAPUCAIA: {len(df_sapucaia)} registros")
            
            if len(df_sapucaia) > 0:
                # Mostra alguns exemplos
                print("\nPrimeiros registros da SAPUCAIA:")
                print(df_sapucaia[['praca', 'tipo_de_veiculo', 'sentido', 'categoria_eixo']].head())
                
                # Testa os filtros
                mask_passeio = df_sapucaia['tipo_de_veiculo'].str.strip().str.lower() == 'passeio'
                mask_crescente = df_sapucaia['sentido'].str.strip().str.lower() == 'crescente'
                mask_categoria = df_sapucaia['categoria_eixo'].str.strip() == '1'
                
                print(f"\nFiltros aplicados:")
                print(f"  - Passeio: {mask_passeio.sum()} registros")
                print(f"  - Crescente: {mask_crescente.sum()} registros")
                print(f"  - Categoria 1: {mask_categoria.sum()} registros")
                
                # Filtro combinado
                mask_final = mask_passeio & mask_crescente & mask_categoria
                resultado = df_sapucaia[mask_final]
                print(f"  - Resultado final: {len(resultado)} registros")
                
                if len(resultado) > 0:
                    print("\nRegistros encontrados:")
                    print(resultado[['mes_ano', 'praca', 'tipo_de_veiculo', 'sentido', 'categoria_eixo', 'volume_total']].head())
        
    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")
        import traceback
        traceback.print_exc()
else:
    print("Arquivo de 2024 não encontrado!") 