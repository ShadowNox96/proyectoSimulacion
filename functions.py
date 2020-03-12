import random

def generateRandoms(x, PP, data):
    rangePersons = range(x)
    result = []
    prod = ''
    cost =0
    totalCost =0
    tdata = len(data)
    for i in rangePersons:
        products = range(random.randint(1,PP))
        for j in products:
            rd = random.randint(0,tdata-1)
            d = data[rd][1]
            prod = str(prod) + ',' + str(d)
            cost = cost + data[rd][0]
            totalCost = totalCost + cost
        
        result.append([i+1,prod,cost])
        prod = ''
        cost =0
                
    return result,totalCost