#include <WiFi.h>
#include <ESPAsyncWebServer.h>

const char* ssid = "";
const char* password = "";

AsyncWebServer server(80);

const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML><html>
<body>
  <button onclick="location.href='/led/on'">Turn LED ON</button><br>
  <button onclick="location.href='/led/off'">Turn LED OFF</button><br>
</body>
</html>
)rawliteral";

void setup() {
  // Serial port for debugging purposes
  Serial.begin(115200);
  
  pinMode(4, OUTPUT);
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println(WiFi.localIP());

  // Route for root / web page
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/html", index_html);
  });

  // Route to set GPIO to HIGH
  server.on("/led/on", HTTP_GET, [](AsyncWebServerRequest *request){
    digitalWrite(4, HIGH);   
    request->send_P(200, "text/plain", "LED is ON");
  });

  // Route to set GPIO to LOW
  server.on("/led/off", HTTP_GET, [](AsyncWebServerRequest *request){
    digitalWrite(4, LOW); 
    request->send_P(200, "text/plain", "LED is OFF");
  });

  // Start server
  server.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
}
