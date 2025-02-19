String x;
void setup() {
 Serial.begin(115200);
 Serial.setTimeout(10);
}
void loop() {
 while (!Serial.available());
 x = Serial.readString();
 x.trim();
 if (x.startsWith("V")){
 Serial.print("Trying to Open Valve");
 } else if (x == "notthis") {
 Serial.print("no");
 }
 
}