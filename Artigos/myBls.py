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

# função que calcula o BLS, dado o tempo e o fluxo
def bls(time,fluxo,delta):
    # time é o eixo x
    # fluxo é o eixo y
    # na lisPeiod vamos guardar os possiveis periodos, no final retornar o maior valor
    lisPeriod = []
    # time e fluxo devem ter o mesmo tamanho
    if len(time) != len(fluxo):
        print("Erro: time e fluxo devem ter o mesmo tamanho")
        return 0
    # vamos verificar se a curva está normalizada, se não iremos normalizar
    if np.mean(fluxo) != 0 or np.std(fluxo) != 1:
        # normalizando
        fluxo = normaliza(fluxo)
    # o periodo é a direferença entre dois pontos consecutivos do vetor time
    # a intenção é calcular todos os periodos e retornar o maior deles
    lisDelta = deltaY(fluxo)
    # vamos verificar os dados, se o delta for proximo, o periodo será o indice dentro deste intervalo
    # se a diferença entre os pontos de lisDelta for menor que delta, continuamos a analise
    start = 0
    for i in range(len(lisDelta)):
        # se a diferença for menor que delta, continuamos
        if lisDelta[i] > delta:
            # a diferença entre os dois pontos não representa parte do poço
            # vamos calcular o periodo
            periodo = time[i+1] - time[start]
            lisPeriod.append(periodo)
            # atualizando o start
            start = i    
    return np.max(lisPeriod)
