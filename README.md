# CTFtimeBot

บอท Discord สำหรับดึงข้อมูลการแข่งขัน CTF จาก CTFtime แล้วแจ้งเตือนในช่อง Discord  
ใช้เพื่อฝึกการเขียน Python และการใช้งาน API

> หมายเหตุ: โปรเจกต์นี้สร้างขึ้นเพื่อการเรียนรู้และพัฒนาทักษะของผู้พัฒนา  
> มุ่งเน้นการใช้งาน Python, CTFtime API และ Discord Bot API

## ภาพรวม

ฟังก์ชันหลักของบอท:
- ดึงข้อมูลการแข่งขัน CTF ที่กำลังจะมาถึง
- สรุปข้อมูลกิจกรรม
- ส่งข้อความแจ้งเตือนใน Discord Server

## เทคโนโลยีที่ใช้

- Python  
- Discord API  
- CTFtime API  
- Asyncio  

## วิธีการใช้งาน

1. โคลนโปรเจกต์  
   git clone https://github.com/same-sain/CTFtimeBot.git  
   cd CTFtimeBot

2. ติดตั้ง dependencies  
   pip install -r requirements.txt

3. คัดลอกไฟล์ตั้งค่า  
   cp config.example.json config.json

4. ใส่ token Discord + channel id

5. เริ่มรันบอท  
   python bot.py

## ฟีเจอร์หลัก

- ดึงกิจกรรม CTF จาก CTFtime  
- แจ้งเตือนผ่าน Discord  
- ตั้งเวลาการแจ้งเตือนได้  
- ปรับแต่งข้อความได้  

## ผู้พัฒนา

- Nitiwat Aurarak
