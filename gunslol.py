import requests
import random
import string
import time
from colorama import Fore, init

# démarrer colorama 
init(autoreset=True)

def random_letters(n):
    """Crée une chaîne de lettres aléatoires et de caractères spéciaux."""
    characters = string.ascii_lowercase + string.digits + "._"
    return ''.join(random.choice(characters) for _ in range(n))

def check_user_status(letter_count, interval, save_to_file=True, webhook_url=None):
    """Il contrôle le statut de l'utilisateur avec le nombre de lettres et la plage spécifiée par l'utilisateur."""
    base_url = "guns.lol/"
    while True:
        # Obtenir le nombre de lettres et les informations de plage de contrôle de l'utilisateur 
        random_suffix = random_letters(letter_count)
        url = base_url + random_suffix

        try:
            # 
            response = requests.get(f"https://{url}")

            if "This user is not claimed" in response.text:
                status = f"{Fore.GREEN}unclaimed"
                # 
                if save_to_file:
                    with open("unclaimed.txt", "a") as file:
                        file.write(f"{url}\n")
                # Discord webhook'
                if webhook_url:
                    payload = {"content": f"Unclaimed username found: {url} @everyone"}
                    try:
                        requests.post(webhook_url, json=payload)
                    except Exception as e:
                        print(f"Webhook : {e}")
            else:
                status = f"{Fore.RED}claimed"

            # 
            print(f"URL: {Fore.MAGENTA}{base_url}{random_suffix} - Status: {status}{Fore.RESET}")

        except Exception as e:
            print(f"Error accessing https://{url}: {e}")

        # 
        time.sleep(interval)

# 
try:
    letter_count = int(input("How many letter usernames should be checked? (Example: 5): "))
    if letter_count <= 0:
        print("L'intervalle de secondes doit être un nombre positif.")
    else:
        interval = float(input("Delay (in seconds *recommended 0.1*): "))
        if interval <= 0:
            print("L'intervalle de secondes doit être un nombre positif.")
        else:
            save_to_file = input("Should unclaimed usernames be saved to unclaimed.txt? (Y/N): ").strip().lower() == 'y'
            use_webhook = input("Should unclaimed usernames be sent to a Discord webhook? (Y/N): ").strip().lower()
            webhook_url = None
            if use_webhook == 'y':
                webhook_url = input("Enter your Discord webhook URL: ").strip()

            # Veuillez entrer un numéro valide 
            check_user_status(letter_count, interval, save_to_file, webhook_url)
except ValueError:
    print("Veuillez entrer un numéro valide .")
