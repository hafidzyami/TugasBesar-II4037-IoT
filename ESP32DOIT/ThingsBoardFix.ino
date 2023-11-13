#include <WiFi.h>
#include <ThingsBoard.h>
#include <Arduino_MQTT_Client.h>

#define WIFI_AP "Perdotaan"
#define WIFI_PASSWORD "yogathedog"
#define TOKEN "b1voedr3m46rl5gz09l6"

const int dry = 4096;
const int wet = 0;

char thingsboardServer[] = "34.101.235.1";

WiFiClient wifiClient;
Arduino_MQTT_Client mqttClient(wifiClient);
ThingsBoard tb(mqttClient);

int status = WL_IDLE_STATUS;
unsigned long lastSend;

void InitWiFi()
{
  Serial.println("Connecting to AP ...");
  // attempt to connect to WiFi network

  WiFi.begin(WIFI_AP, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to AP");
}


void reconnect() {
  // Loop until we're reconnected
  while (!tb.connected()) {
    status = WiFi.status();
    if ( status != WL_CONNECTED) {
      WiFi.begin(WIFI_AP, WIFI_PASSWORD);
      while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
      }
      Serial.println("Connected to AP");
    }
    Serial.print("Connecting to ThingsBoard node ...");
    if ( tb.connect(thingsboardServer, TOKEN) ) {
      Serial.println( "[DONE]" );
    } else {
      Serial.print( "[FAILED]" );
      Serial.println( " : retrying in 5 seconds]" );
      // Wait 5 seconds before retrying
      delay( 5000 );
    }
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(10);
  InitWiFi();
  lastSend = 0;
}

void loop() {

  if ( !tb.connected() ) {
    reconnect();
  }
  // put your main code here, to run repeatedly:
  
  if(millis() - lastSend > 1000){
    int value = analogRead(32);
    int percentageHumidity = map(value, wet, dry, 100, 0);
    Serial.print(percentageHumidity);
    Serial.println("%");
    tb.sendTelemetryData("Humidity", percentageHumidity);
    lastSend = millis();
  }

  tb.loop();
}
