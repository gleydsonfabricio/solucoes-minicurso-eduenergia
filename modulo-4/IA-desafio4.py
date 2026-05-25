import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ---------------------------------------------------------
# Preparação dos Dados
# ---------------------------------------------------------
# Carrega os dados (substitua pelo caminho correto, se necessário)
df = pd.read_csv('dados.csv')

# Filtra apenas os blocos SPLAB e LSD
df_blocos = df[df['Medidor'].isin(['SPLAB', 'LSD'])].copy()

# A medição é horária. Para obter a energia em kWh, dividimos a Potência Ativa (W) por 1000
df_blocos['Consumo_kWh'] = df_blocos['Potencia_ativa'] / 1000

# ---------------------------------------------------------
# 4.1 Medidas de Tendência Central
# ---------------------------------------------------------
print("--- 4.1 Medidas de Tendência Central ---")
for bloco in ['SPLAB', 'LSD']:
    dados_bloco = df_blocos[df_blocos['Medidor'] == bloco]['Consumo_kWh']
    media = dados_bloco.mean()
    mediana = dados_bloco.median()
    # Pega o primeiro valor da moda, caso existam múltiplos valores multimodais
    moda = dados_bloco.mode().iloc[0] if not dados_bloco.mode().empty else "Sem moda"
    
    print(f"Bloco {bloco}:")
    print(f"  Média:   {media:.2f} kWh")
    print(f"  Mediana: {mediana:.2f} kWh")
    print(f"  Moda:    {moda:.2f} kWh\n")

# ---------------------------------------------------------
# 4.2 Medidas de Variabilidade
# ---------------------------------------------------------
print("--- 4.2 Medidas de Variabilidade ---")
for bloco in ['SPLAB', 'LSD']:
    dados_bloco = df_blocos[df_blocos['Medidor'] == bloco]['Consumo_kWh']
    amplitude = dados_bloco.max() - dados_bloco.min()
    desvio_padrao = dados_bloco.std()
    cv = (desvio_padrao / dados_bloco.mean()) * 100 # Em percentual
    
    print(f"Bloco {bloco}:")
    print(f"  Amplitude Total:       {amplitude:.2f} kWh")
    print(f"  Desvio Padrão:         {desvio_padrao:.2f} kWh")
    print(f"  Coeficiente de Var.:   {cv:.2f}%\n")

# ---------------------------------------------------------
# 4.3 Medidas de Posição (Bloco LSD e o valor 17017)
# ---------------------------------------------------------
print("--- 4.3 Medidas de Posição (Bloco LSD) ---")
dados_lsd = df_blocos[df_blocos['Medidor'] == 'LSD']['Consumo_kWh']

# Quartis
q1 = dados_lsd.quantile(0.25)
q3 = dados_lsd.quantile(0.75)
iqr = q3 - q1
limite_superior = q3 + 1.5 * iqr

# Escore-z para 17017 kWh
valor_analise = 17017
media_lsd = dados_lsd.mean()
std_lsd = dados_lsd.std()
z_score = (valor_analise - media_lsd) / std_lsd

print(f"Q1 (25º percentil): {q1:.2f} kWh")
print(f"Q3 (75º percentil): {q3:.2f} kWh")
print(f"Escore-Z para {valor_analise} kWh: {z_score:.2f}")

# Determinando se é atípico
# Um Z-score com valor absoluto maior que 3 é classicamente considerado atípico.
if abs(z_score) > 3 or valor_analise > limite_superior:
    print(f"Conclusão: O consumo de {valor_analise} kWh É ATÍPICO (Outlier).")
else:
    print(f"Conclusão: O consumo de {valor_analise} kWh NÃO É ATÍPICO.")

# ---------------------------------------------------------
# 4.4 Construção de Boxplots
# ---------------------------------------------------------
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

sns.boxplot(x='Medidor', y='Consumo_kWh', data=df_blocos, palette="Set2")
plt.title('4.4 - Boxplot Comparativo: SPLAB vs LSD')
plt.ylabel('Consumo (kWh)')
plt.xlabel('Bloco')

# Mostra o gráfico de boxplot
plt.show()

# ---------------------------------------------------------
# 4.5 Análise Gráfica Complementar
# ---------------------------------------------------------
# Utilizando um Violin Plot e um Histograma de densidade
fig, ax = plt.subplots(1, 2, figsize=(16, 6))

# Gráfico 1: Violin Plot (Mostra a distribuição da densidade dos dados junto com os quartis)
sns.violinplot(x='Medidor', y='Consumo_kWh', data=df_blocos, palette="Set2", ax=ax[0])
ax[0].set_title('Distribuição de Densidade (Violin Plot)')
ax[0].set_ylabel('Consumo (kWh)')

# Gráfico 2: Histograma com KDE (Kernel Density Estimate)
sns.histplot(data=df_blocos, x='Consumo_kWh', hue='Medidor', element='step', stat='density', common_norm=False, kde=True, ax=ax[1], palette="Set2")
ax[1].set_title('Histograma de Consumo por Bloco')
ax[1].set_xlabel('Consumo (kWh)')
ax[1].set_ylabel('Densidade')

plt.tight_layout()
plt.show()