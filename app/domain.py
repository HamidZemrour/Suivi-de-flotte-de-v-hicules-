import math
ZONE = (33.50, 33.66, -7.72, -7.48)
def haversine(lat1, lon1, lat2, lon2):
    a=math.sin(math.radians(lat2-lat1)/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(math.radians(lon2-lon1)/2)**2
    return 6371*2*math.asin(min(1,math.sqrt(a)))
def validate(e):
    try:
        return (bool(e['event_id']) and bool(e['vehicle_id']) and 0 <= float(e['speed_kmh']) <= 220
                and -90 <= float(e['latitude']) <= 90 and -180 <= float(e['longitude']) <= 180
                and int(e['event_ms']) > 0)
    except (KeyError, TypeError, ValueError):
        return False
def incidents(e):
    lo,hi,left,right=ZONE
    return {'speeding':e['speed_kmh']>80, 'outside_zone':not(lo<=e['latitude']<=hi and left<=e['longitude']<=right)}
