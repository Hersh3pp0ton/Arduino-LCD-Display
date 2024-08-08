import pyautogui as gui
from time import sleep

def create_token(account_image, continue_image, close_image):
  account_coords = gui.locateOnScreen(account_image, confidence=0.9)
  gui.click(account_coords)
  sleep(1.5)
  continue_coords = gui.locateOnScreen(continue_image, confidence=0.8)
  gui.click(continue_coords)
  sleep(1)
  gui.scroll(-2000)
  sleep(0.5)
  continue_coords = gui.locateOnScreen(continue_image, confidence=0.8)
  gui.click(continue_coords)
  sleep(3)
  close_windows_cords = gui.locateOnScreen(close_image, confidence=0.8)
  gui.click(close_image)

def find_opera(opera_image):
  opera_coords = gui.locateOnScreen(opera_image, confidence = 0.9)
  gui.click(opera_coords)

def main():
  directory = "C:/Users/MSI/OneDrive/Desktop/Arduino LCD Display/Arduino-LCD-Display/AutoTokenImages"

  opera_image = f"{directory}/opera_image.png"
  account_image = f"{directory}/account_image.png"
  continue_image = f"{directory}/continue.png"
  close_image = f"{directory}/close.png"

  errors = 0
  is_opera_open = False

  while True:
    sleep(0.5)

    if errors >= 50:
      break

    if errors >= 10:
      try:
        if not is_opera_open:
          find_opera(opera_image)
          is_opera_open = True
          sleep(0.5)
        create_token(account_image, continue_image, close_image)
        print("Token creato con successo!")
        break
      except Exception as e:
        errors += 1
        print(f"ERRORE (RICERCA DI OPERA): {e}")

    try:
      create_token(account_image, continue_image, close_image)
      print("Token creato con successo!")
      break
    except Exception as e:
      errors += 1
      print(f"ERRORE: {e}")

if __name__ == "__main__":
  main()