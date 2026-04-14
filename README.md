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

### 2. PC Logger (Linux)
The logger requires Python 3.7+ and two libraries:
```bash
pip install pyserial rich
```

To start logging:
```bash
# Navigate to the pc folder
cd pc

# Run the logger
python3 logger.py
```

## 📊 Features
- **Factory Calibrated**: Uses `analogReadMilliVolts` to utilize ESP32-C6 internal eFuse calibration.
- **Real-time Dashboard**: Beautiful terminal UI with live updates.
- **CSV Logging**: Automatically saves data to `temperature_logs.csv` with ISO timestamps.
- **JSON Protocol**: Structured data transmission for easy expansion.
