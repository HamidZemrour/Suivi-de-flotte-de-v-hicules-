import json, os
import paho.mqtt.client as mqtt
from kafka import KafkaProducer
producer=KafkaProducer(bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP','kafka:9092'),acks='all',retries=10)
def connected(client,userdata,flags,reason,properties):
    client.subscribe('fleet/positions',qos=1)
def received(client,userdata,msg):
    # Le payload est transmis sans transformation. QoS 1 autorise les doublons.
    e=json.loads(msg.payload)
    producer.send('positions',key=e['vehicle_id'].encode(),value=msg.payload).get(timeout=30)
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
c.on_connect=connected; c.on_message=received
c.connect(os.getenv('MQTT_HOST','mqtt'),1883); c.loop_forever()
