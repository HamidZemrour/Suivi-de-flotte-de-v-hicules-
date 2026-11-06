import json, math, os, random, time, uuid
import paho.mqtt.client as mqtt
random.seed(42)
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
c.connect(os.getenv('MQTT_HOST','mqtt'),1883); c.loop_start()
tick=0
phases=[0.0]*12
while True:
    for i in range(12):
        stopped=(tick//15+i)%5==0
        if not stopped: phases[i]+=1/180
        t=phases[i]+i/3
        e=dict(event_id=str(uuid.uuid4()),vehicle_id=f'VEH-{i+1:03d}',event_ms=time.time_ns()//1000000,
               latitude=33.58+(.11 if i==0 else .045)*math.sin(t),longitude=-7.60+.06*math.cos(t),
               speed_kmh=0.0 if stopped else round(max(0,55+35*math.sin(t*2)+random.gauss(0,8)),1))
        c.publish('fleet/positions',json.dumps(e),qos=1).wait_for_publish()
    tick+=1; time.sleep(2)
