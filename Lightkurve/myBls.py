import numpy as np

def normaliza(vetor):
    dp = np.std(vetor)
    media = np.mean(vetor)
    for i in range(len(vetor)):
        vetor[i] = (vetor[i] - media)/dp
    return vetor

def weight(fluxErr,index):
    soma = np.sum(np.fromiter((fluxErr[i]**(-2) for i in len(fluxErr)), dtype=float))
    return fluxErr[index]**(-2)/soma

# o tempo relativo gasto na fase L é definido por L
# o mesmo pode ser calculado como segue abaixo

def rValue(i1,i2,weight):
    return np.sum(np.fromiter((weight[i] for i in range(i1,i2)), dtype=float))

def sValue(i1,i2,weight,fluxo):
    return np.sum(np.fromiter((weight[i]*fluxo[i] for i in range(i1,i2)), dtype=float))

def DValue(lisWeight,fluxo,r,s):
    soma = np.sum(np.fromiter((lisWeight[i]*fluxo[i]**2 for i in range(len(fluxo))), dtype=float))
    return (soma - (s**2)/(r*(1-r)))

# função que calcula o BLS, dado o tempo e o fluxo
#  x[i] = fluxo
#  y[i] = fluxoErRO

def bls(time,fluxo,fluxoErr):
    # fluxo é o eixo x
    # fluxoErr é o eixo y
    # time e fluxo devem ter o mesmo tamanho
    if len(time) != len(fluxo):
        print("Erro: time e fluxo devem ter o mesmo tamanho")
        return -1
    # vamos verificar se a curva está normalizada, se não iremos normalizar
    if np.mean(fluxo) != 0 or np.std(fluxo) != 1:
        fluxo = normaliza(fluxo)
    # agora vamos iterar sobre a lista fluxo, calcular a reg linear
    # caso modulo do coeficiente suba muito, temos uma região de transito

    lisWeight = []
    menorD = None

    for i1 in range(len(fluxo)):
        wi = weight(fluxoErr,i1)
        lisWeight.append(wi)

        for i2 in range(len(fluxoErr)):
            r = rValue(i1,i2,lisWeight)
            s = sValue(i1,i2,lisWeight,fluxo)
            d = DValue(lisWeight,fluxo,r,s)

            if menorD is None:
                menorD = d
                periodo = time[i2] - time[i1]
            elif d < menorD:
                periodo = time[i2] - time[i1]
            
    return periodo