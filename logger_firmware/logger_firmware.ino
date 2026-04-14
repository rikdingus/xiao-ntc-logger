/**
 * XIAO ESP32-C6 Dual NTC Temperature Logger
 * 
 * Hardware Setup:
 * - NTC Thermistor 1 (10k @ 25C, B=3950) -> Pin A0
 * - NTC Thermistor 2 (10k @ 25C, B=3950) -> Pin A1
 * - Voltage Divider: 
 *   3.3V --- [NTC] --- ADC --- [10k Fixed] --- GND
 * 
 * Outputs JSON over Serial at 1Hz.
 */

#include <Arduino.h>

// Pin Definitions
const int PIN_NTC1 = A0;
const int PIN_NTC2 = A1;

// NTC Constants
const float SERIES_RESISTOR = 10000.0;   // 10k fixed resistor
const float NOMINAL_RESISTANCE = 10000.0; // 10k thermistor at 25C
const float NOMINAL_TEMPERATURE = 25.0;  // 25 degrees C
const float BETA_COEFFICIENT = 3950.0;     // Beta value
const float VIN_MV = 3300.0;             // Reference voltage in mV

// Sample rate
const uint32_t INTERVAL_MS = 1000;
uint32_t lastMillis = 0;

/**
 * Convert ADC (mV) to Temperature (Celsius)
 */
float readTemperature(int pin) {
    // Get calibrated millivolts directly
    float vOut = analogReadMilliVolts(pin);
    
    if (vOut >= VIN_MV) return -999.0; // Avoid division by zero/invalid state
    if (vOut <= 0) return 999.0;

    // Resistance = R_fixed * (Vin / Vout - 1)
    float resistance = SERIES_RESISTOR * (VIN_MV / vOut - 1.0);
    
    // Beta Equation: 1/T = 1/T0 + 1/B * ln(R/R0)
    float steinhart;
    steinhart = resistance / NOMINAL_RESISTANCE;      // (R/Ro)
    steinhart = log(steinhart);                       // ln(R/Ro)
    steinhart /= BETA_COEFFICIENT;                    // 1/B * ln(R/Ro)
    steinhart += 1.0 / (NOMINAL_TEMPERATURE + 273.15); // + (1/To)
    steinhart = 1.0 / steinhart;                      // Invert
    steinhart -= 273.15;                              // Convert to Celsius
    
    return steinhart;
}

void setup() {
    Serial.begin(115200);
    while (!Serial) delay(10); // Wait for USB connection
    
    // Set ADC resolution to 12-bit (XIAO C6 default)
    analogReadResolution(12);
    
    // Configure pins
    pinMode(PIN_NTC1, INPUT);
    pinMode(PIN_NTC2, INPUT);
    
    Serial.println("{\"status\": \"initialized\", \"board\": \"XIAO ESP32-C6\"}");
}

void loop() {
    uint32_t currentMillis = millis();
    
    if (currentMillis - lastMillis >= INTERVAL_MS) {
        lastMillis = currentMillis;
        
        float temp1 = readTemperature(PIN_NTC1);
        float temp2 = readTemperature(PIN_NTC2);
        
        // Output JSON formatted data
        Serial.print("{\"t1\": ");
        Serial.print(temp1, 2);
        Serial.print(", \"t2\": ");
        Serial.print(temp2, 2);
        Serial.println("}");
    }
}
