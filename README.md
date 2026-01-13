# CTFtimeBot

บอท Discord สำหรับดึงข้อมูลการแข่งขัน CTF จาก CTFtime แล้วแจ้งเตือนใน Discord  
ใช้เพื่อฝึกการเขียน Python การใช้งาน API และการใช้ Docker สำหรับ deployment

> หมายเหตุ: โปรเจกต์นี้สร้างขึ้นเพื่อการเรียนรู้และพัฒนาทักษะของผู้พัฒนา  
> มุ่งเน้น Python, CTFtime API, Discord Bot API และ Docker

## ฟีเจอร์หลัก

- ดึงรายการแข่งขัน CTF จาก CTFtime
- แจ้งเตือนกิจกรรมผ่าน Discord
- ทำงานอัตโนมัติตามช่วงเวลา
- รองรับการรันใน Docker container

## เทคโนโลยีที่ใช้

- Python
- Discord API
- CTFtime API
- Asyncio
- Docker

## โครงสร้างโปรเจกต์

- main.py — โค้ดหลักของบอท
- config.json — ตัวอย่างไฟล์ตั้งค่า
- Dockerfile — สำหรับสร้าง Docker image
- requirements.txt — ไลบรารีที่ต้องติดตั้ง

## วิธีใช้งานแบบปกติ

### 1. โคลนโปรเจกต์

git clone https://github.com/same-sain/CTFtimeBot.git  
cd CTFtimeBot

### 2. ติดตั้ง dependencies

pip install -r requirements.txt

### 3. ตั้งค่าไฟล์ config

คัดลอกไฟล์:

cp config.example.json config.json

แก้ไขข้อมูล:
- Discord bot token  
- Channel ID  

### 4. รันบอท

python bot.py

## วิธีใช้งานผ่าน Docker

### 1. สร้าง image

docker build -t ctftime-bot .

### 2. รัน container

docker run -d ctftime-bot

(แนะนำให้ตั้งค่า TOKEN ผ่าน environment variable)

ตัวอย่าง:

docker run -e DISCORD_TOKEN=xxxxxxxx -e CHANNEL_ID=12345678 -d ctftime-bot


## ผู้พัฒนา

- Nitiwat Aurarak
