const int trigger = 9;
const int echo = 10;

int getUltrasonicDistance() {
    long duration;
    int distance;
    digitalWrite(trigger, LOW);
    delayMicroseconds(5);
    digitalWrite(trigger, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigger, LOW);

    duration = pulseIn(echo, HIGH);
    distance = duration * 0.034 / 2; 
    return distance;
}
void setup() {
    pinMode(trigger, OUTPUT);
    pinMode(echo, INPUT);

    Serial.begin(9600);
}

void loop() {
    int distance = getUltrasonicDistance(); 
}