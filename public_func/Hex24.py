SPchars="0123456789ABCDEFGHIJKLMN"

def parseXY(SPcode=''):
    lon = -1
    lat = -1
    if len(SPcode)==12:
        lon=Hex24toDecimal(Hexstr=SPcode[0:6])
        lat=Hex24toDecimal(Hexstr=SPcode[6:])
    return lon,lat

def parseSP(lon=-1,lat=-1):
    if lon>180000000 and lon<0 and lat>90000000 and lat<0:
        return None
    result = None
    lonSPkey=parse24Hex(Dec=lon)
    latSPkey=parse24Hex(Dec=lat)
    if lonSPkey is None or latSPkey  is None:
        return None
    return lonSPkey+latSPkey

def parse24Hex(Dec=None):
    result = None
    if Dec is None:
        return result
    try:
    #if True:
        result = ''
        Dec = int(Dec)
        for i in range(6):
            Dec,Hex = divmod(Dec, 24)
            result = SPchars[Hex]+result
        if Dec>24 or len(result)!=6:
            return None
    except:
        pass
    return result

def Hex24toDecimal(Hexstr=''):
    Dec = 0
    for Hexchar in Hexstr:
        Hex = SPchars.find(Hexchar)
        if Hex < 0 :
            return -1
        Dec = (Dec+Hex)*24
    Dec = Dec/24
    return Dec

if __name__=='__main__':
    print parseSP(lon=94086914,lat=24327077)
    print parseXY(SPcode='EGH0I64EBKH2')
    print Hex24toDecimal(Hexstr='EK58B1')
    print Hex24toDecimal(Hexstr='31JC47')
    
