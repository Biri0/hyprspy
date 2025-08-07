import sqlite3
import subprocess
import json
import time
import datetime
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "logs.db")
con = sqlite3.connect(db_path)

cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS logs(start_time, end_time, class, title)")
activewindow = (0, 0)

while True:
    output = subprocess.run(["hyprctl", "-j", "activewindow"], capture_output=True)

    dump = json.loads(output.stdout.decode())

    cur_time = datetime.datetime.today().isoformat()
    wclass = dump["class"]
    title = dump["title"]

    currentwindow = (wclass, title)
    if currentwindow == activewindow:
        cur.execute(
            "UPDATE logs SET end_time = ? WHERE start_time = (SELECT MAX(start_time) FROM logs)",
            (cur_time,),
        )
    else:
        cur.execute(
            "INSERT INTO logs(start_time, end_time, class, title) VALUES (?, ?, ?, ?)",
            (
                cur_time,
                cur_time,
                wclass,
                title,
            ),
        )
        activewindow = currentwindow

    con.commit()
    time.sleep(1)
