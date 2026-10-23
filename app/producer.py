import os, json, time, subprocess
from kafka import KafkaProducer

BOOT = os.environ["KAFKA_BOOTSTRAP"]
TOPIC = os.environ["KAFKA_TOPIC"]
COMM = os.environ["SNMP_COMMUNITY"]
TARGETS = os.environ["SNMP_TARGETS"].split(",")
INTERVAL = int(os.environ.get("POLL_INTERVAL", 10))

def walk(host, oid):
    out = subprocess.run(
        ["snmpwalk", "-v2c", "-c", COMM, "-On", "-Oq", host, oid],
        capture_output=True, text=True, timeout=20).stdout
    result = {}
    for line in out.strip().splitlines():
        o, v = line.split(None, 1)
        result[o.split(".")[-1]] = v.strip().strip('"')
    return result

def get(host, oid):
    return subprocess.run(
        ["snmpget", "-v2c", "-c", COMM, "-Oqv", host, oid],
        capture_output=True, text=True, timeout=10).stdout.strip()

while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers=BOOT,
            value_serializer=lambda v: json.dumps(v).encode())
        break
    except Exception as e:
        print("waiting for kafka...", e, flush=True); time.sleep(5)

while True:
    for host in TARGETS:
        try:
            names = walk(host, "1.3.6.1.2.1.2.2.1.2")
            ins = walk(host, "1.3.6.1.2.1.2.2.1.10")
            outs = walk(host, "1.3.6.1.2.1.2.2.1.16")
            msg = {
                "ts": time.time(),
                "target": host,
                "sysName": get(host, "1.3.6.1.2.1.1.5.0"),
                "sysUpTime": get(host, "1.3.6.1.2.1.1.3.0"),
                "interfaces": [
                    {"index": i, "name": names[i],
                     "in_octets": ins.get(i), "out_octets": outs.get(i)}
                    for i in names
                ],
            }
            producer.send(TOPIC, msg)
            print("sent", host, flush=True)
        except Exception as e:
            print("error", host, e, flush=True)
    producer.flush()
    time.sleep(INTERVAL)
