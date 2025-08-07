import sqlite3
import subprocess
import json
import time
import os
import sys
import atexit

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "logs.db")
lock_file = os.path.join(script_dir, "hyprspy.lock")


def check_if_running():
    if os.path.exists(lock_file):
        try:
            with open(lock_file, "r") as f:
                pid = int(f.read().strip())

            try:
                os.kill(pid, 0)
                print(f"Hyprspy is already running with PID {pid}")
                sys.exit(1)
            except OSError:
                os.remove(lock_file)
        except (ValueError, FileNotFoundError):
            if os.path.exists(lock_file):
                os.remove(lock_file)


def create_lock():
    with open(lock_file, "w") as f:
        f.write(str(os.getpid()))


def cleanup():
    if os.path.exists(lock_file):
        os.remove(lock_file)


check_if_running()
create_lock()
atexit.register(cleanup)

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
