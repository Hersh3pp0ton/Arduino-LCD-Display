import psutil
import time
import serial
import subprocess
import requests

city_name = ""
api_key = ""
link = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

port = 'COM3'           # Arduino port
baud_rate = 9600        # bit/s of Arduino port (COM3)

weather_translation = {     # italian translations
    "clear sky": "Cielo sereno",
    "few clouds": "Poche nuvole",
    "scattered clouds": "Nuvole sparse",
    "broken clouds": "Nuvole sparse",
    "shower rain": "Pioggia leggera",
    "rain": "Pioggia",
    "thunderstorm": "Temporale",
    "snow": "Neve",
    "mist": "Nebbia"
}

try:
    ser = serial.Serial(port, baud_rate, timeout=1)         # tries to connect to COM3 ...
except serial.SerialException as e:
    print(f"Errore nell'aprire la porta seriale: {e}")      # ... else it'll get an error
    exit()

print(f"Connessione stabilita su {port}")                   # connection ready!

def get_weather():
    try:
        print(f"Richiesta meteo all'URL: {link}")  # Debug: shows the URL
        response = requests.get(link)
        response.raise_for_status()  # wrong HTTPS
        print(f"Risposta API: {response.text}")  # Debug: shows response text
        weather_data = response.json()
        description = weather_data['weather'][0]['description']
        return weather_translation.get(description)
    except requests.RequestException as e:
        print(f"Errore nella richiesta delle informazioni meteo: {e}")
        return "N/A"  # standard return for errors

try:
    while True:
        try:
            cpu_usage = psutil.cpu_percent(interval=1)      # CPU usage (in percentual)
            disk_usage = psutil.disk_usage('/').percent     # disk (C:/) remaining memory (in percentual)
            ram_usage = psutil.virtual_memory().percent     # RAM memory (in percentual)
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader'], 
                stdout=subprocess.PIPE,                     # "saves" the output
                creationflags=subprocess.CREATE_NO_WINDOW   # doesn't create a new CMD window (every N seconds)
            )
            gpu_temp = result.stdout.decode('utf-8').strip()

            weather_description = get_weather()

            data = f"{cpu_usage},{disk_usage},{ram_usage},{gpu_temp},{weather_description}\n"
            ser.write(data.encode())
            print(f"Inviato: {data.strip()}")               # sends the data to the COM3 (Arduino)

            time.sleep(5)                                   # waits 5 seconds
        except serial.SerialException as e:
            print(f"Errore durante la comunicazione seriale: {e}")
            break
finally:
    ser.close()
    print(f"Porta seriale {port} chiusa")