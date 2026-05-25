import numpy as np
import matplotlib.pyplot as plt

# 2. Dados fornecidos no PDF (em kWh/mês)
dados_regioes = {
    'Norte': [120, 150, 90, 110, 130],
    'Nordeste': [140, 160, 100, 120, 180],
    'Sudeste': [200, 220, 180, 210, 240],
    'Sul': [160, 170, 150, 140, 190],
    'Centro-oeste': [130, 140, 120, 110, 160]
}

# 4.1. Cálculo de estatísticas básicas
estatisticas = {}
for regiao, valores in dados_regioes.items():
    media = np.mean(valores)
    maior = np.max(valores)
    menor = np.min(valores)
    acima_150 = media > 150
    
    estatisticas[regiao] = {
        'Média': media,
        'Maior': maior,
        'Menor': menor,
        'Acima de 150': acima_150
    }

# Imprimindo respostas das perguntas 1 e 2
print("--- Estatísticas Básicas ---")
for regiao, stats in estatisticas.items():
    print(f"{regiao}: Média={stats['Média']} | Min={stats['Menor']} | Max={stats['Maior']} | >150={stats['Acima de 150']}")

# Resposta Pergunta 3: Os valores variam muito entre si?
# Analisando o desvio padrão para entender a variação (padrão de consumo)
print("\n--- Variação (Desvio Padrão) ---")
for regiao, valores in dados_regioes.items():
    print(f"{regiao}: {np.std(valores):.2f}")

# 4.2. Função de classificação
def classificar_consumo(media):
    if media >= 170:
        return "ALTO"
    elif 130 <= media < 170:
        return "MODERADO"
    else:
        return "BAIXO"

# 4.3. Aplicação da função a todas as regiões
classificacao_regioes = {regiao: classificar_consumo(stats['Média']) for regiao, stats in estatisticas.items()}

print("\n--- Classificação ---")
print(classificacao_regioes)

# 4.4. Visualização
regioes = list(dados_regioes.keys())
medias = [estatisticas[r]['Média'] for r in regioes]

# Mapeando cores conforme a classificação
mapa_cores = {'ALTO': 'red', 'MODERADO': 'orange', 'BAIXO': 'green'}
cores = [mapa_cores[classificacao_regioes[r]] for r in regioes]

plt.figure(figsize=(10, 6))
bars = plt.bar(regioes, medias, color=cores)

plt.axhline(y=150, color='gray', linestyle='--', label='Linha de 150 kWh')
plt.title('Média de Consumo de Energia por Região')
plt.ylabel('Consumo Médio (kWh/mês)')
plt.xlabel('Região')
plt.legend()

# Adicionando os valores em cima das barras para clareza
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 2, round(yval, 1), ha='center', va='bottom')

plt.show()