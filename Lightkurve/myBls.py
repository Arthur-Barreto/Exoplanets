import numpy as np

def normaliza(vetor):
    # calculando o desvio padrão
    dp = np.std(vetor)
    # calculando a média
    media = np.mean(vetor)
    # normalizando
    for i in range(len(vetor)):
        vetor[i] = (vetor[i] - media)/dp
    return vetor

def deltaY(vetor):
    lis = []
    for i in range(len(vetor)-2):
        yi = vetor[i]
        yj = vetor[i+1]
        delta = yj - yi
        lis.append(delta)
    return lis

def linearRegressionCoeficient(dataX,dataY):
    mediaX = np.mean(dataX)
    mediaY = np.mean(dataY)
    SSxx = np.sum(np.fromiter(((mediaX-x)**2 for x in  dataX),dtype=float))
    SSxy = np.sum(np.fromiter(((mediaX-x)*(mediaY-y) for x,y in zip(dataX,dataY)),dtype=float))
    return SSxy/SSxx

# função que calcula o BLS, dado o tempo e o fluxo
def bls(time,fluxo,error):
    # time é o eixo x
    # fluxo é o eixo y
    # na lisPeiod vamos guardar os possiveis periodos, no final retornar o maior valor
    lisPeriod = []
    # time e fluxo devem ter o mesmo tamanho
    if len(time) != len(fluxo):
        print("Erro: time e fluxo devem ter o mesmo tamanho")
        return -1
    # vamos verificar se a curva está normalizada, se não iremos normalizar
    if np.mean(fluxo) != 0 or np.std(fluxo) != 1:
        fluxo = normaliza(fluxo)
    # agora vamos iterar sobre a lista fluxo, calcular a reg linear
    # caso modulo do coeficiente suba muito, temos uma região de transito

    oldCoef = None
    coef = None
    start = 0

    for i in range(1,len(fluxo)):
        smallList = fluxo[:i]
        coef = linearRegressionCoeficient(time[:i],smallList)
        # ao calcular o coef da regresão linear, saberemos o comportamento da curva
        # se ela inclinar muito, temos uma região de transito

        # vamos testar para modulo maior que 0.5
        if abs(coef) > 0.5:
            oldCoef = coef
            start = i

        # se a diferença entre o coefiente antigo e o novo for maior que o erro permitido
        # temos o fim do transito, e o indice atual é o novo start 
        if abs(oldCoef-coef) > error:
            # temos o indicativo do fim do transito, no caso será o i-1
            end = i-1
            periodo = time[end] - time[start]
            lisPeriod.append(periodo)
            start = i

    return np.max(lisPeriod)