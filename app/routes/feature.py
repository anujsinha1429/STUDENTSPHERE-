from flask import Blueprint,render_template,redirect,url_for,request,flash
from app import db  
from flask_login import login_required,current_user
# from app.models import feature
from datetime import datetime,date
from app.models import Holiday, Summary, Timetable
from collections import defaultdict



feature= Blueprint('feature',__name__)
@feature.route('/dashboard',methods=["POST","GET"])
@login_required
def dashboard():
    #today date and time :
    today_date=date.today()
    today=today_date.strftime("%A").upper()

    # 2️⃣ bring the timetable for the current user's section and today's day
    timetable = Timetable.query.filter_by(section=current_user.section,day=today).all()

    #make timetable sorted by time slot
    timetable.sort(key=lambda x: x.slot)
    records = Attendance.query.filter_by(user_id=current_user.id,date=today_date).all()
    attendance={}
    for r in records:
        attendance[r.timetable_id] = r.status

    summary = Summary.query.filter_by(user_id=current_user.id).first()
    if not summary:
        return redirect(url_for("feature.setup"))
    # speacial case 

    special_user = False
    
    if current_user.username.lower() in ["manvi shekhar", "manvi"]:
        special_user = True
        return render_template("dashboard.html",special_user=special_user,timetable=timetable,
                               today=today,attendance=attendance,date=today_date, 
                               section=current_user.section)
    else:
        special_user = False
    #send the timetable to the dashboard template
    return render_template(
        "dashboard.html",
        timetable=timetable,
        today=today,
        attendance=attendance,
        date=today_date,
        section=current_user.section
    )

   
   

from collections import defaultdict

@feature.route("/timetable")
@login_required
def full_timetable():

    data = Timetable.query.filter_by(section=current_user.section).all()

    timetable_dict = defaultdict(lambda: {"morning": [], "evening": []})

    for entry in data:
        hour = int(entry.slot.split(":")[0])

        if hour < 12:
            timetable_dict[entry.day]["morning"].append(entry)
        else:
            timetable_dict[entry.day]["evening"].append(entry)

    # ✅ sort slots
    for day in timetable_dict:
        timetable_dict[day]["morning"] = sorted(timetable_dict[day]["morning"],
                                                key=lambda x: int(x.slot.split(":")[0]))

        timetable_dict[day]["evening"] = sorted(timetable_dict[day]["evening"],
                                                key=lambda x: int(x.slot.split(":")[0]))

    # ✅ fix day order
    day_order = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]

    sorted_timetable = {}

    for day in day_order:
      if day in timetable_dict:
        sorted_timetable[day] = timetable_dict[day]

    return render_template(
        "timetable.html",
        timetable=sorted_timetable
    )

from app.models import Attendance
from datetime import datetime

@feature.route("/mark", methods=["POST"])
@login_required
def mark_attendance():

    timetable_id = int(request.form.get("timetable_id"))
    status = request.form.get("status")

    today = date.today()

    #  check
    existing = Attendance.query.filter_by(
        user_id=current_user.id,
        timetable_id=timetable_id,
        date=today
    ).first()

    if existing:
    #  UPDATE
        existing.status = status
    else:
    #  INSERT
        new_attendance = Attendance(
            user_id=current_user.id,
            timetable_id=timetable_id,
            date=today,
            status=status
        )
        db.session.add(new_attendance)

    db.session.commit()

    return redirect(url_for("feature.dashboard"))


#delete attendance
@feature.route("/undo", methods=["POST"])
@login_required
def undo_attendance():

    timetable_id = int(request.form.get("timetable_id"))
    today = date.today()

    entry = Attendance.query.filter_by(
        user_id=current_user.id,
        timetable_id=timetable_id,
        date=today
    ).first()

    if entry:
        db.session.delete(entry)
        db.session.commit()

    return redirect(url_for("feature.dashboard"))

def clean_subject(name):
        if not name:
            return None
        name = name.upper()
    # remove LAB
        if "UPEM-LAB" in name:
            name = name.replace("UPEM-LAB", "UPEM")
        if "DSA-LAB" in name:
            name = name.replace("DSA-LAB", "DSA")
    # remove brackets
        if "(" in name:
          name = name.split("(")[0]
        name=name.strip()
        if name=="" or name == "BREAK":
            return None
        return name
@feature.route("/attendance")
@login_required
def attendance_summary():
    user_id = current_user.id
    records = Attendance.query.filter_by(user_id=user_id).all()
    timetables = Timetable.query.filter_by(section=current_user.section).all()
    data = {}
    for t in timetables:
        subject = clean_subject(t.subject)
        if subject is None:
            continue
        if subject not in data:
            data[subject] = {"total": 0, "present": 0}

    # ab attendance count kar
    for r in records:
        subject = clean_subject(r.timetable.subject)
        if subject is None:
            continue
        data[subject]["total"] += 1
        if r.status == "Present":
            data[subject]["present"] += 1
    summary_data = Summary.query.filter_by(user_id=current_user.id).all()
    for s in summary_data:
        subject = clean_subject(s.subject)
        if subject is None:
            continue
        if subject not in data:
            data[subject] = {"total": 0, "present": 0}
        data[subject]["total"] += s.total
        data[subject]["present"] += s.present
    # percentage calculate
    result = []
    for subject in data:
        total = data[subject]["total"]
        present = data[subject]["present"]
        percentage = (present / total) * 100 if total > 0 else 0
        # required calculate
        required = 0
        if total > 0 and percentage < 75:
            required = int(((0.75 * total) - present) / 0.25) + 1

        # bunk calculate
        bunk = 0
        if total > 0:
            bunk = int((present / 0.75) - total)
            if bunk < 0:
                bunk = 0
        result.append({"subject": subject,"total": total,"present": present,"percentage": round(percentage, 2),"required": required,"bunk": bunk})
    subjects = [item["subject"] for item in result]
    percentages = [item["percentage"] for item in result]
    return render_template("attendance.html",data=result,subjects=subjects,percentages=percentages)
    # return render_template("attendance.html", data=result)

@feature.route("/setup", methods=["GET", "POST"])
@login_required
def setup():
    existing = Summary.query.filter_by(user_id=current_user.id).first()
    if existing:
       Summary.query.filter_by(user_id=current_user.id).delete()
       db.session.commit()
    
    if request.method=="POST":
        subjects=request.form.getlist("subject")
        totals=request.form.getlist("total")
        presents=request.form.getlist("present")

        for i in range (len(subjects)):
            subject = clean_subject(subjects[i])
            if subject is None:
                continue
            total=int(totals[i])
            present=int(presents[i])
            new_summary=Summary(user_id=current_user.id,subject=subject,total=total,present=present)
            db.session.add(new_summary)
        db.session.commit()
        return redirect(url_for("feature.dashboard"))
    
    timetable= Timetable.query.filter_by(section=current_user.section).all()
    subjects=set()
    for t in timetable:
        sub=clean_subject(t.subject)
        if sub:
            subjects.add(sub)
    return render_template("setup.html", subjects=subjects)

from datetime import timedelta

@feature.route("/calendar")
@login_required
def calendar():

    all_events = Holiday.query.all()
    events = []

    for h in all_events:
        event = {
            "title": h.title,
            "start": h.start_date.strftime("%Y-%m-%d"),
            "allDay": True
        }

        # ✅ handle end date safely
        if h.end_date:
            event["end"] = (h.end_date + timedelta(days=1)).strftime("%Y-%m-%d")

        # 🔥 optional color logic
        if "Exam" in h.title:
            event["color"] = "red"
        elif "Break" in h.title:
            event["color"] = "orange"
        else:
            event["color"] = "green"

        events.append(event)

    return render_template("calender.html", events=events)