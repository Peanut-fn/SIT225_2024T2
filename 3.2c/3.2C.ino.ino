#include "thingProperties.h"
#include <Arduino_LSM6DS3.h> // Include the correct library

void setup() {
  Serial.begin(9600);
  delay(1500);

  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);

  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.println("Setup complete, starting sensor readings...");
}

void loop() {
  ArduinoCloud.update(); // Update IoT Cloud variables

  // Read accelerometer values
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(accel_x, accel_y, accel_z);
  }

  // Print values to Serial Monitor
  Serial.print("X: ");
  Serial.print(accel_x);
  Serial.print("  Y: ");
  Serial.print(accel_y);
  Serial.print("  Z: ");
  Serial.println(accel_z);

  // Check for alarm condition (Example: If movement is too high)
  if (abs(accel_x) > 2.5 || abs(accel_y) > 2.5 || abs(accel_z) > 2.5) {
    alarm_status = true;  // Trigger alarm
    Serial.println("🚨 Alarm triggered! 🚨");
  } else {
    alarm_status = false;
  }

  delay(500);
}

/*
  Since alarm_status is a READ_WRITE variable, this function
  is executed every time a new value is received from IoT Cloud.
*/
void onAlarmStatusChange() {
  Serial.print("Alarm Status Changed: ");
  Serial.println(alarm_status ? "ON" : "OFF");
}