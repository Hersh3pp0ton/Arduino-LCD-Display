#include <LiquidCrystal.h>
#include "DHT.h"

DHT dht(2, DHT11);
LiquidCrystal lcd(4, 5, 6, 7, 8, 9);

int contrasto = 100;
int ritardo = 3000;
String utente = "Giuseppe";
String data = "";
String cpuUsage = "";
String diskUsage = "";
String ramUsage = "";
String gpuTemp = "";

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
  
  analogWrite(3, contrasto);
}

void loop() {
  GetStats();
  PrimaSlide();
  delay(ritardo);
  GetStats();
  SecondaSlide();
  delay(ritardo);
  TerzaSlide();
  GetStats();
  delay(ritardo);
  QuartaSlide(cpuUsage, diskUsage);
  delay(ritardo);
  GetStats();
  QuintaSlide(ramUsage, gpuTemp);
  delay(ritardo);
}

void GetStats() {
  if (Serial.available()) {
    data = Serial.readStringUntil('\n');

    if (data.length() >= 10) {
      cpuUsage = data.substring(0, 6);
      diskUsage = data.substring(6, 11);
      ramUsage = data.substring(11, 17);
      gpuTemp = data.substring(17, data.length());
    } else {
      cpuUsage = "Error";
      diskUsage = "Error";
      ramUsage = "Error";
      gpuTemp = "Error";
    }
  }
}

void PrimaSlide() {
  lcd.clear();
  lcd.createChar(0, smiley);
  lcd.setCursor(0, 0);
  lcd.print("Ciao, ");
  lcd.print(utente);
  lcd.print(" ");
  lcd.write(byte(0));

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  lcd.setCursor(0, 1);
  if (isnan(temperature) || isnan(humidity)) {
    lcd.print("Errore lettura");
  } else if (temperature >= 30) {
    lcd.print("Che caldo...");
  } else if (temperature >= 20) {
    lcd.print("Temperatura OK");
  } else {
    lcd.print("Che freddo! Brrr");
  }
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
  static int secondiTotali = 0;
  static int minutiPassati = 0;
  static int orePassate = 0;

  secondiTotali = millis() / 1000;

  minutiPassati = (secondiTotali / 60) % 60;
  orePassate = secondiTotali / 3600;

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("PC acceso da: ");
  lcd.setCursor(0, 1);

  if (orePassate == 0 && minutiPassati > 0) {
    lcd.print(minutiPassati);
    lcd.print(" min");
  } else if (orePassate > 0) {
    lcd.print(orePassate);
    lcd.print(" h ");
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
  lcd.setCursor(0, 1);
  lcd.print("DISK: ");
  lcd.print(diskUsage);
}

void QuintaSlide(String ramUsage, String gpuTemp) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("RAM:");
  lcd.print(ramUsage);
  lcd.setCursor(0, 1);
  lcd.print("GPU:");
  lcd.print(gpuTemp);
  lcd.print((char)223);
  lcd.print("C");
}
