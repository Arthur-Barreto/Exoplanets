import numpy as np

def normaliza(vetor):
    dp = np.std(vetor)
    media = np.mean(vetor)
    for i in range(len(vetor)):
        vetor[i] = (vetor[i] - media)/dp
    return vetor

# o peso é dado por uma parte comum, dado perto retorno abaixo
# para poupar processo computacional iremos realizar o calcul5o somente uma vez

def weightSoma(fluxErr):
    return np.power(np.sum(np.power(fluxErr,-2)),-1)

# o tempo relativo gasto na fase L é definido por r
# o mesmo pode ser calculado como segue abaixo

def rValue(i1,i2,weight):
    return np.sum(np.fromiter((weight[i] for i in range(i1,i2)), dtype=float))

def sValue(i1,i2,weight,fluxo):
    return np.sum(np.fromiter((weight[i]*fluxo[i] for i in range(i1,i2)), dtype=float))

def somaDvalue(lisWeight,fluxo):
    return np.sum(np.multiply(lisWeight,np.power(fluxo,2)))

# def dValue(soma,r,s):
#     return (soma - (s**2)/(r*(1-r)))

def dValue(somaD,r,s):
    return np.subtract(somaD,np.divide(np.power(s,2),np.multiply(r,(1-r))))

# função que calcula o BLS, dado o tempo e o fluxo
#  x[i] = fluxo
#  y[i] = fluxoErRO

def bls(time,fluxo,fluxoErr):
    # fluxo é o eixo x
    # fluxoErr é o eixo y
    # time e fluxo devem ter o mesmo tamanho
    if (len(time) != len(fluxo)) or (len(time) != len(fluxoErr)):
        print("Erro: time e fluxo devem ter o mesmo tamanho")
        return -1
    # vamos verificar se a curva está normalizada, se não iremos normalizar
    if np.mean(fluxo) != 0 or np.std(fluxo) != 1:
        fluxo = normaliza(fluxo)
    # agora vamos iterar sobre a lista fluxo, calcular a reg linear
    # caso modulo do coeficiente suba muito, temos uma região de transito

    lisWeight = []
    menorD = None
    periodo = None
    somaW = weightSoma(fluxoErr)

    for i1 in range(len(fluxo)):
        wi = somaW*(fluxoErr[i1]**(-2))
        lisWeight.append(wi)

    print(f'len lisWeight: {len(lisWeight)}')
    print(f'len fluxo: {len(fluxo)}')

    somaD = np.array(somaDvalue(lisWeight,fluxo))

    for i1 in range(len(fluxo)):
        for i2 in range(i1+1,len(fluxo)):
            print(f"i1 {i1}, i2 = {i2}")
            r = rValue(i1,i2,lisWeight)
            s = sValue(i1,i2,lisWeight,fluxo)
            print(f"Flux has {len(fluxo)} length")
            d = dValue(somaD,r,s)

            if menorD is None:
                menorD = d
                periodo = time[i2] - time[i1]
            elif d < menorD:
                periodo = time[i2] - time[i1]
            
    return periodo