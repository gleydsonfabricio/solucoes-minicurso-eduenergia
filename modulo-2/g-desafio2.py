import csv
from typing import NamedTuple


# Formato dos dados
# ['Medidor', 'Data_hora', 'Potencia_ativa', 'Potencia_reativa', 'Fator_potencia', 'Corrente_fase_a', 'Corrente_fase_b', 'Corrente_fase_c']

def get_data(data_hora):
    return data_hora.split(",")[0]

class MesBloco(NamedTuple):
    bloco: str
    mes: int 
    ano: int 

with open('dados.csv', mode='r', encoding='utf-8') as ficheiro:
    leitor = csv.DictReader(ficheiro, delimiter=";")

    # blocos: {'MedSPLAB', 'MedLAT', 'MedPop', 'MedCentralDeLabs', 'MedReitoria', 'MedCEEI', 'MedidorLSD'}

    # MesBloco: Consumo em Watts
    consumo_bloco_mes = dict()
    for linha in leitor:
        bloco = linha['Medidor'].split("Med")[-1]
        data_hora = linha['Data_hora']
        data = get_data(data_hora).split("/")
        mes = data[1]
        ano = data[2]

        consumo = float(linha['Potencia_ativa'].replace(',', '.')) # Em Watts

        mes_bloco = MesBloco(bloco, mes, ano)
        consumo_bloco_mes[mes_bloco] = consumo_bloco_mes.get(mes_bloco, 0) + consumo
    
    
    bloco = "CEEI"
    taxa = 0.8
    print("BLOCO", bloco)
    print("Data:\t CustoMensal")
    print("=" * 20)
    for data, watts in consumo_bloco_mes.items():
        if data.bloco == bloco:
            kWh = watts / 1000
            custo_mensal = kWh * taxa
            print(f"{data.mes}/{data.ano}: {custo_mensal:.2f}")

    maior_consumo = max(consumo_bloco_mes, key=consumo_bloco_mes.get)
    print(maior_consumo)
    print(consumo_bloco_mes[maior_consumo] / 1000)
    


