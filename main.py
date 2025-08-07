import sqlite3
import subprocess
import json
import time
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "logs.db")
con = sqlite3.connect(db_path)

cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS logs(start_time, seconds, class, title)")

activewindow = (0, 0)
seconds = 0

while True:
    output = subprocess.run(["hyprctl", "-j", "activewindow"], capture_output=True)

    if output.stdout == b"{}\n":
        activewindow = (0, 0)
        time.sleep(1)
        continue

    dump = json.loads(output.stdout.decode())

    cur_time = int(time.time() * 1000)
    wclass = dump["class"]
    title = dump["title"]

    currentwindow = (wclass, title)
    if currentwindow == activewindow:
        seconds += 1
        cur.execute(
            "UPDATE logs SET seconds = ? WHERE start_time = (SELECT MAX(start_time) FROM logs)",
            (seconds,),
        )
    else:
        seconds = 0
        cur.execute(
            "INSERT INTO logs(start_time, seconds, class, title) VALUES (?, ?, ?, ?)",
            (
                cur_time,
                seconds,
                wclass,
                title,
            ),
        )
        activewindow = currentwindow

    con.commit()
    time.sleep(1)
