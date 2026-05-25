import pandas as pd

# 2. Dados fornecidos [cite: 49]
# Carregando o arquivo .csv com os dados [cite: 51]
# Certifique-se de que o arquivo 'dados.csv' está no mesmo diretório do script
df = pd.read_csv('dados.csv')

# Filtrando o DataFrame para conter apenas os blocos de interesse (CEEI e LAT) 
df_blocos = df[df['Medidor'].isin(['CEEI', 'LAT'])].copy()

# Como a medição é de 1 em 1 hora, a potência (W) x 1h = Wh.
# Dividimos por 1000 para converter a Potência Ativa de Watts (W) para Quilowatts (kWh)
df_blocos['Consumo_kWh'] = df_blocos['Potencia_ativa'] / 1000

# Agrupando por medidor para somar o consumo total (kWh) no período da amostra
consumo_mensal = df_blocos.groupby('Medidor')['Consumo_kWh'].sum()

# Extraindo o consumo de cada bloco
consumo_ceei = consumo_mensal.get('CEEI', 0)
consumo_lat = consumo_mensal.get('LAT', 0)

# 4. Tarefa
# Calculando o custo mensal de operação considerando a tarifa de R$ 0,80/kWh [cite: 55, 56]
tarifa = 0.80
custo_ceei = consumo_ceei * tarifa
custo_lat = consumo_lat * tarifa

# 3. Respostas das Perguntas 

print("--- Respostas do Desafio ---")

# 1. Qual o custo mensal de operação no bloco CEEI? E no LAT? [cite: 53]
print(f"1. Custo mensal de operação:")
print(f"   - Bloco CEEI: R$ {custo_ceei:.2f}")
print(f"   - Bloco LAT: R$ {custo_lat:.2f}\n")

# 2. Qual dos dois blocos tem um custo mais alto? A diferença entre eles é grande? 
if custo_ceei > custo_lat:
    bloco_caro = 'CEEI'
    diferenca = custo_ceei - custo_lat
elif custo_lat > custo_ceei:
    bloco_caro = 'LAT'
    diferenca = custo_lat - custo_ceei
else:
    bloco_caro = 'Nenhum'
    diferenca = 0

print(f"2. Análise de Custo:")
if bloco_caro != 'Nenhum':
    print(f"   - O bloco com o custo mais alto é o {bloco_caro}.")
    print(f"   - A diferença de custo entre o CEEI e o LAT é de R$ {diferenca:.2f}.")
else:
    print("   - Ambos os blocos possuem o mesmo custo de operação.")