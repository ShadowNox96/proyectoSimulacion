import random

def generateRandoms(PLl, PP, HS, data):
    
    ranPerson = range(PLl)
    ranH = range(0, HS,1)
    result =[]
    
    for x in ranH:
        for y in ranPerson:
            products = []
            tProd = random.randint(1, PP)
            ranProd = range(0,tProd,1)
            result.append([x+1,y+1,tProd,products])
            for p in ranProd:
                prodRandom = random.randint(0,len(data)-1)
                products.append(data[prodRandom])
    return result