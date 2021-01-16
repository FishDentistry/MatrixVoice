
#include <ESP8266WiFi.h> // Enables the ESP8266 to connect to the local network (via WiFi)
#include <PubSubClient.h> // Allows us to connect to, and publish to the MQTT broker

const int ledPin = 0; // This code uses the built-in led for visual feedback that a message has been received


const char* ssid = "";
const char* wifi_password = "";

bool blinds_state = false;

int motorpin1 = 12;
int motorpin2 = 13;



const char* mqtt_server = "";
const char* mqtt_topic = "Blinds";
const char* mqtt_username = "";
const char* mqtt_password = "";

const char* clientID = "ESP8266_1";


WiFiClient wifiClient;
PubSubClient client(mqtt_server, 1883, wifiClient); 

void ReceivedMessage(char* topic, byte* payload, unsigned int length) {
  Serial.println("Received");

  if (blinds_state == false) {
    digitalWrite(ledPin, LOW); // Notice for the HUZZAH Pin 0, HIGH is OFF and LOW is ON. Normally it is the other way around.
    digitalWrite(motorpin1, HIGH);
    digitalWrite(motorpin2, LOW);
    delay(1000);
    digitalWrite(motorpin1, LOW);
    digitalWrite(motorpin2, LOW);
    blinds_state = true;
    Serial.println("Opening blinds");
  }
  else{
    digitalWrite(ledPin, HIGH);
    digitalWrite(motorpin1, LOW);
    digitalWrite(motorpin2, HIGH);
    delay(1000);
    digitalWrite(motorpin1, LOW);
    digitalWrite(motorpin2, LOW);
    blinds_state = false;
    Serial.println("Closing blinds");
  }
}

bool Connect() {

  if (client.connect(clientID, mqtt_username, mqtt_password)) {
      client.subscribe(mqtt_topic);
      return true;
    }
    else {
      return false;
  }
}

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(motorpin1, OUTPUT);
  pinMode(motorpin2, OUTPUT);

  // Switch the on-board LED off to start with
  digitalWrite(ledPin, HIGH);
  


  Serial.begin(115200);

  Serial.print("Connecting to ");
  Serial.println(ssid);

  // Connect to the WiFi
  WiFi.begin(ssid, wifi_password);

  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

 
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());


  client.setCallback(ReceivedMessage);
  if (Connect()) {
    Serial.println("Connected Successfully to MQTT Broker!");  
  }
  else {
    Serial.println("Connection Failed!");
  }
}

void loop() {
  // If the connection is lost, try to connect again
  if (!client.connected()) {
    Connect();
  }
  
  client.loop();
  
}
