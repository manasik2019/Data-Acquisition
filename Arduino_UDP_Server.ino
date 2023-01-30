#include <math.h>
#include <Ethernet.h> //Load Ethernet Library
#include <EthernetUdp.h> //Load the Udp Library
#include <SPI.h> //Load SPI Library 
#include "Wire.h" //imports the wire library

const int B = 4275;               // B value of the thermistor
const int R0 = 10000;             // R0 = 100k
const int pinTempSensor = A0;     // Grove - 1st Temperature Sensor connect to A0
const int pinTempSensor2 = A3;    // Grove - 2nd Temperature Sensor connect to A3


byte mac[] = { 0x90, 0xA2, 0xDA, 0x10, 0xBF, 0xB7}; //Assign mac address
IPAddress ip(192, 168, 10, 2); //Assign the IP Adress
unsigned int localPort = 5000; // Assign a port to talk over
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //dimensian a char array to hold our data packet
String datReq; //String for our data
int packetSize; //Size of the packet
EthernetUDP Udp; // Create a UDP Object

#if defined(ARDUINO_ARCH_AVR)
#define debug  Serial
#elif defined(ARDUINO_ARCH_SAMD) ||  defined(ARDUINO_ARCH_SAM)
#define debug  SerialUSB
#else
#define debug  Serial
#endif

void setup() {
  Serial.begin(9600); //Initialize Serial Port
  Ethernet.begin( mac, ip); //Inialize the Ethernet
  Udp.begin(localPort); //Initialize Udp
  delay(1500); //delay
}

void loop() {
  packetSize = Udp.parsePacket(); //Reads the packet size
  
  if (packetSize > 0) { //if packetSize is >0, that means someone has sent a request
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE); //Read the data request
    String datReq(packetBuffer); //Convert char array packetBuffer into a string called datReq

    if (datReq == "Temperature1") { //Do the following if Temperature1 is requested
      int a = analogRead(pinTempSensor);
      float R = 1023.0 / a - 1.0;
      R = R0 * R;
      float temperature1 = 1.0 / (log(R / R0) / B + 1 / 298.15) - 273.15; // convert to temperature via datasheet
      Serial.print("temperature = ");
      Serial.println(temperature1);
      delay(100);
      Udp.beginPacket(Udp.remoteIP(), Udp.remotePort()); //Initialize packet send
      Udp.print(temperature1); //Send the temperature data
      Udp.endPacket(); //End the packet
    }

  if (datReq == "Temperature2") { //Do the following if Temperature2 is requested
      int b = analogRead(pinTempSensor2);
      float R1 = 1023.0 / b - 1.0;
      R1 = R0 * R1;
      float temperature2 = 1.0 / (log(R1 / R0) / B + 1 / 298.15) - 273.15; // convert to temperature via datasheet
      Serial.print("temperature = ");
      Serial.println(temperature2);
      delay(100);
      Udp.beginPacket(Udp.remoteIP(), Udp.remotePort()); //Initialize packet send
      Udp.print(temperature2); //Send the temperature data
      Udp.endPacket(); //End the packet
    }
  }
  memset(packetBuffer, 0, UDP_TX_PACKET_MAX_SIZE); //clear out the packetBuffer array
}
