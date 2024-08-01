#include <LiquidCrystal.h>
#include "DHT.h"
//#include "IRremote.h"

DHT dht(2, DHT11);
LiquidCrystal lcd(4, 5, 6, 7, 8, 9);

int contrast = 100;
String utente = "";
String data = "N/A";
String cpuUsage = "N/A";
String diskUsage = "N/A";
String ramUsage = "N/A";
String gpuTemp = "N/A";
String weatherDesc = "N/A";

unsigned long previousMillis = 0;
const long interval = 3000;
int slideIndex = 0;

/*
int receiverPin = 1;
IRrecv irrecv(receiverPin);
decode_results results;
*/

byte smiley[8] = {
  B00000,
  B10001,
  B00000,
  B00000,
  B10001,
  B01110,
  B00000,
};

void setup() {
  Serial.begin(9600);
  dht.begin();
  lcd.begin(16, 2);
  
  //irrecv.enableIRIn();
  analogWrite(3, contrast);
  lcd.createChar(0, smiley);
}

void loop() {
  if (millis() - previousMillis >= interval) {
    previousMillis = millis();
    GetStats();

    switch(slideIndex) {
      case 0:
        PrimaSlide();
        break;
      case 1:
        SecondaSlide();
        break;
      case 2:
        TerzaSlide();
        break;
      case 3:
        QuartaSlide(cpuUsage, diskUsage);
        break;
      case 4:
        QuintaSlide(ramUsage, gpuTemp);
        break;
    }

    slideIndex = (slideIndex + 1) % 5;
  }
  /*

  if (irrecv.decode(&results)) {
    TranslateIR();
    irrecv.resume();
  }
  */
}
/*
void TranslateIR() {
  switch(results.value) {
    case 0xFF629D:  // VOL+
      contrasto += 10;
      if (contrasto > 255) contrasto = 255;
      analogWrite(3, contrasto);
      break;
    case 0xFFA857:  // VOL-
      contrasto -= 10;
      if (contrasto < 0) contrasto = 0;
      analogWrite(3, contrasto);
      break;
  }

  delay(100);
}
*/

void GetStats() {
  if (Serial.available()) {
    data = Serial.readStringUntil('\n');

    if (data.length() > 1) {
      ParseData(data);
    } else {
      cpuUsage = "Error";
      diskUsage = "Error";
      ramUsage = "Error";
      gpuTemp = "Error";
    }
  }
}

void ParseData(String str) {
  int indexCpuUsage = str.indexOf(",");
  cpuUsage = str.substring(0, indexCpuUsage);
  int indexDiskUsage = str.indexOf(",", indexCpuUsage + 1);
  diskUsage = str.substring(indexCpuUsage + 1, indexDiskUsage);
  int indexRamUsage = str.indexOf(",", indexDiskUsage + 1);
  ramUsage = str.substring(indexDiskUsage + 1, indexRamUsage);
  int indexGpuTemp = str.indexOf(",", indexRamUsage + 1);
  gpuTemp = str.substring(indexRamUsage + 1, indexGpuTemp);
  int indexweatherDesc = str.indexOf("\n", indexGpuTemp + 1);
  weatherDesc = str.substring(indexGpuTemp + 1, indexweatherDesc);
}

void PrimaSlide() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Ciao, ");
  lcd.print(utente);
  lcd.print(" ");
  lcd.write(byte(0));

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  lcd.setCursor(0, 1);
  lcd.print(weatherDesc);
}

void SecondaSlide() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Temp.: ");
  lcd.print(temperature);
  lcd.print((char)223);
  lcd.print("C");
  lcd.setCursor(0, 1);
  lcd.print("Umid.: ");
  lcd.print(humidity);
  lcd.print("%");
}

void TerzaSlide() {
  static unsigned long previousMillis = 0;  // Variabile per il tempo corrente
  static int secondiTotali = 0;
  static int minutiPassati = 0;
  static int orePassate = 0;

  unsigned long currentMillis = millis();
  secondiTotali = (currentMillis - previousMillis) / 1000;
  minutiPassati = (secondiTotali / 60) % 60;
  orePassate = secondiTotali / 3600;

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("PC acceso da: ");
  lcd.setCursor(0, 1);

  if (orePassate > 0) {
    lcd.print(orePassate);
    lcd.print(" h ");
    lcd.print(minutiPassati);
    lcd.print(" min");
  } else if (minutiPassati > 0) {
    lcd.print(minutiPassati);
    lcd.print(" min");
  } else {
    lcd.print(secondiTotali % 60);
    lcd.print(" s");
  }
}

void QuartaSlide(String cpuUsage, String diskUsage) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("CPU: ");
  lcd.print(cpuUsage);
  lcd.print("%");

  lcd.setCursor(0, 1);
  lcd.print("DISK: ");
  lcd.print(diskUsage);
  lcd.print("%");
}

void QuintaSlide(String ramUsage, String gpuTemp) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("RAM: ");
  lcd.print(ramUsage);
  lcd.print("%");

  lcd.setCursor(0, 1);
  lcd.print("GPU: ");
  lcd.print(gpuTemp);
  lcd.print((char)223);
  lcd.print("C");
}
