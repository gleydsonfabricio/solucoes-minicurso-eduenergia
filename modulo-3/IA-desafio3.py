import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 2. Dados fornecidos transcritos da tabela do PDF
dados = {
    'Data e hora': ['24/06/2024 00:00', '24/06/2024 01:00', '24/06/2024 02:00', '24/06/2024 03:00', '24/06/2024 04:00'],
    'Medidor': ['LSD', 'LSD', 'LSD', 'LSD', 'LSD'],
    'Tensão (V)': [127.98, 127.70, 127.79, 127.93, 127.93],
    'Corrente (A)': [43.88, 44.04, 44.23, 44.36, 43.91],
    'Consumo (kWh)': [16578.33, 16685.77, 16844.66, 16739.53, 16700.73],
    'Fator de potência': [0.917, 0.921, 0.922, 0.920, 0.922]
}

# Criando o DataFrame
df = pd.DataFrame(dados)

# Configurando o estilo visual dos gráficos
sns.set_theme(style="whitegrid")
plt.figure(figsize=(15, 10))

# ==========================================
# 4.2. Gráfico de variável qualitativa nominal
# ==========================================
plt.subplot(2, 2, 1)
contagem_medidor = df['Medidor'].value_counts()
sns.barplot(x=contagem_medidor.index, y=contagem_medidor.values, palette="Blues_d")
plt.title('4.2 - Registros por Medidor')
plt.xlabel('Medidor')
plt.ylabel('Quantidade de Registros')
plt.yticks(range(0, 7)) # Ajustando o eixo Y para ficar claro que são 5 registros

# ==========================================
# 4.3. Distribuição de frequência do Consumo
# ==========================================
# O pd.cut divide os dados em 3 faixas de tamanhos iguais automaticamente
df['Faixa_Consumo'] = pd.cut(df['Consumo (kWh)'], bins=3, labels=['Baixa', 'Média', 'Alta'])
contagem_faixas = df['Faixa_Consumo'].value_counts().reindex(['Baixa', 'Média', 'Alta'])

plt.subplot(2, 2, 2)
sns.barplot(x=contagem_faixas.index, y=contagem_faixas.values, palette="viridis")
plt.title('4.3 - Frequência de Consumo em Faixas')
plt.xlabel('Faixa de Consumo')
plt.ylabel('Frequência (Qtd de Horas)')

# ==========================================
# 4.4. Série temporal
# ==========================================
# Extraindo apenas o horário para o eixo X ficar mais limpo
df['Hora'] = df['Data e hora'].apply(lambda x: x.split(' ')[1])

plt.subplot(2, 2, 3)
sns.lineplot(data=df, x='Hora', y='Consumo (kWh)', marker='o', color='coral', linewidth=2)
plt.title('4.4 - Evolução do Consumo no Tempo')
plt.xlabel('Horário')
plt.ylabel('Consumo (kWh)')

# ==========================================
# 4.5. Diagrama de dispersão (corrente x consumo)
# ==========================================
plt.subplot(2, 2, 4)
sns.scatterplot(data=df, x='Corrente (A)', y='Consumo (kWh)', s=100, color='purple')
# Adicionando rótulos aos pontos para ver a hora
for i, linha in df.iterrows():
    plt.text(linha['Corrente (A)'] + 0.01, linha['Consumo (kWh)'], linha['Hora'], fontsize=9)
    
plt.title('4.5 - Dispersão: Corrente vs Consumo')
plt.xlabel('Corrente (A)')
plt.ylabel('Consumo (kWh)')

# Ajustando layout e plotando
plt.tight_layout()
plt.show()

# Imprimindo o DataFrame modificado para verificação
print("--- Classificação de Faixas de Consumo ---")
print(df[['Hora', 'Consumo (kWh)', 'Faixa_Consumo']])