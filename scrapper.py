

import os
import sys
import time
import json
import re
import requests
from urllib.parse import urljoin, urlparse
from colorama import init, Fore, Back, Style
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

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

RESULTS_DIR = os.path.expanduser("~/scraper_results")
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

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
║              🔥 DEV GIFT SCRAPER v8.0 🔥                         ║
║              🕷️ DEEP CRAWLER EDITION                             ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{NC}""")
    print(f"""{YELLOW}┌───────────────────────────────────────────────────────────────────┐
│  DEVELOPER: Dev Gift                         CONTACT: 2349164624021 │
│  VERSION: 8.0                                GITHUB: devvgift       │
│  RESULTS: {GREEN}{RESULTS_DIR}{YELLOW}                                      │
│  STATUS: {GREEN}● ACTIVE{NC}{YELLOW}                                                  │
└───────────────────────────────────────────────────────────────────┘
{NC}""")

def save_results(filename, content):
    try:
        filepath = os.path.join(RESULTS_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath
    except Exception as e:
        print(f"{RED}✗ ERROR saving: {e}{NC}")
        return None

def view_file(filepath):
    try:
        if filepath.startswith('http'):
            response = requests.get(filepath, verify=False, timeout=10)
            content = response.text
        else:
            if not os.path.exists(filepath):
                test_path = os.path.join(RESULTS_DIR, filepath)
                if os.path.exists(test_path):
                    filepath = test_path
                else:
                    print(f"{RED}✗ File not found: {filepath}{NC}")
                    return
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        
        print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"{GREEN}📄 FILE: {WHITE}{filepath}{NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        
        lines = content.split('\n')
        for i, line in enumerate(lines[:100]):
            print(f"{BLUE}{i+1:4d}{NC} {line}")
        
        if len(lines) > 100:
            print(f"\n{YELLOW}... (showing first 100 lines, {len(lines)} total){NC}")
        
        print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
    except Exception as e:
        print(f"{RED}✗ ERROR: {e}{NC}")
    
    input(f"\n{YELLOW}Press Enter to continue...{NC}")

def list_saved_results():
    clear()
    print(f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║              📂 SAVED RESULTS                                     ║
║              {RESULTS_DIR}                                        ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{NC}""")
    
    if not os.path.exists(RESULTS_DIR):
        print(f"\n{RED}✗ No results directory found{NC}")
        input(f"\n{YELLOW}Press Enter to continue...{NC}")
        return
    
    files = [f for f in os.listdir(RESULTS_DIR) if f.endswith('.txt')]
    
    if not files:
        print(f"\n{YELLOW}⚠ No saved results found{NC}")
        input(f"\n{YELLOW}Press Enter to continue...{NC}")
        return
    
    print(f"\n{GREEN}✓ Found {len(files)} result files:{NC}\n")
    for i, file in enumerate(files, 1):
        filepath = os.path.join(RESULTS_DIR, file)
        size = os.path.getsize(filepath)
        mtime = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M')
        print(f"  {GREEN}[{i}]{NC} {file} {BLUE}({size} bytes, {mtime}){NC}")
    
    print(f"\n{YELLOW}OPTIONS:{NC}")
    print(f"  {GREEN}[number]{NC} View file")
    print(f"  {GREEN}[d]{NC} Delete a file")
    print(f"  {GREEN}[c]{NC} Clear all results")
    print(f"  {GREEN}[b]{NC} Back to menu")
    
    choice = input(f"\n{YELLOW}┌─[{GREEN}SELECT OPTION{YELLOW}]{NC}\n└──➜ ")
    
    if choice.lower() == 'b':
        return
    elif choice.lower() == 'c':
        confirm = input(f"{RED}Delete ALL results? (y/n): {NC}")
        if confirm.lower() == 'y':
            for file in files:
                os.remove(os.path.join(RESULTS_DIR, file))
            print(f"{GREEN}✓ All results cleared{NC}")
        input(f"\n{YELLOW}Press Enter to continue...{NC}")
        return
    elif choice.lower() == 'd':
        file_num = input(f"{YELLOW}Enter file number to delete: {NC}")
        try:
            idx = int(file_num) - 1
            if 0 <= idx < len(files):
                os.remove(os.path.join(RESULTS_DIR, files[idx]))
                print(f"{GREEN}✓ Deleted: {files[idx]}{NC}")
            else:
                print(f"{RED}✗ Invalid number{NC}")
        except:
            print(f"{RED}✗ Invalid input{NC}")
        input(f"\n{YELLOW}Press Enter to continue...{NC}")
        return
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                filepath = os.path.join(RESULTS_DIR, files[idx])
                view_file(filepath)
            else:
                print(f"{RED}✗ Invalid number{NC}")
                input(f"\n{YELLOW}Press Enter to continue...{NC}")
        except:
            print(f"{RED}✗ Invalid input{NC}")
            input(f"\n{YELLOW}Press Enter to continue...{NC}")

def main_menu():
    while True:
        banner()
        print(f"""{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{BOLD}  📌 MAIN MENU{NC}
{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        print(f"  {GREEN}[1]{NC} SCRAPE WEBSITE")
        print(f"  {GREEN}[2]{NC} VIEW SAVED RESULTS")
        print(f"  {GREEN}[3]{NC} ABOUT")
        print(f"  {RED}[4]{NC} EXIT")
        print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"\n{YELLOW}┌─[{GREEN}SELECT OPTION{YELLOW}]{NC}")
        choice = input("└──➜ ")

        if choice == '4':
            print(f"\n{RED}✗ EXITING...{NC}")
            sys.exit(0)
        elif choice == '3':
            about()
        elif choice == '2':
            list_saved_results()
        elif choice == '1':
            scrape_website()
        else:
            print(f"\n{RED}✗ INVALID OPTION{NC}")
            time.sleep(1)

def about():
    clear()
    print(f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  🔥 DEV GIFT SCRAPER v8.0 - DEEP CRAWLER                        ║
║                                                                   ║
║  Advanced website scanner that FINDS EVERYTHING:                 ║
║  • All files & directories                                        ║
║  • Hidden admin panels                                            ║
║  • Exposed config files (.env, config.php)                       ║
║  • API keys & secrets                                             ║
║  • Database backups                                               ║
║  • Sensitive JS files                                             ║
║  • Crawls ALL linked pages                                        ║
║  • Finds files in subdirectories                                  ║
║                                                                   ║
║  Results saved to: {GREEN}{RESULTS_DIR}{NC}                                      ║
║                                                                   ║
║  Created by: Dev Gift                                             ║
║  GitHub: github.com/devvgift                                      ║
║  Contact: 2349164624021                                           ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{NC}""")
    input(f"\n{YELLOW}Press Enter to continue...{NC}")

def check_file(url, timeout=5):
    """Check if a file exists and return status"""
    try:
        resp = requests.get(url, timeout=timeout, verify=False)
        return (url, resp.status_code, resp.text[:500] if resp.status_code == 200 else None)
    except:
        return (url, None, None)

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
│  EXAMPLE: example.com                                            │
│  NOTE: Don't add http:// or https://                             │
└───────────────────────────────────────────────────────────────────┘
{NC}""")
    site = input(f"{YELLOW}┌─[{GREEN}ENTER TARGET URL{YELLOW}]{NC}\n└──➜ ")
    site = site.replace('https://', '').replace('http://', '').rstrip('/')
    base_url = f"https://{site}"

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    result_file = f"{site}_{timestamp}.txt"

    clear()
    print(f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║           🚀 DEV GIFT SCRAPER ENGINE                             ║
║           🕷️ DEEP CRAWLER MODE                                   ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{NC}""")
    print(f"""{BLUE}┌───────────────────────────────────────────────────────────────────┐
│  TARGET: {WHITE}{base_url}{BLUE}                                                  │
│  STATUS: {YELLOW}CONNECTING...{BLUE}                                              │
└───────────────────────────────────────────────────────────────────┘
{NC}""")

    try:
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"{BOLD}📡 PHASE 1: FETCHING HOMEPAGE{NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        
        response = requests.get(base_url, headers={'User-Agent': 'Mozilla/5.0'}, verify=False, timeout=30)
        print(f"{GREEN}✓ HOMEPAGE LOADED!{NC}")
        print(f"{GREEN}✓ PAGE SIZE: {len(response.text)} bytes{NC}\n")

        # Extract ALL links
        all_links = re.findall(r'(?:href|src|action)=["\']([^"\']*)["\']', response.text)
        all_links = [urljoin(base_url, link) for link in all_links]
        all_links = list(set(all_links))
        
        # Filter internal links
        internal_links = [l for l in all_links if site in l and not l.endswith(('.jpg','.png','.gif','.svg','.webp','.ico','.mp4','.mp3','.pdf'))]
        
        js_files = re.findall(r'src=["\']([^"\']*\.js)["\']', response.text)
        js_files = [urljoin(base_url, js) for js in js_files]
        
        css_files = re.findall(r'href=["\']([^"\']*\.css)["\']', response.text)
        css_files = [urljoin(base_url, css) for css in css_files]
        
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"{BOLD}🔍 PHASE 2: EXTRACTING ALL RESOURCES{NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        
        print(f"\n{YELLOW}► JAVASCRIPT FILES{NC}")
        for js in js_files[:15]:
            print(f"  {GREEN}↳{NC} {js}")
        
        print(f"\n{YELLOW}► CSS FILES{NC}")
        for css in css_files[:15]:
            print(f"  {GREEN}↳{NC} {css}")
        
        print(f"\n{YELLOW}► TOTAL LINKS FOUND: {len(all_links)}{NC}")
        print(f"{YELLOW}► INTERNAL LINKS: {len(internal_links)}{NC}")
        
        print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"{BOLD}🔎 PHASE 3: DEEP CRAWLING - CHECKING ALL PAGES{NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        
        print(f"\n{YELLOW}► CRAWLING {len(internal_links[:20])} PAGES FOR SECRETS...{NC}")
        
        secret_files = []
        admin_pages = []
        
        # Common secret file patterns
        secret_patterns = [
            '.env', 'config', 'settings', 'credentials', 'secrets', 'keys',
            'password', 'passwd', 'auth', 'token', 'api', 'private', 'backup',
            'database', 'db', 'mysql', 'postgres', 'mongodb', 'redis',
            'wp-config', 'htaccess', 'git', 'ssh', 'ssl', 'crt', 'key',
            'pem', 'cert', 'p12', 'p7b', 'jks', 'keystore', 'truststore'
        ]
        
        # Common sensitive extensions
        sensitive_extensions = ['.txt', '.log', '.json', '.xml', '.yaml', '.yml', '.sql', '.dump']
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            # Check internal pages
            for link in internal_links[:20]:
                futures.append(executor.submit(check_file, link))
            
            # Check common secret paths
            secret_paths = ['admin', 'login', 'dashboard', 'panel', 'console', 'manage', 'wp-admin']
            for path in secret_paths:
                for secret in secret_patterns[:10]:
                    futures.append(executor.submit(check_file, f"{base_url}/{path}/{secret}"))
            
            # Check root secret files
            for secret in secret_patterns:
                futures.append(executor.submit(check_file, f"{base_url}/{secret}"))
                for ext in sensitive_extensions:
                    futures.append(executor.submit(check_file, f"{base_url}/{secret}{ext}"))
            
            # Check common admin paths
            admin_paths = [
                'admin', 'login', 'dashboard', 'panel', 'console', 'manage',
                'wp-admin', 'administrator', 'backend', 'cp', 'cpanel',
                'controlpanel', 'adminpanel', 'adm', 'webadmin', 'siteadmin',
                'user', 'auth', 'signin', 'signup', 'register', 'forgot', 'reset'
            ]
            for path in admin_paths:
                futures.append(executor.submit(check_file, f"{base_url}/{path}"))
                for ext in sensitive_extensions:
                    futures.append(executor.submit(check_file, f"{base_url}/{path}{ext}"))
            
            total = len(futures)
            completed = 0
            
            for future in as_completed(futures):
                completed += 1
                progress(completed, total, f"Checking paths...")
                url, status, content = future.result()
                
                if status and status == 200:
                    # Check if it's an admin page
                    if any(x in url.lower() for x in admin_paths):
                        admin_pages.append(url)
                    
                    # Check if it's a secret file
                    if any(x in url.lower() for x in secret_patterns):
                        secret_files.append((url, content[:1000] if content else ""))
                    elif any(url.lower().endswith(x) for x in sensitive_extensions):
                        secret_files.append((url, content[:1000] if content else ""))
        
        print()
        
        print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"{BOLD}📁 PHASE 4: RESULTS{NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        
        print(f"\n{YELLOW}► ADMIN PAGES FOUND: {len(admin_pages)}{NC}")
        for page in admin_pages[:20]:
            print(f"  {GREEN}✓{NC} {page}")
        
        print(f"\n{YELLOW}► SECRET FILES FOUND: {len(secret_files)}{NC}")
        for url, content in secret_files[:30]:
            print(f"  {GREEN}✓{NC} {url}")
            # Try to find secrets in content
            if content:
                secrets_in_file = re.findall(r'(api[_-]?key|token|secret|password|key|auth)["\']?\s*[:=]\s*["\']([^"\']+)["\']', content, re.IGNORECASE)
                for match in secrets_in_file[:3]:
                    print(f"    {YELLOW}↳{NC} {match[0]}: {match[1][:50]}")
        
        if not secret_files and not admin_pages:
            print(f"  {YELLOW}⚠ No secret files found{NC}")
        
        print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"{GREEN}✅ SCAN COMPLETE!{NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        
        # Build results
        results = []
        results.append("═" * 70)
        results.append("🔥 DEV GIFT SCRAPER v8.0 - DEEP CRAWL RESULTS")
        results.append("═" * 70)
        results.append(f"TARGET: {base_url}")
        results.append(f"DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        results.append("═" * 70)
        results.append("")
        
        results.append("📡 RESOURCES FOUND:")
        results.append("-" * 40)
        results.append(f"JavaScript Files: {len(js_files)}")
        results.append(f"CSS Files: {len(css_files)}")
        results.append(f"Total Links: {len(all_links)}")
        results.append(f"Internal Links: {len(internal_links)}")
        results.append("")
        
        results.append("🔍 ADMIN PAGES FOUND:")
        results.append("-" * 40)
        if admin_pages:
            for page in admin_pages:
                results.append(f"  ✓ {page}")
        else:
            results.append("None found")
        results.append("")
        
        results.append("🔐 SECRET FILES FOUND:")
        results.append("-" * 40)
        if secret_files:
            for url, content in secret_files:
                results.append(f"  ✓ {url}")
                if content:
                    secrets = re.findall(r'(api[_-]?key|token|secret|password|key|auth)["\']?\s*[:=]\s*["\']([^"\']+)["\']', content, re.IGNORECASE)
                    for match in secrets[:3]:
                        results.append(f"    ↳ {match[0]}: {match[1][:50]}")
        else:
            results.append("None found")
        results.append("")
        
        results.append("═" * 70)
        results.append(f"📁 Full results saved to: {RESULTS_DIR}/{result_file}")
        results.append("═" * 70)
        
        result_content = "\n".join(results)
        
        saved_path = save_results(result_file, result_content)
        save_results("latest.txt", result_content)
        
        if saved_path:
            print(f"\n{GREEN}✓ Results saved to: {WHITE}{saved_path}{NC}")
        
        print(f"\n{YELLOW}┌───────────────────────────────────────────────────────────────────┐")
        print(f"│  {GREEN}RESULTS SAVED TO:{NC} {RESULTS_DIR}/{result_file}")
        print(f"│  {GREEN}LATEST RESULTS:{NC} {RESULTS_DIR}/latest.txt")
        print(f"{YELLOW}└───────────────────────────────────────────────────────────────────┘{NC}")
        
        print(f"\n{YELLOW}OPTIONS:{NC}")
        print(f"  {GREEN}[1]{NC} View results now")
        print(f"  {GREEN}[2]{NC} Back to menu")
        
        choice = input(f"\n{YELLOW}┌─[{GREEN}SELECT OPTION{YELLOW}]{NC}\n└──➜ ")
        
        if choice == '1':
            view_file(saved_path)
        
    except Exception as e:
        print(f"\n{RED}✗ ERROR: {e}{NC}")
        input(f"\n{YELLOW}Press Enter to continue...{NC}")

def progress(current, total, text=""):
    width = 40
    percent = int((current * 100) / total)
    filled = int((percent * width) / 100)
    empty = width - filled
    print(f"\r{BLUE}[{NC}{'█' * filled}{'░' * empty}{BLUE}]{NC} {WHITE}{percent:3d}%{NC} {YELLOW}{text}{NC}", end='')

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{RED}✗ EXITING...{NC}")
        sys.exit(0)
