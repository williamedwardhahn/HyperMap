#include <WiFi.h>
#include <FS.h>
#include <SPIFFS.h>
#include <WebServer.h>

// Replace with your network credentials
const char* ssid = "";
const char* password = "";

WebServer server(80);

void setup(void) {
  Serial.begin(115200);

  if (!SPIFFS.begin(true)) {
    Serial.println("An error has occurred while mounting SPIFFS");
    return;
  }

  // Check if index.html exists, if not create it
  if (!SPIFFS.exists("/index.html")) {
    File file = SPIFFS.open("/index.html", FILE_WRITE);
    if (!file) {
      Serial.println("There was an error opening the file for writing");
      return;
    }

    // Content of the default index.html file
    String html = "<h1>Welcome to ESP32!</h1>";
    if (file.print(html)) {
      Serial.println("File was written");
    } else {
      Serial.println("File write failed");
    }

    file.close();
  }

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println(WiFi.localIP());

  // Route for root / web page
  server.on("/", HTTP_GET, [](){
    File file = SPIFFS.open("/index.html", "r");
    server.streamFile(file, "text/html");
    file.close();
  });

  // Route for update page
  server.on("/update", HTTP_GET, [](){
    File file = SPIFFS.open("/index.html", "r");
    String html = "<form method='POST' action='/update'><textarea name='content' rows='30' cols='80'>" + file.readString() + "</textarea><input type='submit' value='Update'></form>";
    server.send(200, "text/html", html);
    file.close();
  });

  // handle update
  server.on("/update", HTTP_POST, []() {
    if (server.hasArg("content")) {
      SPIFFS.remove("/index.html");
      File file = SPIFFS.open("/index.html", "w");
      if (file.print(server.arg("content"))) {
        Serial.println("File was updated");
        server.send(200, "text/plain", "File was updated");
      } else {
        Serial.println("File update failed");
        server.send(500, "text/plain", "File update failed");
      }
      file.close();
    } else {
      server.send(500, "text/plain", "Bad arguments");
    }
  });

  server.begin();
}

void loop(void) {
  server.handleClient();
}
