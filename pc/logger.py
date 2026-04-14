#!/usr/bin/env python3
"""
XIAO ESP32-C6 NTC Logger - Linux PC Client
Features: 
- Auto-discovery of serial ports
- Real-time "Rich" dashboard
- CSV logging
- Robust error handling
"""

import os
# Python NTC Logger PC Client
import sys
import serial
import json
import csv
import time
import glob
from datetime import datetime
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich import box

# Configuration
LOG_FILE = "temperature_logs.csv"
BAUD_RATE = 115200
DEFAULT_TIMEOUT = 2

console = Console()

def find_serial_port():
    """Finds available serial ports on Linux/macOS/Windows."""
    if sys.platform.startswith('linux'):
        ports = glob.glob('/dev/ttyACM*') + glob.glob('/dev/ttyUSB*')
    elif sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    else:
        ports = glob.glob('/dev/tty.*')
    
    valid_ports = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            valid_ports.append(port)
        except (OSError, serial.SerialException):
            pass
    return valid_ports

def generate_dashboard(data, status="Connected"):
    """Generates the Rich dashboard layout."""
    table = Table(box=box.DOUBLE_EDGE, expand=True)
    table.add_column("Timestamp", style="cyan", justify="center")
    table.add_column("Sensor 1 (A0)", style="bold magenta", justify="center")
    table.add_column("Sensor 2 (A1)", style="bold green", justify="center")
    table.add_column("Difference", style="yellow", justify="center")

    t1 = data.get("t1", 0.0)
    t2 = data.get("t2", 0.0)
    diff = abs(t1 - t2)
    now = datetime.now().strftime("%H:%M:%S")

    table.add_row(
        now,
        f"{t1:.2f} °C",
        f"{t2:.2f} °C",
        f"{diff:.2f} °C"
    )

    status_color = "green" if status == "Connected" else "red"
    panel = Panel(
        table,
        title=f"[bold white]XIAO ESP32-C6 Temperature Logger[/]",
        subtitle=f"[bold {status_color}]Status: {status}[/]",
        border_style="bright_blue"
    )
    return panel

def main():
    console.clear()
    console.print(Panel("[bold yellow]Scanning for XIAO ESP32-C6...[/]", border_style="yellow"))
    
    ports = find_serial_port()
    if not ports:
        console.print("[bold red]Error: No serial ports found. Please connect your XIAO ESP32-C6.[/]")
        sys.exit(1)
    
    target_port = ports[0]
    console.print(f"[bold green]Targeting port: {target_port}[/]")

    # Initialize CSV
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Temp1_C", "Temp2_C"])

    try:
        with serial.Serial(target_port, BAUD_RATE, timeout=DEFAULT_TIMEOUT) as ser:
            latest_data = {"t1": 0.0, "t2": 0.0}
            
            with Live(generate_dashboard(latest_data), refresh_per_second=4, console=console) as live:
                while True:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if not line:
                        continue
                    
                    try:
                        data = json.loads(line)
                        if "t1" in data and "t2" in data:
                            latest_data = data
                            live.update(generate_dashboard(latest_data))
                            
                            # Log to CSV
                            with open(LOG_FILE, 'a', newline='') as f:
                                writer = csv.writer(f)
                                writer.writerow([
                                    datetime.now().isoformat(),
                                    data["t1"],
                                    data["t2"]
                                ])
                    except json.JSONDecodeError:
                        # Skip malformed lines (e.g., boot messages)
                        pass

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Logging stopped by user.[/]")
    except Exception as e:
        console.print(f"\n[bold red]Fatal Error: {e}[/]")

if __name__ == "__main__":
    main()
