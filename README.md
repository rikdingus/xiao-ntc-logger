# XIAO ESP32-C6 Dual NTC Logger

A professional-grade temperature logging system for the Seeed Studio XIAO ESP32-C6.

## 🔌 Wiring Diagram

Connect your NTC thermistors and fixed resistors as follows:

```text
3.3V (VCC) ---------+-----------+
                    |           |
                  [NTC1]      [NTC2]
                    |           |
A0 -----------------+           |
                    |           |
                  [10k]         |
                    |           |
A1 -----------------+-----------+
                    |
                  [10k]
                    |
GND ----------------+-----------+
```

| Component | Value | Connection |
|-----------|-------|------------|
| NTC1 | 10kΩ | Between 3.3V and A0 |
| NTC2 | 10kΩ | Between 3.3V and A1 |
| Resistor1 | 10kΩ | Between A0 and GND |
| Resistor2 | 10kΩ | Between A1 and GND |

## 🚀 Getting Started

### 1. Firmware (ESP32-C6)

1. Open `logger_firmware/logger_firmware.ino` in the Arduino IDE.
2. Install the **ESP32** board manager (version 3.0.0+ for ESP32-C6 support).
3. Select board: `XIAO_ESP32C6`.
4. Flash the code to your XIAO.

### 2. PC Logger (Windows/Linux)

The logger requires Python 3.12+ and several libraries. We recommend using a local virtual environment for isolation and full IDE support.

#### Local Environment Setup (Recommended)

This repository includes a `.vscode/settings.json` that automatically detects the local `venv`. To set it up manually:

```bash
# Navigate to the pc folder
cd pc

# Create and activate venv (Windows)
python -m venv venv
.\venv\Scripts\activate

# Install requirements
pip install pyserial rich
```

To start logging:

```bash
python logger.py
```

#### Global Setup (Quick Start)

Alternatively, you can install the libraries globally:

```bash
pip install pyserial rich
python pc/logger.py
```

## 📊 Features

- **Factory Calibrated**: Uses `analogReadMilliVolts` to utilize ESP32-C6 internal eFuse calibration.
- **Real-time Dashboard**: Beautiful terminal UI with live updates.
- **CSV Logging**: Automatically saves data to `temperature_logs.csv` with ISO timestamps.
- **JSON Protocol**: Structured data transmission for easy expansion.
