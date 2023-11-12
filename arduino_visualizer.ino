
#include <NeoPixelBus.h>
#include <WS2812FX.h>
#include <WiFiManager.h>

#if defined(ESP8266)
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#elif defined(ESP32)
#include <WiFi.h>
#else
#error "This is not a ESP8266 or ESP32!"
#endif

#define reset_wifi D0
#define change_modes D2
#define change_static D6
int buttonState = 0;
int modeState = 0;
int colorStatic = 0;
int color_mode = 0;

int mode_rgb_light = 0;
int code_static_color = 0;

int led_seting_firmware = 0;

int led_mode = 0;



#define NUM_LEDS 75
#define BUFFER_LEN 1024
#define PRINT_FPS 1
#define colorSaturation 255


const uint8_t PixelPin = 3;
uint32_t colors[] = {WHITE, BLUE, GREEN, RED, YELLOW, CYAN,  MAGENTA, PURPLE, ORANGE, PINK, GRAY, ULTRAWHITE};
uint32_t modes[] = {12, 2, 7, 11, 15, 32,  33, 46};

RgbColor red(colorSaturation, 0, 0);
RgbColor green(0, colorSaturation, 0);
RgbColor blue(0, 0, colorSaturation);
RgbColor white(colorSaturation);
RgbColor black(0);

HslColor hslRed(red);
HslColor hslGreen(green);
HslColor hslBlue(blue);
HslColor hslWhite(white);
HslColor hslBlack(black);

// Wifi and socket settings
const char* ssid     = "eleVAted.network";
const char* password = "blackcoffee";
unsigned int localPort = 7777;
char packetBuffer[BUFFER_LEN];

uint8_t N = 0;
bool res;
WiFiUDP port;
IPAddress ip(192, 168, 100, 77);
IPAddress gateway(192, 168, 100, 1);
IPAddress subnet(255, 255, 255, 0);
NeoPixelBus<NeoGrbFeature, Neo800KbpsMethod> ledstrip(NUM_LEDS, PixelPin);
WS2812FX ws2812fx = WS2812FX(NUM_LEDS, PixelPin, NEO_RGB + NEO_KHZ800);

void setup() {
    Serial.begin(115200);
    pinMode(reset_wifi, INPUT);
    pinMode(change_modes, INPUT);
    pinMode(change_static, INPUT);
    Serial.println("Awal");
    WiFiManager wifiManager;
    WiFi.mode(WIFI_STA);
    //WiFi.config(ip, gateway, subnet);
//    WiFi.begin(ssid, password);
    Serial.println("satu");
    Serial.println("");
    res = wifiManager.autoConnect("Apex Light Wifi", "apexfuture");
    // Connect to wifi and print the IP address over serial
   
     if(!res) {
        Serial.println("Failed to connect");
        // ESP.restart();
    } 
    if(res) {
        //if you get here you have connected to the WiFi    
        Serial.println("connected...yeey :)");
    }
    
    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    
    port.begin(localPort);
    
    ledstrip.Begin();//Begin output
    ledstrip.Show();//Clear the strip for use


    mode_rgb_light = 2;
    
}

#if PRINT_FPS
    uint16_t fpsCounter = 0;
    uint32_t secondTimer = 0;
#endif

void music_reactive(){ 
    int packetSize = port.parsePacket();
    if (packetSize) {
        int len = port.read(packetBuffer, BUFFER_LEN);
        for(int i = 0; i < len; i+=5) {
            packetBuffer[len] = 0;
            N = ((packetBuffer[i] << 8) + packetBuffer[i + 1]);
            RgbColor pixel((uint8_t)packetBuffer[i+2], (uint8_t)packetBuffer[i+3], (uint8_t)packetBuffer[i+4]);
            ledstrip.SetPixelColor(N, pixel);//N is the pixel number
        } 
        ledstrip.Show();
        #if PRINT_FPS
            fpsCounter++;
            Serial.print("/");
        #endif
    }
    #if PRINT_FPS
        if (millis() - secondTimer >= 1000U) {
            secondTimer = millis();
            Serial.printf("FPS: %d\n", fpsCounter);
            fpsCounter = 0;
        }   
    #endif
}


void rainbow_cycle(){
  ws2812fx.service();
}

void loop() {


    buttonState = digitalRead(reset_wifi);
    if (buttonState == HIGH) {
      WiFiManager wifiManager;
      wifiManager.resetSettings();
      setup();
      Serial.println("Tertekan");
    }

    modeState = digitalRead(change_modes);
    if (modeState == HIGH) {
      mode_rgb_light = mode_rgb_light + 1;
      delay(200);
    }

    colorStatic = digitalRead(change_static);
    if (colorStatic == HIGH && led_mode == 1) {
      code_static_color = code_static_color + 1;
      if(code_static_color == 11){code_static_color = 0;}
      delay(200);
    }
    if (colorStatic == HIGH && led_mode == 2) {
      color_mode = color_mode + 1;
      if(color_mode == 7){color_mode = 0;}
      delay(200);
    }


/////NEOPIXEL LIBRARY///
if(led_seting_firmware == 1){ledstrip.Begin(); ledstrip.Show();  led_seting_firmware = 0;}
/////WS2812BFX///
if(led_seting_firmware == 2){ws2812fx.init();ws2812fx.setBrightness(255);ws2812fx.start();led_seting_firmware = 0;}




if(mode_rgb_light == 1){
  music_reactive();
}

if(mode_rgb_light == 2){
  led_seting_firmware = 2;
  mode_rgb_light = 3;
}

if(mode_rgb_light == 3){
      ws2812fx.setSegment(0, 0, NUM_LEDS-1, FX_MODE_STATIC, colors[code_static_color], 2000);
      ws2812fx.service();
      led_mode = 1;
}

if(mode_rgb_light == 4){
      ws2812fx.setSegment(0, 0, NUM_LEDS-1, modes[color_mode], WHITE, 2000);
      ws2812fx.service();
      led_mode = 2;
}

if(mode_rgb_light == 5){
  led_seting_firmware = 1;
  mode_rgb_light = 1;
}


}