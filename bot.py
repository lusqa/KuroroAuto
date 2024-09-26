import time
import requests
import os
import signal
import traceback
from colorama import Fore, Style, init
from datetime import datetime

# Initialize colorama for color output
init(autoreset=True)

# Global variable to control the main loop
running = True

def signal_handler(signum, frame):
    global running
    running = False
    print(Fore.LIGHTBLACK_EX + f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
          Fore.YELLOW + "Received interrupt signal. Preparing to exit...")

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def art(total_accounts):
    print(Fore.GREEN + Style.BRIGHT + r"""

   ░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓████▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓███████▓▒░ ░▒▓██████▓▒░  
   ░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     
   ░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     
   ░▒▓█▓▒░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     
                   
    Auto Claim Bot For Kuroro - Lucky, O Foda
    Author  : Lucas Gomes
    Github: 
    """ + Style.RESET_ALL)
    
    print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Total accounts: {total_accounts}")
    print(Fore.YELLOW + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def read_data_file(file_path):
    accounts = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            encoded_data = line.strip()
            if encoded_data:
                accounts.append(encoded_data)
    return accounts

def player_state(bearer):
    url = "https://ranch-api.kuroro.com/api/Game/GetPlayerState"
    headers = {
        "authorization": "Bearer " + bearer,
        "referrer": "https://ranch.kuroro.com/",
    }

    try:
        response = requests.get(
            url=url,
            headers=headers,
            timeout=20,
        )
        data = response.json()
        energy = data["energySnapshot"]["value"]
        shards = data["shards"]
        
        print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
                Fore.GREEN + f"Energy: " + Fore.WHITE + f"{energy} | " + 
                Fore.GREEN + f"Shards: " + Fore.WHITE + f"{shards}")
        
        return energy, shards
    except Exception as e:
        print(f"{Fore.WHITE}Error mining: {e}")
        traceback.print_exc()
        return None 

def mine(energy, bearer):
    url = "https://ranch-api.kuroro.com/api/Clicks/MiningAndFeeding"
    headers = {
        "authorization": "Bearer " + bearer,
        "referrer": "https://ranch.kuroro.com/",
    }

    energy_remaining = energy
    while energy_remaining > 0:
        payload = {"feedAmount":0,"mineAmount":1}

        try:
            requests.post(
                url=url,
                headers=headers,
                json=payload,
                timeout=20,
            )
            print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
                    Fore.GREEN + f"Mined: " + Fore.WHITE + f"{energy - energy_remaining} | " + 
                    Fore.GREEN + f"Energy remaining: " + Fore.WHITE + f"{energy_remaining}")
            energy_remaining = energy_remaining - 1
        except Exception as e:
            print(f"{Fore.WHITE}Error mining: {e}")
            traceback.print_exc()
            return None
    
    return energy

def feed(shards, bearer):
    url = "https://ranch-api.kuroro.com/api/Clicks/MiningAndFeeding"
    headers = {
        "authorization": "Bearer " + bearer,
        "referrer": "https://ranch.kuroro.com/",
    }

    shards_remaining = shards
    while shards_remaining > 0:
        payload = { "feedAmount": 1, "mineAmount": 0 }

        try:
            requests.post(
                url=url,
                headers=headers,
                json=payload,
                timeout=20,
            )
            print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
                    Fore.GREEN + f"Feeded: " + Fore.WHITE + f"{shards - shards_remaining} | " + 
                    Fore.GREEN + f"Shards remaining: " + Fore.WHITE + f"{shards_remaining}")
            shards_remaining = shards_remaining - 1
        except Exception as e:
            print(f"{Fore.WHITE}Error feeding: {e}")
            traceback.print_exc()
            return None

def main():
    global running
    file_path = "data.txt"
    encoded_data_list = read_data_file(file_path)
    total_accounts = len(encoded_data_list)
    
    try:
        while running:
            clear_terminal()
            art(total_accounts)
        
            for index, encoded_data in enumerate(encoded_data_list, start=1):
                if not running:
                    break
                print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
                      Fore.GREEN + f"Processing Account No.{index}")
                try:
                    energy, shards = player_state(encoded_data)
                    new_shards = mine(energy, encoded_data)
                    feed(shards + new_shards, encoded_data)
                except Exception as e:
                    print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
                          Fore.RED + f"Error processing account {index}: {str(e)}")
            
            if running:
                timeout = 60 * 30
                print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
                      Fore.YELLOW + f"Waiting for {timeout / 60} minutes before next cycle...")
                for _ in range(timeout):
                    if not running:
                        break
                    time.sleep(1)
    except Exception as e:
        print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
              Fore.RED + f"An unexpected error occurred: {str(e)}")
    finally:
        print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
              Fore.GREEN + "Successfully logged out from bot. Goodbye!")

if __name__ == "__main__":
    main()
