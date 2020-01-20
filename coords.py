def parseCoords(coords):
    info, payload = coords.split(':')
    payload.strip()
    if 'CGPSINFO' not in info:
        return None
    lat, latdir, lon, londir = payload.split(',')[:4]
    lat = degValue(float(lat), latdir)
    lon = degValue(float(lon), londir)
    return lat, lon

def degValue(value, dir):
    degrees = value // 100
    minutes = value - degrees * 100
    degrees += minutes / 60
    if dir == 'S' or dir == 'W':
        degrees *= -1
    return degrees

# a = parseCoords('+CGPSINFO: 4627.550763,N,03045.104499,W,100120,074931.0,54.4,0.0,264.1')
# print(a)
    