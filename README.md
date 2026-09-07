DEV GIFT WEB SCRAPER
====================

Advanced Website Scanner & File Finder

Version: 4.0
License: MIT
Author: Dev Gift

DESCRIPTION
-----------
Dev Gift Web Scraper is a powerful bash-based tool that scans websites for:
- Hidden admin panels
- Exposed configuration files
- API keys and secrets
- Database backups
- Unsecured directories
- Sensitive JavaScript files

FEATURES
--------
- Resource extraction (JS, CSS, Images, Links)
- Admin scanner 
- Sensitive file finder 
- JavaScript secret analyzer
- HTTP status code display
- Fast multi-threaded scanning

INSTALLATION
------------

1. Clone the repository:
   git clone https://github.com/devvgift/scraper.git
   cd scraper

2. Make executable:
   chmod +x scraper.sh

3. Run the tool:
   ./scraper.sh

QUICK INSTALL (ONE-LINER)
-------------------------
curl -s https://raw.githubusercontent.com/devvgift/scraper/main/scraper.sh -o scraper.sh && chmod +x scraper.sh && ./scraper.sh

USAGE
-----

1. Launch the tool:
   ./scraper.sh

2. Select option:
   [1] SCRAPE WEBSITE
   [2] EXIT

3. Enter target URL:
   └──➜ example.com

4. Wait for results:
   - Tool automatically scans homepage resources
   - Scans admin routes
   - Checks sensitive files
   - Analyzes JavaScript for secrets

📱 RUN ON TERMUX:                          
║                                             
║  git clone https://github.com/devvgift/     
║  Web-scrapper-.git                          
║                                              
║  cd Web-scrapper-                           
║                                              
║  chmod +x scraper.sh                        
║                                              
║  ./scraper.sh                               
║                                              
REQUIREMENTS
------------
- Bash 5.0 or higher
- curl
- Internet connection

TROUBLESHOOTING
---------------
If tool fails to fetch website:
- Check internet connection
- Verify URL is correct
- Try with/without www
- Some sites block curl user-agent

If permission denied:
- Run: chmod +x scraper.sh

If command not found:
- Install curl: pkg install curl (Termux)
- Or: apt-get install curl (Linux)

GITHUB
------
https://github.com/devvgift/scraper

CONTRIBUTING
------------
Pull requests welcome. For major changes, please open an issue first.

LICENSE
-------
MIT License - feel free to use 

DISCLAIMER
----------
This tool is for educational purposes only.
