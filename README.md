# SNMP-Kafka Project
Network Analytics and Telemetry - Lab

## วัตถุประสงค์
เก็บข้อมูล interface counter จาก Router ด้วย SNMP แล้วส่งเข้า Apache Kafka เพื่อให้ consumer อ่านไปวิเคราะห์ต่อ

## สถาปัตยกรรม

    [GNS3: R1 -- R2] --SNMP(UDP 161)--> [Ubuntu VM: Docker]
                                          |- producer (poll SNMP)
                                          |- Kafka (KRaft)
                                          |- consumer

## เครื่องมือที่ใช้
GNS3, VMware, Ubuntu Server, Docker, Apache Kafka, Python

## ขั้นตอนการรัน
1. สร้าง topology ใน GNS3 และนำคอนฟิกใน `configs/R1.txt`, `configs/R2.txt` ไปใส่ที่ router
2. คัดลอก `.env.example` เป็น `.env` แล้วแก้ `SNMP_TARGETS` เป็น IP ของ fa0/0
3. รัน `docker compose up -d --build`
4. ดูผลด้วย `docker compose logs -f producer` และ `docker compose logs -f consumer`

## ผลการทดลอง
สามารถดูได้จากไฟล์ 01-topology.png

## ผู้จัดทำ
Mr.Chayut Samanupawin 6631501151
