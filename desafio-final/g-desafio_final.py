import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def simetria(dados):
    media = np.mean(dados)
    mediana = np.median(dados)

    if media == mediana: return "Simetrica"
    elif media > mediana: return "Assimetrica Positiva"
    else: return "Assimetrica Negativa"


# carregamento e limpeza dos dados
df = pd.read_csv('dados.csv', sep=';', decimal=',')

df["Medidor"] = df["Medidor"].str.replace(r'^(Medidor|Med)', '', regex=True)
df['Data_hora'] = pd.to_datetime(df['Data_hora'], dayfirst=True)

# converter para KW
# df['Potencia_ativa'] = df['Potencia_ativa'] / 1000
df = df.dropna() #remover celulas vazias

'''
df["Data_hora"].dt.year
df["Data_hora"].dt.month
df["Data_hora"].dt.day
'''

df = df[df['Potencia_ativa'] > 0]

# Análise exploratória básica
'''
print("Consumo Médio dos blocos:")
print(df.groupby('Medidor')['Potencia_ativa'].mean().to_string(header=False))

consumos = df['Potencia_ativa']
print("Media:,", consumos.mean())
print("Mediana:", consumos.median())
print("Desvio Padrão:", consumos.std())
print("Simetria:", simetria(consumos))


# Identificação de padrões temporais 

bloco = 'LSD'
dados_bloco = df[df['Medidor'] == bloco]

sns.lineplot(x='Data_hora', y='Potencia_ativa', data=dados_bloco)
plt.axhline(y=dados_bloco['Potencia_ativa'].mean(), color='red')
plt.show()

df['horario'] = df['Data_hora'].dt.hour 

horarios_agrupados = df.groupby('horario')['Potencia_ativa'].mean()


horarios_agrupados.plot(kind='bar')

plt.title("Campus I: Média de consumo por horario")
plt.xlabel("Horários")
plt.ylabel("Consumo (KW)")
plt.xticks(rotation=0)
plt.grid(axis='y')

plt.show()
'''

'''
FP = 'Fator_potencia'
desperdicios = df[df[FP] < 0.92]
# print(set(desperdicios['Medidor'].unique()) == set(df['Medidor'].unique())) # todos os blocos já tiveram disperdicio!

total_medicoes = df.groupby('Medidor')[FP].count()
total_desperdicios = desperdicios.groupby('Medidor')[FP].count()

porcentagem_desperdicio = total_desperdicios * 100 / total_medicoes
'''
'''
grafico = porcentagem_desperdicio.plot(kind='bar')
plt.ylim(0, 100)
plt.title("Índice de Desperdício por Medidor")
plt.xlabel("Blocos")
plt.ylabel("Percentual (%)")
plt.xticks(rotation=45)
plt.grid(axis='y', color='red', linestyle='--', alpha=0.5)

for i, v in enumerate(porcentagem_desperdicio.values):
    grafico.text(i, v, f'{v:.1f}%', ha='center', va='bottom')

plt.show()
'''
'''
#                     lin, col
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.scatterplot(data=df, x='Potencia_ativa', y='Corrente_fase_a', ax=axes[0], color='red')
axes[0].set_title("Relação: Potencia Ativa X Corrente Fase A")

sns.scatterplot(data=df, x='Potencia_ativa', y='Corrente_fase_b', ax=axes[1], color='purple')
axes[1].set_title("Relação: Potencia Ativa X Corrente Fase B")

sns.scatterplot(data=df, x='Potencia_ativa', y='Corrente_fase_c', ax=axes[2])
axes[2].set_title("Relação: Potencia Ativa X Corrente Fase C")

plt.show()
'''

# Relatorio Final

consumos_medio = df.groupby('Medidor')['Potencia_ativa'].mean()
maior_consumidor = consumos_medio.idxmax()
maior_consumo =  consumos_medio.max()

print(f'''===== Maior Consumo Médio =====
Bloco: {maior_consumidor}
Consumo: {maior_consumo:.2f} W''')

print()

df['horario'] = df['Data_hora'].dt.hour 
horarios_agrupados = df.groupby('horario')['Potencia_ativa'].mean()
horario_pico = horarios_agrupados.idxmax()
demanda = horarios_agrupados.max()

print("===== Horário de pico no campus =====")
print(f'Horário com pico de demanda: {horario_pico}h')
print(f'Consumo Médio: {demanda:.2f} W')


print()

desperdicios = df[df['Fator_potencia'] < 0.92]
total_medicoes = df.groupby('Medidor')['Fator_potencia'].count()
total_desperdicios = desperdicios.groupby('Medidor')['Fator_potencia'].count()
porcentagem_desperdicio = total_desperdicios * 100 / total_medicoes

bloco_maior_desperdicio = porcentagem_desperdicio.idxmax()
maior_percentual_desperdicio = porcentagem_desperdicio.max()

print("==== Desperdicio de Energia ====")
print(f'Bloco com maior desperdicio: {bloco_maior_desperdicio}')
print(f'Percentual de Desperdicio: {maior_percentual_desperdicio:.2f}%')





