# OPD SmartQueue — Hackathon Prototype

## Problem
Hospital OPD patients often do not know how long they will wait. Queue size, consultation time and doctor delays make the waiting time uncertain.

## Solution
OPD SmartQueue estimates a waiting-time range using:
- Patients ahead in the queue
- Average consultation duration
- Doctor delay/unavailability

The estimate changes when staff call the next patient or add a delay.

## Run
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Run:
   `pip install -r requirements.txt`
4. Start:
   `python app.py`
5. Open the local address shown in the terminal, usually `http://127.0.0.1:5000`.

## Demo flow
1. Open the patient page.
2. Choose a department and click **Get Token**.
3. Show the token and estimated wait.
4. Open **Hospital Dashboard**.
5. Click **Call Next** and refresh the patient view.
6. Click **+10m Delay** to demonstrate uncertainty.
7. Explain that real hospital systems could feed live queue/doctor data into the same prediction engine.

## Important
This is a hackathon prototype using simulated data. It is not a medical decision-making system and should not be deployed in a real hospital without security, privacy, validation and integration work.
