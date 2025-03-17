void setup() {
    // Initialize serial communication at 9600 bits per second
    Serial.begin(9600);  
    // Set the built-in LED pin (usually pin 13) as an output
    pinMode(LED_BUILTIN, OUTPUT);  
}

void loop() {
    // Check if data is available to read from the serial port
    if (Serial.available() > 0) {  
        // Read an integer from the serial input
        int num = Serial.parseInt();  

        // Check if the received number is greater than 0
        if (num > 0) {
            // Blink the LED 'num' times
            for (int i = 0; i < num; i++) {
                digitalWrite(LED_BUILTIN, HIGH);  // Turn the LED on
                delay(1000);                     // Wait for 1 second
                digitalWrite(LED_BUILTIN, LOW);   // Turn the LED off
                delay(1000);                     // Wait for 1 second
            }

            // Generate a random number between 2 and 5 (inclusive)
            int r = random(2, 6); 
            // Send the generated random number back to the serial port
            Serial.println(r);  
        }
        // Short delay to avoid overwhelming the serial port
        delay(100);
    }
}
