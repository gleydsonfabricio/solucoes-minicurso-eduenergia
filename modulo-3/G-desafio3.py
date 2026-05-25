import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('desafio3.csv', sep=';')

print(df.columns)


# q1
print(df.dtypes)

print("Variaveis Qualitativas:")
print(df.select_dtypes(include=['object']).columns)
#nominal: medidor
#ordinal: data_hora

print("Variaveis Quantitativas:")
print(df.select_dtypes(include=['float64']).columns)
#continuas: todas


# q2
''' teria apenas uma barra, visto que na tabela é fornecido dados apenas de um medidor, 
 dessa forma, a frequencia absoluta seria a quantidade de dados, e freq relativa seria 100%
'''


# q3
consumos = df['Consumo'].tolist()

def categoria_consumo(consumo):
    if consumo < 16600: return 'baixo'
    elif consumo > 16800: return 'alto'
    return 'medio' 


#deve ter uma forma mais idiomatica com pandas
faixa_consumo = [categoria_consumo(c) for c in consumos]
df["Grupo_consumo"] = faixa_consumo
print(df["Grupo_consumo"].value_counts())



# q4
'''
sns.lineplot(data=df, x='Data_hora', y='Consumo', marker='o', linestyle='--')
plt.title("Evolução consumo")
plt.xlabel("Data_Hora")
plt.ylabel("Consumo (KWh)")
plt.grid()
plt.show()
'''


#q5
sns.regplot(data=df, x="Corrente", y="Consumo")
plt.show()

#com os poucos dados, é possivel identificar uma correlação positiva