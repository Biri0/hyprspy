# HyprSpy

HyprSpy is a lightweight Python utility for tracking your active window usage on Hyprland-based Linux systems. It periodically records the currently focused window's class and title, along with timestamps, to a local SQLite database. This allows you to analyze your workflow, productivity, or simply keep a history of your window activity.

## Features

- Monitors the active window every second
- Logs window class and title with start time and duration
- Stores data in a local SQLite database (`logs.db`)
- Simple, efficient, and easy to use

## Requirements

- Python 3.7 or newer
- [Hyprland](https://github.com/hyprwm/Hyprland) window manager
- `hyprctl` command-line tool (included with Hyprland)
- Standard Python libraries: `sqlite3`, `subprocess`, `json`, `time`, `os`, `sys`, `atexit`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Biri0/hyprspy.git
    cd hyprspy
    ```

2. Make sure you are running Hyprland and have `hyprctl` available in your PATH.

## Recommended Usage

The best way to start HyprSpy is to add the following line to your `hyprland.conf` file:
```
exec-once = python3 /absolute/path/to/hyprspy/main.py
```
Replace `/absolute/path/to/hyprspy/main.py` with the actual path to the file on your system. This will ensure HyprSpy starts automatically when your Hyprland session begins.

## Manual Usage

You can also run the script manually:
```bash
python3 main.py
```
This will start logging your active window information to `logs.db` located in the same directory as the script, regardless of where you run the command. The script runs indefinitely, updating the database every second.

## Database Schema

HyprSpy creates a SQLite database named `logs.db` with a single table:

- `logs(start_time, seconds, class, title)`

Each entry represents a period during which a specific window was active. `start_time` is a timestamp in milliseconds, `seconds` is the duration in seconds, while `class` and `title` describe the window.

## Example Query

To view your logged window activity, you can use the SQLite CLI:
```bash
sqlite3 logs.db "SELECT * FROM logs ORDER BY start_time DESC LIMIT 10;"
```

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to contribute or suggest improvements!
