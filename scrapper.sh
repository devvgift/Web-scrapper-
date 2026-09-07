#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'
BOLD='\033[1m'
BLINK='\033[5m'

clear

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║     ██████  ███████ ██    ██  ██████  ██ ███████                  ║"
echo "║     ██   ██ ██      ██    ██ ██       ██ ██                       ║"
echo "║     ██   ██ █████   ██    ██ ██   ███ ██ █████                    ║"
echo "║     ██   ██ ██       ██  ██  ██    ██ ██ ██                       ║"
echo "║     ██████  ███████   ████    ██████  ██ ██                       ║"
echo "║                                                                   ║"
echo "║          ███████  ██████ ██████  █████  ██████  ███████           ║"
echo "║          ██      ██      ██   ██ ██   ██ ██   ██ ██              ║"
echo "║          ███████ ██      ██████  ███████ ██████  █████            ║"
echo "║               ██ ██      ██   ██ ██   ██ ██      ██              ║"
echo "║          ███████  ██████ ██   ██ ██   ██ ██      ███████         ║"
echo "║                                                                   ║"
echo "║              ${YELLOW}🔥 DEV GIFT SCRAPER ${RED}${BLINK}●${NC}${CYAN}🔥                          ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${YELLOW}┌───────────────────────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│${NC}  ${BOLD}DEVELOPER:${NC} Dev Gift                                    ${YELLOW}│${NC}"
echo -e "${YELLOW}│${NC}  ${BOLD}TOOL:${NC} Website Scraper v5.0                            ${YELLOW}│${NC}"
echo -e "${YELLOW}│${NC}  ${BOLD}GITHUB:${NC} github.com/devvgift                           ${YELLOW}│${NC}"
echo -e "${YELLOW}│${NC}  ${BOLD}CONTACT:${NC} 2349164624021                                ${YELLOW}│${NC}"
echo -e "${YELLOW}│${NC}  ${BOLD}STATUS:${NC} ${GREEN}● READY${NC}                                      ${YELLOW}│${NC}"
echo -e "${YELLOW}└───────────────────────────────────────────────────────────────────┘${NC}"
echo ""

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}  📌 MAIN MENU${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  ${GREEN}[1]${NC} SCRAPE WEBSITE"
echo -e "  ${GREEN}[2]${NC} ABOUT"
echo -e "  ${GREEN}[3]${NC} CONTACT DEV"
echo -e "  ${RED}[4]${NC} EXIT"
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}┌─[${GREEN}SELECT OPTION${YELLOW}]${NC}"
read -p "└──➜ " CHOICE

if [ "$CHOICE" == "4" ]; then
    echo -e "\n${RED}✗ EXITING...${NC}"
    exit 0
fi

if [ "$CHOICE" == "3" ]; then
    clear
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║                                                                   ║"
    echo "║  📱 CONTACT DEV GIFT                                             ║"
    echo "║                                                                   ║"
    echo "║  Phone: 2349164624021                                            ║"
    echo "║  GitHub: github.com/devvgift                                     ║"
    echo "║                                                                   ║"
    echo "║  Feel free to reach out for:                                     ║"
    echo "║  • Support                                                       ║"
    echo "║  • Collaboration                                                 ║"
    echo "║  • Custom tools                                                  ║"
    echo "║  • Bug reports                                                   ║"
    echo "║                                                                   ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo -e "${YELLOW}Press Enter to continue...${NC}"
    read
    exec "$0"
fi

if [ "$CHOICE" == "2" ]; then
    clear
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║                                                                   ║"
    echo "║  🔥 DEV GIFT SCRAPER v5.0                                       ║"
    echo "║                                                                   ║"
    echo "║  A powerful website scanner that FINDS EVERYTHING:               ║"
    echo "║  • All files linked on the page                                  ║"
    echo "║  • Hidden directories                                            ║"
    echo "║  • Admin panels                                                  ║"
    echo "║  • Exposed config files                                          ║"
    echo "║  • API keys and secrets                                          ║"
    echo "║  • Database backups                                              ║"
    echo "║                                                                   ║"
    echo "║  Created by: Dev Gift                                            ║"
    echo "║  GitHub: github.com/devvgift                                     ║"
    echo "║  Contact: 2349164624021                                          ║"
    echo "║                                                                   ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo -e "${YELLOW}Press Enter to continue...${NC}"
    read
    exec "$0"
fi

if [ "$CHOICE" != "1" ]; then
    echo -e "\n${RED}✗ INVALID OPTION${NC}"
    exit 1
fi

clear

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║              🎯 TARGET WEBSITE INPUT                             ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${YELLOW}┌───────────────────────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│${NC}  ${BOLD}EXAMPLE:${NC} example.com                                      ${YELLOW}│${NC}"
echo -e "${YELLOW}│${NC}  ${BOLD}NOTE:${NC} Don't add http:// or https://                    ${YELLOW}│${NC}"
echo -e "${YELLOW}└───────────────────────────────────────────────────────────────────┘${NC}"
echo ""
echo -e "${YELLOW}┌─[${GREEN}ENTER TARGET URL${YELLOW}]${NC}"
read -p "└──➜ " SITE

SITE=$(echo $SITE | sed 's/https\?:\/\///g' | sed 's/\/$//')
BASE_URL="https://$SITE"

clear

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║           🚀 DEV GIFT SCRAPER ENGINE                             ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${BLUE}┌───────────────────────────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│${NC}  ${BOLD}TARGET:${NC} $BASE_URL"
echo -e "${BLUE}│${NC}  ${BOLD}STATUS:${NC} ${YELLOW}CONNECTING...${NC}"
echo -e "${BLUE}└───────────────────────────────────────────────────────────────────┘${NC}"
echo ""

spinner() {
    local pid=$1
    local spin='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    local i=0
    while kill -0 $pid 2>/dev/null; do
        i=$(( (i+1) % 10 ))
        printf "\r${CYAN}[${spin:$i:1}]${NC} ${BLUE}FETCHING HOMEPAGE...${NC}"
        sleep 0.1
    done
    printf "\r${GREEN}[✓] HOMEPAGE LOADED!     ${NC}\n"
}

progress() {
    local current=$1
    local total=$2
    local width=50
    local percent=$((current * 100 / total))
    local filled=$((percent * width / 100))
    local empty=$((width - filled))
    printf "\r${BLUE}[${NC}"
    printf "%${filled}s" | tr ' ' '█'
    printf "%${empty}s" | tr ' ' '░'
    printf "${BLUE}] ${WHITE}%3d%%${NC}" $percent
}

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}📡 PHASE 1: FETCHING HOMEPAGE${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

curl -s -k "$BASE_URL" -o /tmp/page.html 2>/dev/null &
PID=$!
spinner $PID

if [ ! -s /tmp/page.html ]; then
    echo -e "\n${RED}✗ FAILED TO FETCH WEBSITE${NC}"
    exit 1
fi

echo -e "${GREEN}✓ PAGE SIZE: $(wc -c < /tmp/page.html) bytes${NC}\n"

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}🔍 PHASE 2: EXTRACTING ALL RESOURCES${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "\n${YELLOW}► JAVASCRIPT FILES${NC}"
grep -o 'src="[^"]*\.js"' /tmp/page.html | cut -d'"' -f2 | sed "s|^|$BASE_URL/|" | while read line; do
    echo -e "  ${GREEN}↳${NC} $line"
done

echo -e "\n${YELLOW}► CSS FILES${NC}"
grep -o 'href="[^"]*\.css"' /tmp/page.html | cut -d'"' -f2 | sed "s|^|$BASE_URL/|" | while read line; do
    echo -e "  ${GREEN}↳${NC} $line"
done

echo -e "\n${YELLOW}► IMAGES${NC}"
grep -o 'src="[^"]*\.\(jpg\|png\|gif\|svg\|webp\|jpeg\|ico\)"' /tmp/page.html | cut -d'"' -f2 | sed "s|^|$BASE_URL/|" | while read line; do
    echo -e "  ${GREEN}↳${NC} $line"
done

echo -e "\n${YELLOW}► ALL LINKS FOUND ON PAGE${NC}"
grep -o 'href="[^"]*"' /tmp/page.html | cut -d'"' -f2 | grep -v "^http" | sed "s|^|$BASE_URL/|" | sort -u | while read line; do
    echo -e "  ${GREEN}↳${NC} $line"
done

echo -e "\n${YELLOW}► ABSOLUTE URLS FOUND${NC}"
grep -o 'href="https\?://[^"]*"' /tmp/page.html | cut -d'"' -f2 | sort -u | while read line; do
    echo -e "  ${GREEN}↳${NC} $line"
done

echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}🔎 PHASE 3: FINDING ADMIN PANELS (AUTO-DISCOVER)${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "\n${YELLOW}► CHECKING ALL DISCOVERED PATHS${NC}"

grep -o 'href="[^"]*"' /tmp/page.html | cut -d'"' -f2 | grep -v "^http" | sed "s|^|$BASE_URL/|" | sort -u | while read path; do
    status=$(curl -s -o /dev/null -w "%{http_code}" -k "$path" 2>/dev/null)
    if [ "$status" == "200" ] || [ "$status" == "403" ] || [ "$status" == "401" ]; then
        echo -e "  ${GREEN}✓${NC} $path ${BLUE}[$status]${NC}"
    fi
done

echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}📁 PHASE 4: FINDING SENSITIVE FILES${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "\n${YELLOW}► CHECKING COMMON CONFIG FILES${NC}"

FILES=("robots.txt" "sitemap.xml" ".env" "config.php" "settings.json" "package.json" "composer.json" "wp-config.php" ".htaccess" "web.config" "backup.zip" "db.sql" "dump.sql" "README.md" "LICENSE" "CHANGELOG.md" "Dockerfile" "docker-compose.yml" "nginx.conf" "php.ini" "index.php" "index.html" "default.php" "default.html" "home.php" "home.html" "main.php" "main.html" "app.js" "app.css" "style.css" "script.js" "config.js" "settings.js" "credentials.txt" "passwords.txt" "admin.txt" "login.txt" "config.txt" "backup.tar.gz" "backup.rar" "site.zip" "database.sql" "db_backup.sql" "mysql.sql" "postgres.sql")

count=0
total=${#FILES[@]}
found=0

echo ""
for file in "${FILES[@]}"; do
    count=$((count + 1))
    progress $count $total
    status=$(curl -s -o /dev/null -w "%{http_code}" -k "$BASE_URL/$file" 2>/dev/null)
    
    if [ "$status" == "200" ]; then
        printf "\n${GREEN}✓ FOUND${NC} $BASE_URL/$file ${BLUE}[$status]${NC}"
        found=$((found + 1))
    fi
done

printf "\n\n${GREEN}✓ SENSITIVE FILES FOUND: $found${NC}\n"

echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}🔬 PHASE 5: ANALYZING JAVASCRIPT FILES${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

grep -o 'src="[^"]*\.js"' /tmp/page.html | cut -d'"' -f2 | head -10 | while read js; do
    js_url="$BASE_URL/$js"
    echo -e "\n${YELLOW}►${NC} $(basename $js)"
    
    curl -s -k "$js_url" 2>/dev/null | grep -E "api|key|token|secret|admin|password|url|endpoint|auth|firebase|aws|s3|mongodb|mysql|database|jwt|bearer|client_id|client_secret|private|public|stripe|paypal|github|gitlab|facebook|google|twitter|instagram" | head -5 | while read line; do
        echo -e "  ${GREEN}↳${NC} $line"
    done
done

echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ SCAN COMPLETE - DEV GIFT SCRAPER${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "\n${YELLOW}┌───────────────────────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│${NC}  ${GREEN}RESULTS SAVED TO:${NC} /tmp/scrape_results.txt           ${YELLOW}│${NC}"
echo -e "${YELLOW}└───────────────────────────────────────────────────────────────────┘${NC}"

{
    echo "DEV GIFT SCRAPER RESULTS"
    echo "========================"
    echo "Target: $BASE_URL"
    echo "Date: $(date)"
    echo ""
    echo "ALL FOUND FILES:"
    echo "----------------"
    grep -o 'href="[^"]*"' /tmp/page.html | cut -d'"' -f2 | grep -v "^http" | sed "s|^|$BASE_URL/|" | sort -u
    echo ""
    echo "SENSITIVE FILES FOUND:"
    echo "---------------------"
    for file in "${FILES[@]}"; do
        status=$(curl -s -o /dev/null -w "%{http_code}" -k "$BASE_URL/$file" 2>/dev/null)
        if [ "$status" == "200" ]; then
            echo "$BASE_URL/$file [$status]"
        fi
    done
} > /tmp/scrape_results.txt

rm -f /tmp/page.html

echo ""
echo -e "${YELLOW}Press Enter to return to menu...${NC}"
read
exec "$0"
