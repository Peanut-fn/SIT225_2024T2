void setup() {
    Serial.begin(9600);  
    pinMode(LED_BUILTIN, OUTPUT);  
}

void loop() {
    if (Serial.available() > 0) {  
        int num = Serial.parseInt();  

        if (num > 0) {
            for (int i = 0; i < num; i++) {
                digitalWrite(LED_BUILTIN, HIGH);
                delay(1000);
                digitalWrite(LED_BUILTIN, LOW);
                delay(1000);
            }

            int r = random(2, 6); 
            Serial.println(r);  
        }
        delay(100);
    }
}