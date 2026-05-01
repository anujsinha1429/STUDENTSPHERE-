from datetime import date
from app import create_app, db
from app.models import Timetable, Holiday
from run import app


with app.app_context():
   db.create_all()

   timetable_data = {
    "25E1H2": {
        "MONDAY": [
            ("UPEM-LAB", "07:45-09:15"),
            ("BREAK", "09:15-10:00"),
            ("DSA-LAB", "10:00-11:30")
        ],
        "TUESDAY": [
            ("ITW", "15:45-16:30"),
            ("CAL B", "16:30-17:15"),
            ("IGT", "17:15-18:00"),
            ("UPEM", "18:00-18:45")
        ],
        "WEDNESDAY": [
            ("IKS", "08:30-09:15"),
            ("DSA", "09:15-10:00"),
            ("CAL B", "10:00-10:45"),
            ("ITW", "10:45-11:30")
        ],
        "THURSDAY": [
            ("ITW", "08:30-09:15"),
            ("IGT", "09:15-10:00"),
            ("CAL B", "10:00-10:45"),
            ("UPEM", "10:45-11:30")
        ],
        "FRIDAY": [
            ("CAL B", "15:45-16:30"),
            ("UPEM", "16:30-17:15"),
            ("DSA", "17:15-18:00"),
            ("IGT", "18:00-18:45")
        ],
        "SATURDAY": [
            ("IKS (E-356)", "15:45-16:30"),
            ("DSA (E-356)", "16:30-17:15"),
            ("IGT (E-356)", "17:15-18:00")
        ]
    },

    "25E1K1": {
        "MONDAY": [
            ("UPEM-LAB", "15:45-17:15"),
            ("DSA-LAB", "17:15-18:45")
        ],
        "TUESDAY": [
            ("CAL B", "08:30-09:15"),
            ("UPEM", "09:15-10:00"),
            ("IGT", "10:00-10:45"),
            ("ITW", "10:45-11:30")
        ],
        "WEDNESDAY": [
            ("IKS", "15:45-16:30"),
            ("DSA", "16:30-17:15"),
            ("UPEM", "17:15-18:00"),
            ("IGT", "18:00-18:45")
        ],
        "THURSDAY": [
            ("DSA (E-356)", "09:15-10:00"),
            ("CAL B (E-356)", "10:00-10:45"),
            ("IKS (E-356)", "10:45-11:30")
        ],
        "FRIDAY": [
            ("DSA", "08:30-09:15"),
            ("ITW", "09:15-10:00"),
            ("CAL B", "10:00-10:45"),
            ("IGT", "10:45-11:30")
        ],
        "SATURDAY": [
            ("IGT", "15:45-16:30"),
            ("ITW", "16:30-17:15"),
            ("CAL B", "17:15-18:00"),
            ("UPEM", "18:00-18:45")
        ]
    }
}

   for section in timetable_data:
        for day in timetable_data[section]:
            for subject,slot in timetable_data[section][day]:
                timetable_entry = Timetable(section=section, day=day, subject=subject, slot=slot)
                db.session.add(timetable_entry)

   
   print("Data inserted")

   holidays = [

        # ===== MAIN HOLIDAYS =====
        Holiday(title="Republic Day 🇮🇳", start_date=date(2026, 1, 26), end_date=date(2026, 1, 26)),
        Holiday(title="Holi 🎨", start_date=date(2026, 3, 4), end_date=date(2026, 3, 4)),
        Holiday(title="Good Friday ✝️", start_date=date(2026, 4, 3), end_date=date(2026, 4, 3)),
        Holiday(title="Id-ul-Zuha 🕌", start_date=date(2026, 5, 27), end_date=date(2026, 5, 27)),
        Holiday(title="Rath Yatra 🚩", start_date=date(2026, 7, 16), end_date=date(2026, 7, 16)),
        Holiday(title="Independence Day 🇮🇳", start_date=date(2026, 8, 15), end_date=date(2026, 8, 15)),
        Holiday(title="Janmashtami 🦚", start_date=date(2026, 9, 4), end_date=date(2026, 9, 4)),
        Holiday(title="Ganesh Puja 🐘", start_date=date(2026, 9, 14), end_date=date(2026, 9, 14)),
        Holiday(title="Gandhi Jayanti 🕊️", start_date=date(2026, 10, 2), end_date=date(2026, 10, 2)),
        Holiday(title="Maha Navami 🔱", start_date=date(2026, 10, 19), end_date=date(2026, 10, 19)),
        Holiday(title="Vijaya Dashami 🏹", start_date=date(2026, 10, 20), end_date=date(2026, 10, 20)),
        Holiday(title="Christmas 🎄", start_date=date(2026, 12, 25), end_date=date(2026, 12, 25)),

        # ===== OPTIONAL HOLIDAYS =====
        Holiday(title="Dola Purnima 🌕", start_date=date(2026, 3, 3), end_date=date(2026, 3, 3)),
        Holiday(title="Id-Ul-Fitre 🕌", start_date=date(2026, 3, 21), end_date=date(2026, 3, 21)),
        Holiday(title="Maha Bisuba Sankranti 🌞", start_date=date(2026, 4, 14), end_date=date(2026, 4, 14)),
        Holiday(title="Budha Purnima 🌕", start_date=date(2026, 5, 1), end_date=date(2026, 5, 1)),
        Holiday(title="Sabitri Amabasya 🌑", start_date=date(2026, 5, 16), end_date=date(2026, 5, 16)),
        Holiday(title="Raja Sankranti 🌾", start_date=date(2026, 6, 15), end_date=date(2026, 6, 15)),
        Holiday(title="Moharram 🕌", start_date=date(2026, 6, 26), end_date=date(2026, 6, 26)),
        Holiday(title="Bahuda Yatra 🚩", start_date=date(2026, 7, 24), end_date=date(2026, 7, 24)),
        Holiday(title="Nuakhai 🌾", start_date=date(2026, 9, 15), end_date=date(2026, 9, 15)),
        Holiday(title="Prathamastami 👶", start_date=date(2026, 12, 1), end_date=date(2026, 12, 1)),
    ]
   
   events = [

        Holiday(title="Bridge Course Starts", start_date=date(2025,8,25)),

        Holiday(title="Odd Semester Classes Start", start_date=date(2025,9,15)),

        Holiday(title="1st Quiz Test", start_date=date(2025,10,6), end_date=date(2025,10,15)),

        Holiday(title="2nd Quiz Test", start_date=date(2025,11,3), end_date=date(2025,11,8)),

        Holiday(title="Mid Semester Exam", start_date=date(2025,11,12), end_date=date(2025,11,22)),

        Holiday(title="3rd Quiz Test", start_date=date(2025,12,15), end_date=date(2025,12,20)),

        Holiday(title="Odd Semester Break", start_date=date(2025,12,29), end_date=date(2026,1,3)),

        Holiday(title="Last Day Odd Semester", start_date=date(2026,1,7)),

        Holiday(title="Revision Classes", start_date=date(2026,1,8), end_date=date(2026,1,10)),

        Holiday(title="End Semester Exam", start_date=date(2026,1,14), end_date=date(2026,1,30)),

        # EVEN SEM

        Holiday(title="Even Semester Classes Start", start_date=date(2026,2,2)),

        Holiday(title="Even Semester Break", start_date=date(2026,2,10), end_date=date(2026,2,17)),

        Holiday(title="1st Quiz Test", start_date=date(2026,3,2), end_date=date(2026,3,7)),

        Holiday(title="2nd Quiz Test", start_date=date(2026,4,6), end_date=date(2026,4,11)),

        Holiday(title="Mid Semester Exam", start_date=date(2026,4,15), end_date=date(2026,4,25)),

        Holiday(title="3rd Quiz Test", start_date=date(2026,5,4), end_date=date(2026,5,9)),

        Holiday(title="Last Day Even Semester", start_date=date(2026,5,16)),

        Holiday(title="Revision Classes", start_date=date(2026,5,18), end_date=date(2026,5,20)),

        Holiday(title="Preparatory Break", start_date=date(2026,5,21), end_date=date(2026,5,23)),

        Holiday(title="End Semester Exam", start_date=date(2026,5,25), end_date=date(2026,6,10)),
    ]
   db.session.bulk_save_objects(holidays)
   db.session.bulk_save_objects(events)
   db.session.commit()

   print("✅ Holidays seeded successfully!")