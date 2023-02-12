import numpy as np

def weightSoma(fluxErr):
    return np.power(np.sum(np.power(fluxErr,-2)),-1)

def rValue(i1,i2,weight):
    return np.sum(np.fromiter((weight[i] for i in range(i1,i2)), dtype=float))

def sValue(i1,i2,weight,fluxo):
    return np.sum(np.fromiter((weight[i]*fluxo[i] for i in range(i1,i2)), dtype=float))

def dValue(lisWeight,fluxo,r,s):
    soma = np.sum(np.fromiter((lisWeight[i]*fluxo[i]**2 for i in range(len(lisWeight))), dtype=float))
    return (soma - (s**2)/(r*(1-r)))

def myBls(fluxo,fluxoErr):
    lisWeight = []
    somaW = weightSoma(fluxoErr)

    for i1 in range(len(fluxo)):
        wi = somaW*(fluxoErr[i1]**(-2))
        lisWeight.append(wi)

    for i1 in range(946,len(fluxo)):
        for i2 in range(i1+1,len(fluxo)):
            print(f"i1 {i1+1}, i2 = {i2+1}")
            r = rValue(i1,i2,lisWeight)
            s = sValue(i1,i2,lisWeight,fluxo)
            d = dValue(lisWeight,fluxo,r,s)

            with open('/content/gdrive/MyDrive/logArthur/data.csv', 'a') as f:
                f.write(str(i1)+',' + str(i2) +',' + str(d) + '\n')