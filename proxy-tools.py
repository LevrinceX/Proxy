import requests
import os
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor

RESULTS_FILE = "active-proxy.txt"

def check_proxy(proxy, proxy_type):
    try:
        if proxy_type == "http":
            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}",
            }
        else:
            proxies = {
                "http": f"{proxy_type}://{proxy}",
                "https": f"{proxy_type}://{proxy}",
            }

        response = requests.get("https://www.google.com", proxies=proxies, timeout=5)
        if response.status_code == 200:
            with open(RESULTS_FILE, "a") as live_file:
                live_file.write(proxy + "\n")
            print(Fore.GREEN + f"[ {proxy} ({proxy_type}) >> Live ]" + Style.RESET_ALL)
            return
    except Exception as e:
        pass
    print(Fore.RED + f"[ {proxy} ({proxy_type}) >> Dead ]" + Style.RESET_ALL)

def proxy_checker():
    if os.path.exists(RESULTS_FILE):
        os.remove(RESULTS_FILE)

    print("""
    ____                                  __              __            
   / __ \_________  _  ____  __     _____/ /_  ___  _____/ /_____  _____
  / /_/ / ___/ __ \| |/_/ / / /    / ___/ __ \/ _ \/ ___/ //_/ _ \/ ___/
 / ____/ /  / /_/ />  </ /_/ /    / /__/ / / /  __/ /__/ ,< /  __/ /    
/_/   /_/   \____/_/|_|\__, /     \___/_/ /_/\___/\___/_/|_|\___/_/     
                      /____/    
                      
            — coded by NowMeee [ 2023-11-07 ]
    """)
    list_file = input("Input list: ")
    thread_count = int(input("Thread: "))

    with open(list_file, "r") as file:
        proxies = file.read().splitlines()

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for proxy in proxies:
            for proxy_type in ["http", "https", "socks4", "socks5"]:
                executor.submit(check_proxy, proxy, proxy_type)

def get_proxies(api_key):
    url = "https://v1.nomisec07.site/api/v2/proxy?apikey=" + api_key
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        proxies = data.get("proxies", [])
        return proxies
    else:
        print("Gagal mengambil data dari API")
        return []

def proxy_grabber():
    print("""
 _____                                       _     _               
 |  __ \                                     | |   | |              
 | |__) | __ _____  ___   _    __ _ _ __ __ _| |__ | |__   ___ _ __ 
 |  ___/ '__/ _ \ \/ / | | |  / _` | '__/ _` | '_ \| '_ \ / _ \ '__|
 | |   | | | (_) >  <| |_| | | (_| | | | (_| | |_) | |_) |  __/ |   
 |_|   |_|  \___/_/\_\\__, |  \__, |_|  \__,_|_.__/|_.__/ \___|_|   
                       __/ |   __/ |                                
                      |___/   |___/     
                      
                   — coded by NowMeee
  """)
    api_key = input("Masukkan API Key: ")

    proxies = get_proxies(api_key)
    if proxies:
        with open("grabbed-proxies.txt", "w") as file:
            for proxy in proxies:
                ip, port = proxy.split(":")
                file.write(f"{ip}:{port}\n")
                print(f"{Fore.YELLOW}{ip}:{port}{Style.RESET_ALL}")

def main_menu():
    while True:
        print("""
 ██████╗ ██╗  ██╗██╗███████╗
██╔═══██╗╚██╗██╔╝██║██╔════╝
██║   ██║ ╚███╔╝ ██║█████╗  
██║   ██║ ██╔██╗ ██║██╔══╝  
╚██████╔╝██╔╝ ██╗██║███████╗
 ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝
    — coded by NowMeee
        """)
        print("[1] — Proxy grabber >> update new proxy after 10 sec")
        print("[2] — Proxy checker >> using proxy list file")
        print("[3] — Keluar")

        choice = input("Choose: ")

        if choice == "1":
            proxy_grabber()
        elif choice == "2":
            proxy_checker()
        elif choice == "3":
            break
        else:
            print("Pilihan tidak valid. Silakan pilih lagi.")

if __name__ == "__main__":
    main_menu()
