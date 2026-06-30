#include <SPI.h>
#include <LoRa.h>

// --- Config: SX1276/78 Pins (Common for TTGO/ESP32-LoRa) ---
#define SCK 5
#define MISO 19
#define MOSI 27
#define SS 18
#define RST 14
#define DIO0 26

// --- Config: Frequency ---
// India/EU use 866E6 (866 MHz)
#define BAND 866E6

// --- Config: Sensor ---
#define SENSOR_PIN 34 // Analog Pin (Check your board!)
#define AIR_VALUE 3500 // Capacitive: Dry
#define WATER_VALUE 1800 // Capacitive: Wet

// --- Config: Deep Sleep ---
#define uS_TO_S_FACTOR 1000000ULL
#define TIME_TO_SLEEP 3600 // Sleep for 1 hour (3600s) - Set to 10s for testing

void setup() {
  Serial.begin(115200);

  // Power Sensor only during read (optional: if using a transistor switch)
  // pinMode(SENSOR_POWER_PIN, OUTPUT);

  // --- LoRa Init ---
  SPI.begin(SCK, MISO, MOSI, SS);
  LoRa.setPins(SS, RST, DIO0);

  if (!LoRa.begin(BAND)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }

  // Maximize Power for Underground TX
  LoRa.setTxPower(20); // 20dBm is max for SX1276
  LoRa.setSpreadingFactor(12); // SF12 = Max Range (Slowest)
  LoRa.setSignalBandwidth(125E3);

  // --- Read Sensor ---
  int rawValue = analogRead(SENSOR_PIN);
  int percent = map(rawValue, AIR_VALUE, WATER_VALUE, 0, 100);
  percent = constrain(percent, 0, 100);

  // --- Send Packet ---
  Serial.print("Sending Moisture: ");
  Serial.println(percent);

  LoRa.beginPacket();
  LoRa.print("NODE_01:");
  LoRa.print(percent);
  LoRa.endPacket();

  // --- Go to Deep Sleep ---
  // Ensure LoRa is in sleep mode
  LoRa.sleep();

  // Configure ESP32 Sleep
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  Serial.println("Sleeping...");
  Serial.flush();
  esp_deep_sleep_start();
}

void loop() {
  // Never reached
}
