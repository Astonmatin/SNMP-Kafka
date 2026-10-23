import os, json, time
from kafka import KafkaConsumer

while True:
    try:
        c = KafkaConsumer(
            os.environ["KAFKA_TOPIC"],
            bootstrap_servers=os.environ["KAFKA_BOOTSTRAP"],
            group_id="snmp-consumer",
            auto_offset_reset="earliest",
            value_deserializer=lambda v: json.loads(v.decode()))
        break
    except Exception as e:
        print("waiting for kafka...", e, flush=True); time.sleep(5)

for m in c:
    d = m.value
    print(f"[{d['sysName']}] up={d['sysUpTime']}", flush=True)
    for i in d["interfaces"]:
        print(f"   {i['name']}: in={i['in_octets']} out={i['out_octets']}", flush=True)
