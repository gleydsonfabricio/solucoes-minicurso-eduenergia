def media(valores: list[int]) -> float:
    return sum(valores) / len(valores)

consumo_kwh = {
    "norte": [120, 150, 90, 110, 130],
    "nordeste": [140, 160, 100, 120, 180],
    "sudeste": [200, 220, 180, 210, 240],
    "sul": [160, 170, 150, 140, 190],
    "centro_oeste": [130, 140, 120, 110, 160]}


print("---- Média por região ----")
for estado, consumos in consumo_kwh.items():
    print(f"{estado}: {media(consumos)}")

todos_os_consumos = []
for consumos in consumo_kwh.values(): 
    todos_os_consumos += consumos

menor_consumo = min(todos_os_consumos)
maior_consumo = max(todos_os_consumos)

print("Menor consumo:", menor_consumo)
print("Maior consumo:", maior_consumo)

consumo_medio = media(todos_os_consumos)
print("consumo medio é acima de 150 kWh/mes?", 
      "Sim" if consumo_medio > 150 else "Não")

# 4.2
def classifica_energia(dados: dict, regiao: str) -> str:
    med = media(dados[regiao])
    if med > 170: return "ALTO"
    elif med < 130: return "BAIXO"
    else: return "MODERADO"


# 4.3
regioes = list(consumo_kwh.keys())
classificao_por_regiao = dict()
for regiao in regioes:
    classificao_por_regiao[regiao] = classifica_energia(consumo_kwh, regiao)

print(classificao_por_regiao)



# 4.4
import matplotlib.pyplot as plt

medias = [media(consumo_kwh[reg]) for reg in regioes]

map_cores = {
    'ALTO':'red',
    'MODERADO': 'yellow',
    'BAIXO': 'green'
}

cores_categorias = [map_cores[classificao_por_regiao[reg]] for reg in regioes]

plt.figure(figsize=(10, 5))
plt.bar(range(len(regioes)), medias, color=cores_categorias)
plt.xticks(range(len(regioes)), regioes)
plt.show()

