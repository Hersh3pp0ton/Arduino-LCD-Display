import psutil
import time
import serial
import subprocess

port = 'COM3'           # Arduino port
baud_rate = 9600        # bit/s of Arduino port (COM3)

try:
    ser = serial.Serial(port, baud_rate, timeout=1)         # tries to connect to COM3 ...
except serial.SerialException as e:
    print(f"Errore nell'aprire la porta seriale: {e}")      # ... else it'll get an error
    exit()

print(f"Connessione stabilita su {port}")                   # connection ready!

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

            data = f"{cpu_usage}%  {disk_usage}%  {ram_usage}% {gpu_temp}\n"
            ser.write(data.encode())
            print(f"Inviato: {data.strip()}")               # sends the data to the COM3 (Arduino)

            time.sleep(5)                                   # waits 5 seconds
        except serial.SerialException as e:
            print(f"Errore durante la comunicazione seriale: {e}")
            break
finally:
    ser.close()
    print(f"Porta seriale {port} chiusa")
