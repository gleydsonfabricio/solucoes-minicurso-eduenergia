import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 


df = pd.read_csv("dados.csv", sep=";", decimal=",")
df['Medidor'] = df['Medidor'].str.split("Medidor").str[-1]
df['Medidor'] = df['Medidor'].str.split("Med").str[-1]
df["Data_hora"] = pd.to_datetime( df["Data_hora"], format="%d/%m/%Y, %H:%M:%S")

#media = np.mean(df['Potencia_ativa'])
'''
#q03 
print("Media: ", np.mean(df['Potencia_ativa']))
print("Mediana: ", np.median(df['Potencia_ativa']))
print("Moda: ", df['Potencia_ativa'].mode()[0]) #moda é 0, existem 

print(df.loc[df['Potencia_ativa'] == 0.0, ['Medidor', 'Data_hora', 'Potencia_ativa']])

amplitude_total = df['Potencia_ativa'].max() - df['Potencia_ativa'].min() 
print("Amplitude: ", amplitude_total)

desvio_padrao = df['Potencia_ativa'].std()
print("Desvio Padrão: ", desvio_padrao)

coeficiente_variacao = desvio_padrao / media * 100
print("Coeficiente De Variação: ", coeficiente_variacao)

arr = df["Potencia_ativa"].to_numpy()

dif = arr - 17017
print(sorted(dif[(dif > 0)])[:5])

q1 = np.percentile(df['Potencia_ativa'], 25)
q3 = np.percentile(df['Potencia_ativa'], 75)

iqr = q3 - q1 

lim_inf = q1 - 1.5 * iqr 
lim_sup = q3 - 1.5 * iqr

atipico = 17017 > lim_sup or 17017 < lim_inf

print("Atipico" if atipico else "Tipico")
'''



#q04
'''
print(df.columns)
blocos = df["Medidor"].unique()

for bloco in blocos:
    print("=" * 20)
    print(f"Tendencia Central - {bloco}")
    consumos = df.loc[df["Medidor"] == bloco, "Potencia_ativa"]
    print("Media: ", consumos.mean())
    print("Mediana: ", consumos.median())
    print("Moda: ", consumos.round().mode()[0])

    print("Amplitude total: ", consumos.max() - consumos.min())
    print("Desvio Padrão: ", consumos.std())
    cv = (consumos.std() / consumos.mean()) * 100
    print("Coeficiente de variação: ", cv)

    print("Quartil 1: ", np.percentile(consumos, 25))
    print("Quartil 3: ", np.percentile(consumos, 75))
'''

'''
sns.regplot(x='Potencia_ativa', y='Corrente_fase_a', data=df)
plt.show()
'''

bloco = "SPLAB"
dados_bloco = df[df["Medidor"] == bloco].sort_values("Data_hora")
sns.lineplot(x='Data_hora', y='Potencia_ativa', data=dados_bloco)
plt.title(bloco)
plt.show()