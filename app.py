from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)

# Demo data — replace with a real database for production.
doctors = {
    "General Medicine": {"doctor": "Dr. Sharma", "avg_time": 5, "delay": 0, "current": 42, "waiting": [43,44,45,46,47,48,49,50]},
    "Orthopedics": {"doctor": "Dr. Patel", "avg_time": 7, "delay": 0, "current": 18, "waiting": [19,20,21,22,23]},
    "Dermatology": {"doctor": "Dr. Mehta", "avg_time": 4, "delay": 10, "current": 9, "waiting": [10,11,12]},
}

def estimate(dept):
    d = doctors[dept]
    patients_ahead = len(d["waiting"])
    minutes = patients_ahead * d["avg_time"] + d["delay"]
    # A simple uncertainty range makes the estimate more realistic.
    low = max(0, minutes - 5)
    high = minutes + 10
    return patients_ahead, low, high

@app.route("/")
def index():
    dept = request.args.get("department", "General Medicine")
    if dept not in doctors:
        dept = "General Medicine"
    patients, low, high = estimate(dept)
    d = doctors[dept]
    return render_template("index.html", departments=doctors, dept=dept, d=d,
                           patients=patients, low=low, high=high)

@app.route("/get-token", methods=["POST"])
def get_token():
    dept = request.form.get("department", "General Medicine")
    if dept not in doctors:
        return redirect(url_for("index"))
    d = doctors[dept]
    last = d["waiting"][-1] if d["waiting"] else d["current"]
    token = last + 1
    d["waiting"].append(token)
    return redirect(url_for("patient", department=dept, token=token))

@app.route("/patient")
def patient():
    dept = request.args.get("department", "General Medicine")
    token = request.args.get("token", "")
    if dept not in doctors:
        dept = "General Medicine"
    d = doctors[dept]
    try:
        token_num = int(token)
    except (ValueError, TypeError):
        token_num = None
    ahead = sum(1 for t in d["waiting"] if token_num is not None and t < token_num)
    if token_num is not None and token_num == d["current"]:
        ahead = 0
    minutes = ahead * d["avg_time"] + d["delay"]
    return render_template("patient.html", dept=dept, d=d, token=token_num,
                           ahead=ahead, minutes=minutes)

@app.route("/admin")
def admin():
    stats = {}
    for dept, d in doctors.items():
        ahead, low, high = estimate(dept)
        stats[dept] = {"ahead": ahead, "low": low, "high": high, **d}
    return render_template("admin.html", stats=stats)

@app.route("/next", methods=["POST"])
def next_patient():
    dept = request.form["department"]
    d = doctors[dept]
    if d["waiting"]:
        d["current"] = d["waiting"].pop(0)
    return redirect(url_for("admin"))

@app.route("/delay", methods=["POST"])
def delay():
    dept = request.form["department"]
    amount = int(request.form.get("amount", 10))
    doctors[dept]["delay"] = max(0, doctors[dept]["delay"] + amount)
    return redirect(url_for("admin"))

@app.route("/reset-delay", methods=["POST"])
def reset_delay():
    dept = request.form["department"]
    doctors[dept]["delay"] = 0
    return redirect(url_for("admin"))

@app.route("/api/status")
def status():
    result = {}
    for dept, d in doctors.items():
        ahead, low, high = estimate(dept)
        result[dept] = {
            "doctor": d["doctor"],
            "current_token": d["current"],
            "patients_waiting": ahead,
            "estimated_wait": f"{low}-{high} min",
            "delay": d["delay"]
        }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
