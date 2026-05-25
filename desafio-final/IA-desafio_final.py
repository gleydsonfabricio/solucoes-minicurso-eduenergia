import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração visual dos gráficos
sns.set_theme(style="whitegrid")

# ==========================================
# 4.1. Carregamento e Limpeza dos Dados
# ==========================================
print("--- 4.1 Carregamento e Limpeza ---")
# Importando os dados
df = pd.read_csv('dados.csv')

# Tratando valores ausentes (removendo linhas com dados faltantes para garantir precisão)
df = df.dropna()

# Convertendo a coluna hora para datetime
df['Data_hora'] = pd.to_datetime(df['Data_hora'])

# Convertendo colunas numéricas para float (garantia de tipo)
colunas_numericas = ['Potencia_ativa', 'Potencia_reativa', 'Fator_potencia', 
                     'Corrente_fase_a', 'Corrente_fase_b', 'Corrente_fase_c']
for col in colunas_numericas:
    df[col] = df[col].astype(float)

print("Dados carregados e limpos com sucesso!\n")

# ==========================================
# 4.2. Análise Exploratória Básica
# ==========================================
print("--- 4.2 Estatísticas Descritivas ---")
# Calculando média, mediana e desvio padrão para variáveis numéricas
estatisticas = df[colunas_numericas].agg(['mean', 'median', 'std']).T
print(estatisticas)

print("\n--- Consumo Médio por Bloco ---")
consumo_por_bloco = df.groupby('Medidor')['Potencia_ativa'].mean().sort_values(ascending=False)
print(consumo_por_bloco)

# ==========================================
# 4.3. Identificação de Padrões Temporais
# ==========================================
# Gráfico 1: Variação da potência para um bloco específico (Ex: o bloco com maior consumo)
bloco_alvo = consumo_por_bloco.index[0]
df_bloco = df[df['Medidor'] == bloco_alvo].sort_values('Data_hora')

plt.figure(figsize=(14, 5))
plt.plot(df_bloco['Data_hora'], df_bloco['Potencia_ativa'], color='teal')
plt.title(f'4.3 - Variação da Potência Ativa ao Longo do Tempo ({bloco_alvo})')
plt.xlabel('Data e Hora')
plt.ylabel('Potência Ativa (kW)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Gráfico 2: Horários de pico (agrupando por hora do dia)
df['Hora_do_dia'] = df['Data_hora'].dt.hour
pico_diario = df.groupby('Hora_do_dia')['Potencia_ativa'].mean()

plt.figure(figsize=(10, 5))
sns.barplot(x=pico_diario.index, y=pico_diario.values, palette='magma')
plt.title('4.3 - Consumo Médio por Hora do Dia (Identificação de Picos)')
plt.xlabel('Hora do Dia (0-23h)')
plt.ylabel('Potência Ativa Média (kW)')
plt.show()

# ==========================================
# 4.4. Análise de Fator de Potência
# ==========================================
plt.figure(figsize=(10, 5))
sns.histplot(data=df, x='Fator_potencia', hue='Medidor', bins=30, kde=True, palette='tab10')
plt.axvline(x=0.92, color='red', linestyle='--', label='Limite de Eficiência (0.92)')
plt.title('4.4 - Distribuição do Fator de Potência por Bloco')
plt.xlabel('Fator de Potência')
plt.ylabel('Frequência')
plt.legend()
plt.show()

# Identificando blocos ineficientes (Média abaixo de 0.92)
fp_medio_bloco = df.groupby('Medidor')['Fator_potencia'].mean()
blocos_ineficientes = fp_medio_bloco[fp_medio_bloco < 0.92]

# ==========================================
# 4.5. Correlação entre Variáveis (Dispersão)
# ==========================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fases = ['Corrente_fase_a', 'Corrente_fase_b', 'Corrente_fase_c']
cores = ['blue', 'green', 'orange']

for i, fase in enumerate(fases):
    sns.scatterplot(data=df, x=fase, y='Potencia_ativa', ax=axes[i], color=cores[i], alpha=0.5)
    axes[i].set_title(f'Potência Ativa vs {fase}')
    axes[i].set_xlabel(f'Corrente (A) - Fase {["A", "B", "C"][i]}')
    axes[i].set_ylabel('Potência Ativa (kW)')

plt.tight_layout()
plt.show()

# ==========================================
# 4.6. Relatório Final (Síntese)
# ==========================================
print("\n" + "="*50)
print("RELATÓRIO FINAL DE CONSUMO - SMARTCAMPUS UFCG")
print("="*50)

# 1. Qual bloco tem o maior consumo médio?
print(f"-> Maior Consumo Médio:")
print(f"   O bloco com o maior consumo médio de energia é o '{consumo_por_bloco.index[0]}', "
      f"com uma média de {consumo_por_bloco.iloc[0]:.2f} kW.\n")

# 2. Em quais horários ocorrem picos de demanda?
horario_pico = pico_diario.idxmax()
print(f"-> Picos de Demanda Temporais:")
print(f"   A análise diária indica que o horário de maior pico de consumo ocorre às {horario_pico}h, "
      f"sugerindo os momentos de maior ocupação dos blocos.\n")

# 3. Há blocos com fator de potência preocupante?
print(f"-> Eficiência Energética (Fator de Potência < 0.92):")
if not blocos_ineficientes.empty:
    print("   ATENÇÃO: Os seguintes blocos apresentam fator de potência médio abaixo do ideal (0.92), "
          "indicando desperdício e potencial incidência de multas tarifárias:")
    for bloco, fp in blocos_ineficientes.items():
        print(f"   - {bloco}: {fp:.3f}")
else:
    print("   Excelente! Nenhum bloco apresentou fator de potência médio abaixo de 0.92. O sistema é eficiente.")
print("="*50)