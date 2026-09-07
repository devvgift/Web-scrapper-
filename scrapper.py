#!/usr/bin/env python3

import os
import sys
import time
import json
import subprocess
import requests
from urllib.parse import urlparse, urljoin
from colorama import init, Fore, Back, Style
import threading

init(autoreset=True)

RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
PURPLE = Fore.MAGENTA
CYAN = Fore.CYAN
WHITE = Fore.WHITE
NC = Fore.RESET
BOLD = Style.BRIGHT
BLINK = '\033[5m'

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    clear()
    print(f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║     ██████  ███████ ██    ██  ██████  ██ ███████                  ║
║     ██   ██ ██      ██    ██ ██       ██ ██                       ║
║     ██   ██ █████   ██    ██ ██   ███ ██ █████                    ║
║     ██   ██ ██       ██  ██  ██    ██ ██ ██                       ║
║     ██████  ███████   ████    ██████  ██ ██                       ║
║                                                                   ║
║          ███████  ██████ ██████  █████  ██████  ███████           ║
║          ██      ██      ██   ██ ██   ██ ██   ██ ██              ║
║          ███████ ██      ██████  ███████ ██████  █████            ║
║               ██ ██      ██   ██ ██   ██ ██      ██              ║
║          ███████  ██████ ██   ██ ██   ██ ██      ███████         ║
║                                                                   ║
║              {YELLOW}🔥 DEV GIFT SCRAPER {RED}{BLINK}●{NC}{CYAN}🔥                          ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{NC}""")

    print(f"""{YELLOW}┌───────────────────────────────────────────────────────────────────┐
│{NC}  {BOLD}DEVELOPER:{NC} Dev Gift                                    {YELLOW}│
│{NC}  {BOLD}TOOL:{NC} Website Scraper v6.0                            {YELLOW}│
│{NC}  {BOLD}GITHUB:{NC} github.com/devvgift                           {YELLOW}│
│{NC}  {BOLD}CONTACT:{NC} 2349164624021                                {YELLOW}│
│{NC}  {BOLD}STATUS:{NC} {GREEN}● READY{NC}                                      {YELLOW}│
{YELLOW}└───────────────────────────────────────────────────────────────────┘{NC}
""")

def spinner():
    chars = '⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    i = 0
    while not stop_spinner:
        print(f"\r{CYAN}[{chars[i % len(chars)]}]{NC} {BLUE}FETCHING...{NC}", end='')
        i += 1
        time.sleep(0.1)

def progress(current, total):
    width = 50
    percent = int((current * 100) / total)
    filled = int((percent * width) / 100)
    empty = width - filled
    print(f"\r{BLUE}[{NC}{'█' * filled}{'░' * empty}{BLUE}]{NC} {WHITE}{percent:3d}%{NC}", end='')

def main_menu():
    while True:
        banner()
        print(f"""{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{BOLD}  📌 MAIN MENU{NC}
{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        print(f"  {GREEN}[1]{NC} SCRAPE WEBSITE")
        print(f"  {GREEN}[2]{NC} SCRAPE API")
        print(f"  {GREEN}[3]{NC} ABOUT")
        print(f"  {GREEN}[4]{NC} CONTACT DEV")
        print(f"  {RED}[5]{NC} EXIT")
        print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"\n{YELLOW}┌─[{GREEN}SELECT OPTION{YELLOW}]{NC}")
        choice = input("└──➜ ")

        if choice == '5':
            print(f"\n{RED}✗ EXITING...{NC}")
            sys.exit(0)
        elif choice == '4':
            contact()
        elif choice == '3':
            about()
        elif choice == '2':
            scrape_api()
        elif choice == '1':
            scrape_website()
        else:
            print(f"\n{RED}✗ INVALID OPTION{NC}")
            time.sleep(1)

def contact():
    clear()
    print(f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  📱 CONTACT DEV GIFT                                             ║
║                                                                   ║
║  Phone: 2349164624021                                            ║
║  GitHub: github.com/devvgift                                     ║
║                                                                   ║
║  Feel free to reach out for:                                     ║
║  • Support                                                       ║
║  • Collaboration                                                 ║
║  • Custom tools                                                  ║
║  • Bug reports                                                   ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{NC}""")
    input(f"\n{YELLOW}Press Enter to continue...{NC}")

def about():
    clear()
    print(f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  🔥 DEV GIFT SCRAPER v6.0                                       ║
║                                                                   ║
║  A powerful website scanner that FINDS EVERYTHING:               ║
║  • All files linked on the page                                  ║
║  • Hidden directories                                            ║
║  • Admin panels                                                  ║
║  • Exposed config files                                          ║
║  • API keys and secrets                                          ║
║  • Database backups                                              ║
║  • API endpoints                                                 ║
║  • API responses                                                 ║
║                                                                   ║
║  Created by: Dev Gift                                            ║
║  GitHub: github.com/devvgift                                     ║
║  Contact: 2349164624021                                          ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{NC}""")
    input(f"\n{YELLOW}Press Enter to continue...{NC}")

def scrape_api():
    clear()
    print(f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║              🎯 API SCRAPER                                      ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{NC}""")
    print(f"""{YELLOW}┌───────────────────────────────────────────────────────────────────┐
│{NC}  {BOLD}EXAMPLE:{NC} https://api.example.com/data                 {YELLOW}│
│{NC}  {BOLD}NOTE:{NC} Enter full API URL                          {YELLOW}│
{YELLOW}└───────────────────────────────────────────────────────────────────┘{NC}
""")
    api_url = input(f"{YELLOW}┌─[{GREEN}ENTER API URL{YELLOW}]{NC}\n└──➜ ")

    print(f"""{YELLOW}
┌───────────────────────────────────────────────────────────────────┐
│{NC}  {BOLD}METHOD:{NC}                                             {YELLOW}│
│{NC}  {GREEN}[1]{NC} GET                                           {YELLOW}│
│{NC}  {GREEN}[2]{NC} POST                                          {YELLOW}│
{YELLOW}└───────────────────────────────────────────────────────────────────┘
""")
    method = input(f"{YELLOW}┌─[{GREEN}SELECT METHOD{YELLOW}]{NC}\n└──➜ ")

    clear()
    print(f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║           🚀 API SCRAPER ENGINE                                  ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{NC}""")

    print(f"""{BLUE}┌───────────────────────────────────────────────────────────────────┐
│{NC}  {BOLD}API URL:{NC} {api_url}
│{NC}  {BOLD}METHOD:{NC} {'GET' if method == '1' else 'POST'}
│{NC}  {BOLD}STATUS:{NC} {YELLOW}FETCHING...{NC}
{BLUE}└───────────────────────────────────────────────────────────────────┘
{NC}""")

    try:
        if method == '1':
            response = requests.get(api_url, headers={'User-Agent': 'DevGiftScraper'}, verify=False)
        else:
            post_data = input(f"{YELLOW}┌─[{GREEN}ENTER POST DATA (JSON){YELLOW}]{NC}\n└──➜ ")
            response = requests.post(api_url, json=json.loads(post_data), headers={'User-Agent': 'DevGiftScraper'}, verify=False)

        print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"{BOLD}📡 API RESPONSE{NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

        if response.status_code == 200:
            print(f"\n{GREEN}✓ RESPONSE SIZE: {len(response.text)} bytes{NC}\n")
            print(f"{YELLOW}► RAW RESPONSE:{NC}")
            print(f"{BLUE}───────────────────────────────────────────────────────────────────{NC}")
            print(response.text[:1000])
            print(f"\n{BLUE}───────────────────────────────────────────────────────────────────{NC}")

            print(f"\n{YELLOW}► EXTRACTED DATA:{NC}")
            try:
                data = response.json()
                print(f"{GREEN}✓ JSON parsed successfully{NC}\n")
                print(json.dumps(data, indent=2)[:500])

                print(f"\n{YELLOW}► KEYS FOUND:{NC}")
                print(list(data.keys()))

                print(f"\n{YELLOW}► SEARCHING FOR SECRETS:{NC}")
                secrets = []
                def find_secrets(obj):
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            if any(x in str(value).lower() for x in ['key', 'token', 'secret', 'password', 'api']):
                                secrets.append(f"{key}: {value}")
                            find_secrets(value)
                    elif isinstance(obj, list):
                        for item in obj:
                            find_secrets(item)
                find_secrets(data)
                for secret in secrets[:10]:
                    print(f"  {GREEN}↳{NC} {secret}")
            except:
                print(f"{YELLOW}⚠ Not valid JSON{NC}")

            with open('/tmp/api_results.txt', 'w') as f:
                f.write(f"DEV GIFT API SCRAPE RESULTS\n")
                f.write(f"============================\n")
                f.write(f"API URL: {api_url}\n")
                f.write(f"Method: {'GET' if method == '1' else 'POST'}\n")
                f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"RESPONSE:\n")
                f.write(f"---------\n")
                f.write(response.text)

            print(f"\n{YELLOW}┌───────────────────────────────────────────────────────────────────┐")
            print(f"│{NC}  {GREEN}RESULTS SAVED TO:{NC} /tmp/api_results.txt              {YELLOW}│")
            print(f"{YELLOW}└───────────────────────────────────────────────────────────────────┘{NC}")
        else:
            print(f"\n{RED}✗ API ERROR: {response.status_code}{NC}")

    except Exception as e:
        print(f"\n{RED}✗ ERROR: {e}{NC}")

    input(f"\n{YELLOW}Press Enter to continue...{NC}")

def scrape_website():
    clear()
    print(f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║              🎯 TARGET WEBSITE INPUT                             ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{NC}""")
    print(f"""{YELLOW}┌───────────────────────────────────────────────────────────────────┐
│{NC}  {BOLD}EXAMPLE:{NC} example.com                                      {YELLOW}│
│{NC}  {BOLD}NOTE:{NC} Don't add http:// or https://                    {YELLOW}│
{YELLOW}└───────────────────────────────────────────────────────────────────┘
{NC}""")
    site = input(f"{YELLOW}┌─[{GREEN}ENTER TARGET URL{YELLOW}]{NC}\n└──➜ ")
    site = site.replace('https://', '').replace('http://', '').rstrip('/')
    base_url = f"https://{site}"

    clear()
    print(f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║           🚀 DEV GIFT SCRAPER ENGINE                             ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{NC}""")
    print(f"""{BLUE}┌───────────────────────────────────────────────────────────────────┐
│{NC}  {BOLD}TARGET:{NC} {base_url}
│{NC}  {BOLD}STATUS:{NC} {YELLOW}CONNECTING...{NC}
{BLUE}└───────────────────────────────────────────────────────────────────┘
{NC}""")

    print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
    print(f"{BOLD}📡 PHASE 1: FETCHING HOMEPAGE{NC}")
    print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

    try:
        response = requests.get(base_url, headers={'User-Agent': 'DevGiftScraper'}, verify=False, timeout=30)
        print(f"{GREEN}✓ HOMEPAGE LOADED!{NC}")
        print(f"{GREEN}✓ PAGE SIZE: {len(response.text)} bytes{NC}\n")

        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"{BOLD}🔍 PHASE 2: EXTRACTING ALL RESOURCES{NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

        import re
        js_files = re.findall(r'src="([^"]*\.js)"', response.text)
        print(f"\n{YELLOW}► JAVASCRIPT FILES{NC}")
        for js in js_files[:10]:
            print(f"  {GREEN}↳{NC} {urljoin(base_url, js)}")

        css_files = re.findall(r'href="([^"]*\.css)"', response.text)
        print(f"\n{YELLOW}► CSS FILES{NC}")
        for css in css_files[:10]:
            print(f"  {GREEN}↳{NC} {urljoin(base_url, css)}")

        images = re.findall(r'src="([^"]*\.(?:jpg|png|gif|svg|webp|jpeg|ico))"', response.text)
        print(f"\n{YELLOW}► IMAGES{NC}")
        for img in images[:10]:
            print(f"  {GREEN}↳{NC} {urljoin(base_url, img)}")

        links = re.findall(r'href="([^"]*)"', response.text)
        internal_links = [l for l in links if not l.startswith('http')]
        print(f"\n{YELLOW}► ALL LINKS FOUND ON PAGE{NC}")
        for link in internal_links[:20]:
            print(f"  {GREEN}↳{NC} {urljoin(base_url, link)}")

        print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"{BOLD}🔎 PHASE 3: FINDING ADMIN PANELS (AUTO-DISCOVER){NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

        print(f"\n{YELLOW}► CHECKING ALL DISCOVERED PATHS{NC}")
        total = len(internal_links[:20])
        for i, link in enumerate(internal_links[:20]):
            progress(i+1, total)
            try:
                test_url = urljoin(base_url, link)
                resp = requests.get(test_url, timeout=5)
                if resp.status_code in [200, 403, 401]:
                    print(f"\n  {GREEN}✓{NC} {test_url} {BLUE}[{resp.status_code}]{NC}")
            except:
                pass

        print(f"\n\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"{BOLD}📁 PHASE 4: FINDING SENSITIVE FILES{NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

        sensitive_files = [
            "robots.txt", "sitemap.xml", ".env", "config.php", "settings.json",
            "package.json", "composer.json", "wp-config.php", ".htaccess",
            "web.config", "backup.zip", "db.sql", "dump.sql", "README.md",
            "LICENSE", "CHANGELOG.md", "Dockerfile", "docker-compose.yml",
            "nginx.conf", "php.ini", "index.php", "index.html", "default.php",
            "default.html", "home.php", "home.html", "main.php", "main.html",
            "app.js", "app.css", "style.css", "script.js", "config.js",
            "settings.js", "credentials.txt", "passwords.txt", "admin.txt",
            "login.txt", "config.txt", "backup.tar.gz", "backup.rar",
            "site.zip", "database.sql", "db_backup.sql", "mysql.sql",
            "postgres.sql"
        ]

        found = 0
        total = len(sensitive_files)
        for i, file in enumerate(sensitive_files):
            progress(i+1, total)
            try:
                test_url = f"{base_url}/{file}"
                resp = requests.get(test_url, timeout=5)
                if resp.status_code == 200:
                    print(f"\n{GREEN}✓ FOUND{NC} {test_url} {BLUE}[{resp.status_code}]{NC}")
                    found += 1
            except:
                pass

        print(f"\n\n{GREEN}✓ SENSITIVE FILES FOUND: {found}{NC}\n")

        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"{BOLD}🔬 PHASE 5: ANALYZING JAVASCRIPT FILES{NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

        for js in js_files[:5]:
            print(f"\n{YELLOW}►{NC} {os.path.basename(js)}")
            try:
                js_url = urljoin(base_url, js)
                js_response = requests.get(js_url, timeout=10)
                secrets = re.findall(r'(api|key|token|secret|admin|password|url|endpoint|auth|firebase|aws|s3|mongodb|mysql|database|jwt|bearer|client_id|client_secret|private|public|stripe|paypal|github|gitlab|facebook|google|twitter|instagram)', js_response.text.lower())
                for secret in secrets[:5]:
                    print(f"  {GREEN}↳{NC} {secret}")
            except:
                pass

        print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"{GREEN}✅ SCAN COMPLETE - DEV GIFT SCRAPER{NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")

        with open('/tmp/scrape_results.txt', 'w') as f:
            f.write(f"DEV GIFT SCRAPER RESULTS\n")
            f.write(f"========================\n")
            f.write(f"Target: {base_url}\n")
            f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("ALL FOUND FILES:\n")
            f.write("----------------\n")
            for link in internal_links[:50]:
                f.write(f"{urljoin(base_url, link)}\n")
            f.write("\nSENSITIVE FILES FOUND:\n")
            f.write("---------------------\n")
            for file in sensitive_files:
                try:
                    test_url = f"{base_url}/{file}"
                    resp = requests.get(test_url, timeout=5)
                    if resp.status_code == 200:
                        f.write(f"{test_url} [{resp.status_code}]\n")
                except:
                    pass

        print(f"\n{YELLOW}┌───────────────────────────────────────────────────────────────────┐")
        print(f"│{NC}  {GREEN}RESULTS SAVED TO:{NC} /tmp/scrape_results.txt           {YELLOW}│")
        print(f"{YELLOW}└───────────────────────────────────────────────────────────────────┘{NC}")

    except Exception as e:
        print(f"\n{RED}✗ ERROR: {e}{NC}")

    input(f"\n{YELLOW}Press Enter to continue...{NC}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{RED}✗ EXITING...{NC}")
        sys.exit(0)
