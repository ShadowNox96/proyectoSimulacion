import random


def generateRandoms(x, PP, data):
    rangePersons = range(x)
    result = []
    prod = ''
    cost = 0
    totalCost = 0
    tdata = len(data)
    for i in rangePersons:
        products = range(random.randint(1, PP))

        for j in products:
            rd = random.randint(0, tdata-1)
            d = data[rd][1]
            prod = str(prod) + ',' + str(d)
            cost = cost + data[rd][0]
        totalCost = totalCost + cost
        print(totalCost)
        result.append([i+1, prod, cost])
        prod = ''
        cost = 0
    return result, totalCost


def colasdeEspera(Pll, PS):
    lq = round(((Pll**2)/(PS*(PS-Pll))), 0)
    wq = round(lq/Pll, 4)
    ls = round(((Pll)/(PS-Pll)), 0)
    ws = round((ls/Pll), 4)
    tllegada = round((1/Pll), 4)
    tservicio = round((1/PS), 4)
    return lq, wq, ls, ws, tllegada, tservicio
