import psutil
import time
import serial
import subprocess
import requests
import ezgmail
import datetime
import os

ezgmail.init(tokenFile='token.json', credentialsFile='C:/Users/MSI/OneDrive/Desktop/Arduino LCD Display/Arduino-LCD-Display/credentials.json')
    recipient="eppesuig08@gmail.com",
def delete_token():
    try:
        os.remove('C:/Users/MSI/OneDrive/Desktop/Arduino LCD Display/Arduino-LCD-Display/token.json')
    except:
        print("Non è stato trovato il file 'token.json'.")

def initialize_email():
    try:
    except Exception as e:
        print(f"Errore nell'inizializzazione di ezgmail: {e}")
        os.remove('token.json')
        exit()

def send_email_notification():
    try:
        now = datetime.datetime.now()
        ezgmail.send(
            subject="Il tuo PC è stato acceso",
            body=f"Il tuo PC è stato appena acceso: {now.day}/{now.month}/{now.year} - {now.hour}:{now.minute}"
        )
        print("Email inviata correttamente")
    except Exception as e:
        print(f"Errore nell'invio dell'email: {e}")

def get_weather(api_key, city_name):
    link = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    weather_translation = {
        "clear sky": "Cielo sereno",
        "few clouds": "Poche nuvole",
        "scattered clouds": "Nuvole sparse",
        "broken clouds": "Nuvole sparse",
        "shower rain": "Pioggia leggera",
        "moderate rain": "Pioggia Moderata",
        "rain": "Pioggia",
        "thunderstorm": "Temporale",
        "snow": "Neve",
        "mist": "Nebbia"
    }

    try:
        print(f"Richiesta meteo all'URL: {link}")  # Debug: shows the URL
        response = requests.get(link)
        response.raise_for_status()
        print(f"Risposta API: {response.text}")  # Debug: shows response text
        weather_data = response.json()
        description = weather_data['weather'][0]['description']
        return weather_translation.get(description, "Descrizione non disponibile")
    except requests.RequestException as e:
        print(f"Errore nella richiesta delle informazioni meteo: {e}")
        return "N/A"

def get_gpu_temperature():
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader'],
            stdout=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return result.stdout.decode('utf-8').strip()
    except subprocess.SubprocessError as e:
        print(f"Errore nel recupero della temperatura della GPU: {e}")
        return "N/A"

def main():
    try:
        initialize_email()
    except:
        delete_token()
        initialize_email()

    send_email_notification()

    port = 'COM3'
    baud_rate = 9600

    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"Connessione stabilita su {port}")
    except serial.SerialException as e:
        print(f"Errore nell'aprire la porta seriale: {e}")
        exit()

    try:
        while True:
            try:
                cpu_usage = psutil.cpu_percent(interval=1)
                disk_usage = psutil.disk_usage('/').percent
                ram_usage = psutil.virtual_memory().percent
                gpu_temp = get_gpu_temperature()
                weather_description = get_weather(api_key, city_name)

                data = f"{cpu_usage},{disk_usage},{ram_usage},{gpu_temp},{weather_description}\n"
                ser.write(data.encode())
                print(f"Inviato: {data.strip()}")

                time.sleep(5)
            except serial.SerialException as e:
                print(f"Errore durante la comunicazione seriale: {e}")
                break
    finally:
        ser.close()
        print(f"Porta seriale {port} chiusa")

if __name__ == "__main__":
    main()