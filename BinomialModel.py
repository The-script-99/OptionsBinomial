from decimal import Decimal 

#Enter data
priceSec = 50
priceUp = 2
priceDown = 1/2
time = 2
intrest = 0.25
strike = 5


def getOptionValue(p,t,pUp,pDown,intrest,strike):

    outcomes = getOutcomes(t,pUp,pDown,p)
    values = setSubOptionValue(outcomes,strike)

    if((pDown/p>0 and pDown/p<1+intrest) and 1+intrest<pUp/p):
        return "N/A. 0<d<1+r<u"
    
    if(len(values)>1):
        i = len(values)-2
        while i>=0:
            j = 0
            l = []
            while j<len(values[i]):
                l.append(getValue(outcomes[i][j],outcomes[i+1][j*2],outcomes[i+1][j*2+1],values[i+1][j*2],values[i+1][j*2+1],intrest))
                j+=1
            values[i] = l
            i-=1
   
    return getValue(p,outcomes[0][0],outcomes[0][1],values[0][0],values[0][1],intrest)

def getValue(p,pUp,pDown,vUp,vDown,i):
    value = 0

    #price parameters
    delta = (vUp-vDown)/(pUp-pDown)
    bond = (vDown-delta*pDown)/(1+i)
    
    value = delta*p+bond

    if(value<0):
        return 0

    return value

def setSubOptionValue(out,strike):
    
    list = []
    p = 0
    for x in out[len(out)-1]:
        p = x-strike
        if(p<0):
            list.append(0)
            continue
        list.append(p)
    out = out*1
    out[len(out)-1] = list

    return out

def getOutcomes(time,stepUp,stepDown,price):
    outcomes = []

    i = 1
    while i<=time:
        if(i==1):
            outcomes.append(getSubOutcomes(stepUp,stepDown,price))
            i+=1
            continue
        list = []
        for x in outcomes[i-2]:
            for y in getSubOutcomes(stepUp,stepDown,x):
                list.append(y)
        
        outcomes.append(list)
        i+=1
    
    return outcomes

def getSubOutcomes(stepUp,stepDown,price):
    
    list = []

    i = 1
    j = 1
    z = i
    y = 0
    while j<=pow(2,i):
        x = price * pow(stepUp,z)*pow(stepDown,y)
        z -= 1
        y += 1
        j += 1
        list.append(x)

    return list

def setSubPutValue(out,strike):
    
    list = []
    p = 0
    for x in out[len(out)-1]:
        p = strike-x
        if(p<0):
            list.append(0)
            continue
        list.append(p)
    out = out*1
    out[len(out)-1] = list

    return out

def getValuePut(p,pUp,pDown,vUp,vDown,i):
    value = 0

    delta = (vDown-vUp)/(pDown-pUp)
    bond = (vDown-delta*pDown)/(1+i)
    
    value = delta*p+bond

    if(value<0):
        return 0

    return value

def getPutValue(p,t,pUp,pDown,i,strike):
    outcomes = getOutcomes(t,pUp,pDown,p)
    values = setSubPutValue(outcomes,strike)
    
    if((pDown/p>0 and pDown/p<1+i) and 1+i<pUp/p):
        return "N/A. 0<d<1+r<u"
    
    if(len(values)>1):
        i = len(values)-2
        while i>=0:
            j = 0
            l = []
            while j<len(values[i]):
                l.append(getValuePut(outcomes[i][j],outcomes[i+1][j*2],outcomes[i+1][j*2+1],values[i+1][j*2],values[i+1][j*2+1],intrest))
                j+=1
            values[i] = l
            i-=1
    return getValuePut(p,outcomes[0][0],outcomes[0][1],values[0][0],values[0][1],intrest)

def getCallRisk(p,t,pUp,pDown,intrest,strike):

    values = getOutcomes(t,pUp,pDown,p)
    values = setSubOptionValue(values,strike)

    if((pDown/p>0 and pDown/p<1+intrest) and 1+intrest<pUp/p):
        return "N/A. 0<d<1+r<u"
    
    if(len(values)>1):
        i = len(values)-2
        while i>=0:
            j = 0
            l = []
            while j<len(values[i]):
                l.append(getValueRisk(pUp,pDown,values[i+1][j*2],values[i+1][j*2+1],intrest))
                j+=1
            values[i] = l
            i-=1
    return getValueRisk(pUp,pDown,values[0][0],values[0][1],intrest)

def getValueRisk(pUp,pDown,vUp,vDown,i):

    u = pUp
    d = pDown
    p = (1+i-d)/(u-d)
    q = (u-1-i)/(u-d)

    v = (p*vUp+q*vDown)/(1+i)
    if(v<0):
        return 0

    return v

def getPutRisk(p,t,pUp,pDown,intrest,strike):

    values = getOutcomes(t,pUp,pDown,p)
    values = setSubPutValue(values,strike)

    if((pDown/p>0 and pDown/p<1+intrest) and 1+intrest<pUp/p):
        return "N/A. 0<d<1+r<u"
    
    if(len(values)>1):
        i = len(values)-2
        while i>=0:
            j = 0
            l = []
            while j<len(values[i]):
                l.append(getValueRisk(pUp,pDown,values[i+1][j*2],values[i+1][j*2+1],intrest))
                j+=1
            values[i] = l
            i-=1
    return getValueRisk(pUp,pDown,values[0][0],values[0][1],intrest)

def getCallRiskDirect(p,t,pUp,pDown,intrest,strike):

    if((pDown/p>0 and pDown/p<1+intrest) and 1+intrest<pUp/p):
        return "N/A. 0<d<1+r<u"
    price = p
    outcomes = binary_list(t)
    value = []

    x  = 0
    u = pUp
    d = pDown
    p = (1+intrest-d)/(u-d)
    q = 1-p

    for x in outcomes:
        v = price
        for i in x:
            if(i == "0"):
                v = v*u
                continue
            v = v*d
        value.append(v)
    e = 0
   
    j = -1
    for x in value:
        v = x-strike
        j +=1
        if(v<0):
            continue
        for i in outcomes[j]:
            if(i == "0"):
                v = v*p
                continue
            v = v * q
        e = e + v/pow(1+intrest,t)

    return e

def binary_list(n):
    l = []
    for i in range(pow(2,n)):
        b = bin(i)[2:]
        b = str(b).zfill(n)
        l.append(b)
    return l

def getCallRiskPascal(price,t,u,d,intrest,strike):

    p = (1+intrest-d)/(u-d)
    q = 1-p
    i,j = t,0
    row = getRow(t)
    value = 0

    if(not(0<d<1+intrest<u)):
        return "N/A. 0<d<1+r<u"

    for x in row:
        x = Decimal(x)
        v = price*pow(u,i)*pow(d,j)
        v = v-strike
        
        if(v>0):
            v = v*pow(p,i)*pow(q,j)
            v = Decimal(v)
            o = Decimal(v*x)
            de = Decimal(pow(1+intrest,t))
            o = o/de
            value = value + o
        j+=1
        i-=1

    return value

def getRow(N):

    l = []
    prev = 1
    l.append(prev)

    for i in range(1, N + 1):
        curr = (prev * (N - i + 1)) // i
        l.append(curr)
        prev = curr

    return l

def getAmericanPut(price,t,u,d,intrest,strike):
    
    outcomes = getOutcomes(t,u,d,price)
    values = setSubPutValue(outcomes,strike)
    
    if(not(0<d<1+intrest<u)):
        return "N/A. 0<d<1+r<u"
    
    if(len(values)>1):
        i = len(values)-2
        while i>=0:
            j = 0
            l = []
            while j<len(values[i]):
                l.append(getValuePutAmerican(outcomes[i][j],outcomes[i+1][j*2],outcomes[i+1][j*2+1],values[i+1][j*2],values[i+1][j*2+1],intrest,strike))
                j+=1
            values[i] = l
            i-=1
    
    return getValuePutAmerican(price,outcomes[0][0],outcomes[0][1],values[0][0],values[0][1],intrest,strike)

def getValuePutAmerican(p,pUp,pDown,vUp,vDown,i,strike):
    value = 0

    #price parameters
    delta = (vDown-vUp)/(pDown-pUp)
    bond = (vDown-delta*pDown)/(1+i)
    
    value = delta*p+bond
    if(value<strike-p):
        value = strike-p
    if(value<0):
        return 0

    return value
#print("Option value is: ",str(getOptionValue(priceSec,time,priceUp,priceDown,intrest,strike)))

#print("Option value is: ",str(getCallRisk(priceSec,time,priceUp,priceDown,intrest,strike)))

#print("Option value is: ",str(getPutRisk(priceSec,time,priceUp,priceDown,intrest,strike)))

#print("Option value is: ",str(getCallRiskDirect(priceSec,time,priceUp,priceDown,intrest,strike)))

#print("Option value is: ",str(getCallRiskPascal(priceSec,time,priceUp,priceDown,intrest,strike)))

print("Option value is: ",str(getAmericanPut(priceSec,time,priceUp,priceDown,intrest,strike)))