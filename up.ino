// Arduino Code for a Single Ultrasonic Sensor (HC-SR04)

const int trigPin = 9;
const int echoPin = 10;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  // Clear the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Set the trigPin to HIGH for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read the echoPin, and return the sound wave travel time in microseconds
  long duration = pulseIn(echoPin, HIGH);

  // Calculate the distance in cm
  // Speed of sound is 343 m/s or 0.0343 cm/µs.
  // Distance = (duration * 0.0343) / 2
  float distance = duration * 0.0343 / 2;

  // Print the distance to the serial monitor
  Serial.println(distance);

  delay(100); // Send ~10 readings per second
}