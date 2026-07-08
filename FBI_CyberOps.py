#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███████╗██████╗ ██╗      ██████╗ ████████╗                               ║
║   ██╔════╝██╔══██╗██║     ██╔═══██╗╚══██╔══╝                               ║
║   █████╗  ██████╔╝██║     ██║   ██║   ██║                                  ║
║   ██╔══╝  ██╔══██╗██║     ██║   ██║   ██║                                  ║
║   ██║     ██║  ██║███████╗╚██████╔╝   ██║                                  ║
║   ╚═╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝    ╚═╝                                  ║
║                                                                              ║
║   FEDERAL BUREAU OF INVESTIGATION - CYBER OPERATIONS DIVISION              ║
║   Développé par HiddenWorld - Hackers Tchadiens                            ║
║   Système d'Opérations Cybernétiques Avancé                                ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import socket
import threading
import subprocess
import re
import math
import random
import signal
import platform
import curses
import select
import termios
import tty
from datetime import datetime
from collections import deque

if platform.system() != "Linux":
    print("[!] Ce script est conçu pour Linux uniquement.")
    sys.exit(1)

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    DARK = '\033[90m'
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

FBI_LOGO = f"""
{Colors.BLUE}{Colors.BOLD}
         ███████╗██████╗ ██╗      ██████╗ ████████╗
         ██╔════╝██╔══██╗██║     ██╔═══██╗╚══██╔══╝
         █████╗  ██████╔╝██║     ██║   ██║   ██║   
         ██╔══╝  ██╔══██╗██║     ██║   ██║   ██║   
         ██║     ██║  ██║███████╗╚██████╔╝   ██║   
         ╚═╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝    ╚═╝   
{Colors.RESET}
{Colors.RED}{Colors.BOLD}
    ╔═══════════════════════════════════════════════════╗
    ║  FEDERAL BUREAU OF INVESTIGATION                  ║
    ║  CYBER OPERATIONS DIVISION                        ║
    ║  CLASSIFIED - TOP SECRET                          ║
    ╚═══════════════════════════════════════════════════╝
{Colors.RESET}
{Colors.YELLOW}
         [ SECURE TERMINAL v9.2.1 - ENCRYPTED ]
         [ Développé par HiddenWorld - Hackers Tchadiens ]
{Colors.RESET}
"""

class FBICyberOps:
    def __init__(self):
        self.running = True
        self.current_user = os.getenv('USER', 'agent')
        self.hostname = socket.gethostname()
        self.clearance_level = "TOP SECRET"
        self.session_id = f"FBI-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{random.randint(1000,9999)}"
        self.active_terminals = {}
        self.log_file = f"fbi_ops_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.setup_terminal()
    
    def setup_terminal(self):
        os.system("clear")
        os.system("echo -e '\033]11;#000510\033\\'")
        os.system("echo -e '\033]10;#00ff41\033\\'")
    
    def log_activity(self, module, action):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "session": self.session_id,
            "user": self.current_user,
            "module": module,
            "action": action
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def print_header(self):
        print(f"{Colors.BLUE}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║  FBI CYBER OPS - Session: {self.session_id:<45} ║")
        print(f"║  Agent: {self.current_user:<20} | Niveau: {self.clearance_level:<20} ║")
        print(f"║  Heure: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<60} ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}")
    
    def boot_sequence(self):
        os.system("clear")
        print(FBI_LOGO)
        time.sleep(1)
        
        messages = [
            ("[INIT] Chargement du noyau sécurisé FBI...", 0.3),
            ("[INIT] Vérification des signatures cryptographiques...", 0.5),
            ("[INIT] Connexion au réseau sécurisé Quantico...", 0.7),
            ("[INIT] Authentification biométrique...", 0.4),
            ("[INIT] Scan des menaces actives...", 0.6),
            ("[INIT] Chargement des modules d'analyse forensique...", 0.5),
            ("[INIT] Initialisation de l'interface multi-terminal...", 0.4),
            ("[INIT] Système prêt. Bienvenue, Agent.", 0.3),
        ]
        
        for msg, delay in messages:
            color = Colors.GREEN if "prêt" in msg else Colors.CYAN
            print(f"{color}{msg}{Colors.RESET}")
            time.sleep(delay)
        
        time.sleep(1)
    
    def launch_terminal(self, name, command, geometry="80x24+0+0"):
        print(f"{Colors.GREEN}[+] Lancement terminal: {name}{Colors.RESET}")
        try:
            term_cmd = f"xterm -title '{name}' -geometry {geometry} -bg black -fg green -fa 'Monospace' -fs 10 -e '{command}; read -p \"Appuyez sur Entrée...\"' &"
            subprocess.Popen(term_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.active_terminals[name] = {"cmd": command, "time": datetime.now()}
            self.log_activity("terminal", f"Launch {name}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur lancement terminal: {e}{Colors.RESET}")
    
    def show_menu(self):
        while self.running:
            os.system("clear")
            self.print_header()
            
            print(f"{Colors.CYAN}{Colors.BOLD}    ╔══════════════════════════════════════════════════════════════════════╗")
            print(f"    ║                    MENU PRINCIPAL - FBI CYBER OPS                    ║")
            print(f"    ╠══════════════════════════════════════════════════════════════════════╣{Colors.RESET}")
            
            menu_items = [
                ("1", "FORENSICS", "Analyse forensique et récupération de données"),
                ("2", "NETWORK OPS", "Opérations réseau et surveillance"),
                ("3", "MALWARE ANALYSIS", "Analyse et reverse engineering"),
                ("4", "CRYPTO", "Cryptographie et décryptage"),
                ("5", "OSINT", "Renseignement sources ouvertes"),
                ("6", "WIRELESS", "Opérations sans fil"),
                ("7", "WEB OPS", "Opérations web et application"),
                ("8", "DATABASE", "Forensique base de données"),
                ("9", "MULTI-TERMINAL", "Lancer plusieurs outils simultanément"),
                ("10", "SYSTEM", "Outils système et configuration"),
                ("11", "LOGS", "Visualiser les logs d'opérations"),
                ("12", "CLEARANCE", "Modifier niveau d'habilitation"),
                ("0", "EXIT", "Quitter le système"),
            ]
            
            for num, title, desc in menu_items:
                color = Colors.RED if num == "0" else Colors.GREEN
                print(f"    {color}[{num:>2}]{Colors.RESET} {Colors.BOLD}{title:<20}{Colors.RESET} {Colors.DARK}- {desc}{Colors.RESET}")
            
            print(f"{Colors.CYAN}    ╚══════════════════════════════════════════════════════════════════════╝{Colors.RESET}")
            print(f"\n{Colors.YELLOW}[?] Sélectionnez une option: {Colors.RESET}", end="")
            
            choice = input().strip()
            
            if choice == "1":
                self.forensics_menu()
            elif choice == "2":
                self.network_menu()
            elif choice == "3":
                self.malware_menu()
            elif choice == "4":
                self.crypto_menu()
            elif choice == "5":
                self.osint_menu()
            elif choice == "6":
                self.wireless_menu()
            elif choice == "7":
                self.webops_menu()
            elif choice == "8":
                self.database_menu()
            elif choice == "9":
                self.multiterminal_menu()
            elif choice == "10":
                self.system_menu()
            elif choice == "11":
                self.view_logs()
            elif choice == "12":
                self.change_clearance()
            elif choice == "0":
                self.shutdown()
            else:
                print(f"{Colors.RED}[!] Option invalide{Colors.RESET}")
                time.sleep(1)
    
    def forensics_menu(self):
        while True:
            os.system("clear")
            self.print_header()
            print(f"{Colors.GREEN}{Colors.BOLD}    [ FORENSICS - Analyse et Récupération de Données ]{Colors.RESET}\n")
            
            tools = [
                ("1", "Autopsy", "Suite forensique complète (GUI)", "autopsy"),
                ("2", "Sleuth Kit", "Outils ligne de commande forensique", "tsk_recover -l /dev/sda1"),
                ("3", "PhotoRec", "Récupération de fichiers supprimés", "photorec"),
                ("4", "Foremost", "Récupération par headers", "foremost -i image.raw -o output/"),
                ("5", "Scalpel", "Carving de fichiers avancé", "scalpel image.raw -o output/"),
                ("6", "Binwalk", "Analyse et extraction firmware", "binwalk -e firmware.bin"),
                ("7", "Volatility", "Analyse mémoire RAM", "volatility -f memory.dump imageinfo"),
                ("8", "Bulk Extractor", "Extraction rapide de données", "bulk_extractor -o out/ image.raw"),
                ("9", "TestDisk", "Récupération de partitions", "testdisk"),
                ("10", "ddrescue", "Imager disque robuste", "ddrescue /dev/sda1 image.img logfile"),
                ("11", "ExifTool", "Analyse métadonnées", "exiftool image.jpg"),
                ("12", "Strings", "Extraction chaînes de caractères", "strings -n 8 file.bin"),
                ("0", "Retour", "", ""),
            ]
            
            for num, name, desc, cmd in tools:
                if num == "0":
                    print(f"\n    {Colors.RED}[{num}]{Colors.RESET} {Colors.BOLD}{name}{Colors.RESET}")
                else:
                    print(f"    {Colors.CYAN}[{num:>2}]{Colors.RESET} {Colors.BOLD}{name:<20}{Colors.RESET} {Colors.DARK}{desc}{Colors.RESET}")
            
            print(f"\n{Colors.YELLOW}[?] Choix: {Colors.RESET}", end="")
            choice = input().strip()
            
            if choice == "0":
                break
            elif choice in [str(i) for i in range(1, 13)]:
                idx = int(choice) - 1
                name, _, _, cmd = tools[idx]
                if name == "Autopsy":
                    self.launch_terminal("FBI-Forensics-Autopsy", "autopsy", "120x40+0+0")
                elif name == "TestDisk":
                    self.launch_terminal("FBI-Forensics-TestDisk", "testdisk", "100x30+100+100")
                elif name == "PhotoRec":
                    self.launch_terminal("FBI-Forensics-PhotoRec", "photorec", "100x30+200+200")
                else:
                    print(f"{Colors.CYAN}[*] Commande: {cmd}{Colors.RESET}")
                    print(f"{Colors.YELLOW}[*] Entrez le fichier cible (ou chemin): {Colors.RESET}", end="")
                    target = input().strip()
                    if target:
                        full_cmd = cmd.replace("image.raw", target).replace("file.bin", target).replace("firmware.bin", target).replace("memory.dump", target).replace("image.jpg", target)
                        self.launch_terminal(f"FBI-Forensics-{name}", full_cmd, "100x30+50+50")
                input(f"\n{Colors.DARK}[Appuyez sur Entrée...]{Colors.RESET}")
    
    def network_menu(self):
        while True:
            os.system("clear")
            self.print_header()
            print(f"{Colors.GREEN}{Colors.BOLD}    [ NETWORK OPS - Surveillance et Analyse Réseau ]{Colors.RESET}\n")
            
            tools = [
                ("1", "Wireshark", "Analyseur de protocoles réseau", "wireshark"),
                ("2", "tcpdump", "Capture paquets ligne de commande", "sudo tcpdump -i eth0 -w capture.pcap"),
                ("3", "nmap", "Scan réseau et découverte", "sudo nmap -sS -A 192.168.1.0/24"),
                ("4", "Masscan", "Scan rapide Internet", "sudo masscan -p1-65535 192.168.1.0/24"),
                ("5", "Zeek", "Analyse trafic réseau", "sudo zeek -i eth0"),
                ("6", "Suricata", "IDS/IPS avancé", "sudo suricata -i eth0"),
                ("7", "Snort", "Système de détection d'intrusion", "sudo snort -i eth0 -c /etc/snort/snort.conf"),
                ("8", "Netcat", "Swiss army knife réseau", "nc -lvp 4444"),
                ("9", "Hping3", "Crafting paquets TCP/IP", "sudo hping3 -S -p 80 192.168.1.1"),
                ("10", "Tshark", "Wireshark en ligne de commande", "tshark -i eth0 -f 'port 80'"),
                ("11", "iftop", "Bande passante en temps réel", "sudo iftop -i eth0"),
                ("12", "nethogs", "Utilisation réseau par processus", "sudo nethogs eth0"),
                ("0", "Retour", "", ""),
            ]
            
            for num, name, desc, cmd in tools:
                if num == "0":
                    print(f"\n    {Colors.RED}[{num}]{Colors.RESET} {Colors.BOLD}{name}{Colors.RESET}")
                else:
                    print(f"    {Colors.CYAN}[{num:>2}]{Colors.RESET} {Colors.BOLD}{name:<20}{Colors.RESET} {Colors.DARK}{desc}{Colors.RESET}")
            
            print(f"\n{Colors.YELLOW}[?] Choix: {Colors.RESET}", end="")
            choice = input().strip()
            
            if choice == "0":
                break
            elif choice in [str(i) for i in range(1, 13)]:
                idx = int(choice) - 1
                name, _, _, cmd = tools[idx]
                if name in ["Wireshark"]:
                    self.launch_terminal(f"FBI-Network-{name}", cmd, "140x40+0+0")
                else:
                    print(f"{Colors.CYAN}[*] Commande: {cmd}{Colors.RESET}")
                    print(f"{Colors.YELLOW}[*] Modifier les paramètres? (oui/non): {Colors.RESET}", end="")
                    if input().strip().lower() == "oui":
                        print(f"{Colors.YELLOW}[*] Entrez la commande complète: {Colors.RESET}", end="")
                        cmd = input().strip()
                    self.launch_terminal(f"FBI-Network-{name}", cmd, "120x35+50+50")
                input(f"\n{Colors.DARK}[Appuyez sur Entrée...]{Colors.RESET}")
    
    def malware_menu(self):
        while True:
            os.system("clear")
            self.print_header()
            print(f"{Colors.GREEN}{Colors.BOLD}    [ MALWARE ANALYSIS - Reverse Engineering ]{Colors.RESET}\n")
            
            tools = [
                ("1", "Ghidra", "Suite reverse engineering NSA", "ghidra"),
                ("2", "IDA Free", "Désassembleur interactif", "ida64"),
                ("3", "Radare2", "Framework reverse engineering", "r2 -A /bin/ls"),
                ("4", "Cutter", "Interface graphique Radare2", "cutter"),
                ("5", "x64dbg", "Débogueur Windows (via Wine)", "wine x64dbg"),
                ("6", "OllyDbg", "Débogueur classique", "wine ollydbg"),
                ("7", "PEStudio", "Analyse fichiers PE", "pestudio"),
                ("8", "Detect It Easy", "Identifiant packers/compilateurs", "die"),
                ("9", "YARA", "Classification malware", "yara rules.yar sample.exe"),
                ("10", "Capstone", "Engine désassemblage", "cstool x32 9090"),
                ("11", "Unicorn", "Engine d'émulation CPU", "python3 unicorn_sample.py"),
                ("12", "LIEF", "Manipulation formats binaires", "python3 lief_parse.py"),
                ("0", "Retour", "", ""),
            ]
            
            for num, name, desc, cmd in tools:
                if num == "0":
                    print(f"\n    {Colors.RED}[{num}]{Colors.RESET} {Colors.BOLD}{name}{Colors.RESET}")
                else:
                    print(f"    {Colors.CYAN}[{num:>2}]{Colors.RESET} {Colors.BOLD}{name:<20}{Colors.RESET} {Colors.DARK}{desc}{Colors.RESET}")
            
            print(f"\n{Colors.YELLOW}[?] Choix: {Colors.RESET}", end="")
            choice = input().strip()
            
            if choice == "0":
                break
            elif choice in [str(i) for i in range(1, 13)]:
                idx = int(choice) - 1
                name, _, _, cmd = tools[idx]
                if name in ["Ghidra", "Cutter", "IDA Free"]:
                    self.launch_terminal(f"FBI-Malware-{name}", cmd, "160x50+0+0")
                else:
                    print(f"{Colors.CYAN}[*] Commande: {cmd}{Colors.RESET}")
                    print(f"{Colors.YELLOW}[*] Fichier cible: {Colors.RESET}", end="")
                    target = input().strip()
                    if target:
                        cmd = cmd.replace("/bin/ls", target).replace("sample.exe", target)
                    self.launch_terminal(f"FBI-Malware-{name}", cmd, "120x35+50+50")
                input(f"\n{Colors.DARK}[Appuyez sur Entrée...]{Colors.RESET}")
    
    def crypto_menu(self):
        while True:
            os.system("clear")
            self.print_header()
            print(f"{Colors.GREEN}{Colors.BOLD}    [ CRYPTO - Cryptographie et Décryptage ]{Colors.RESET}\n")
            
            tools = [
                ("1", "Hashcat", "Crack passwords GPU/CPU", "hashcat -m 0 hash.txt wordlist.txt"),
                ("2", "John", "John the Ripper", "john --wordlist=password.lst hash.txt"),
                ("3", "Hydra", "Brute force réseau", "hydra -l admin -P pass.txt ssh://192.168.1.1"),
                ("4", "Aircrack-ng", "Crack WPA/WEP", "aircrack-ng -w wordlist.txt capture.cap"),
                ("5", "GPG", "Chiffrement PGP", "gpg --encrypt --recipient user file.txt"),
                ("6", "OpenSSL", "Outils cryptographiques", "openssl enc -aes-256-cbc -in file -out file.enc"),
                ("7", "Cryptsetup", "Chiffrement disque LUKS", "cryptsetup luksFormat /dev/sda1"),
                ("8", "VeraCrypt", "Conteneurs chiffrés", "veracrypt"),
                ("9", "Stegseek", "Stéganalyse", "stegseek image.jpg wordlist.txt"),
                ("10", "Steghide", "Stéganographie", "steghide embed -cf image.jpg -ef secret.txt"),
                ("11", "Outguess", "Stéganographie avancée", "outguess -k password -d secret.txt image.jpg out.jpg"),
                ("12", "Ciphey", "Décryptage automatique", "ciphey -t 'encrypted_text'"),
                ("0", "Retour", "", ""),
            ]
            
            for num, name, desc, cmd in tools:
                if num == "0":
                    print(f"\n    {Colors.RED}[{num}]{Colors.RESET} {Colors.BOLD}{name}{Colors.RESET}")
                else:
                    print(f"    {Colors.CYAN}[{num:>2}]{Colors.RESET} {Colors.BOLD}{name:<20}{Colors.RESET} {Colors.DARK}{desc}{Colors.RESET}")
            
            print(f"\n{Colors.YELLOW}[?] Choix: {Colors.RESET}", end="")
            choice = input().strip()
            
            if choice == "0":
                break
            elif choice in [str(i) for i in range(1, 13)]:
                idx = int(choice) - 1
                name, _, _, cmd = tools[idx]
                if name == "VeraCrypt":
                    self.launch_terminal("FBI-Crypto-VeraCrypt", "veracrypt", "100x30+100+100")
                else:
                    print(f"{Colors.CYAN}[*] Commande: {cmd}{Colors.RESET}")
                    self.launch_terminal(f"FBI-Crypto-{name}", cmd, "120x35+50+50")
                input(f"\n{Colors.DARK}[Appuyez sur Entrée...]{Colors.RESET}")
    
    def osint_menu(self):
        while True:
            os.system("clear")
            self.print_header()
            print(f"{Colors.GREEN}{Colors.BOLD}    [ OSINT - Renseignement Sources Ouvertes ]{Colors.RESET}\n")
            
            tools = [
                ("1", "theHarvester", "Collecte emails/noms/domaines", "theHarvester -d fbi.gov -b all"),
                ("2", "Maltego", "Visualisation OSINT", "maltego"),
                ("3", "Recon-ng", "Framework OSINT", "recon-ng"),
                ("4", "SpiderFoot", "Automatisation OSINT", "spiderfoot -l 127.0.0.1:5001"),
                ("5", "Sherlock", "Recherche username", "sherlock username"),
                ("6", "Social Engineer", "Ingénierie sociale", "setoolkit"),
                ("7", "OSRFramework", "Outils OSINT divers", "usufy.py -n username"),
                ("8", "DarkSearch", "Recherche dark web", "darksearch"),
                ("9", "Shodan", "Recherche appareils IoT", "shodan host 8.8.8.8"),
                ("10", "Censys", "Recherche internet", "censys search 'services.http.status_code:200'"),
                ("11", "Metagoofil", "Extraction métadonnées", "metagoofil -d fbi.gov -t pdf,doc -l 100"),
                ("12", "ExifTool", "Analyse métadonnées images", "exiftool -a -u image.jpg"),
                ("0", "Retour", "", ""),
            ]
            
            for num, name, desc, cmd in tools:
                if num == "0":
                    print(f"\n    {Colors.RED}[{num}]{Colors.RESET} {Colors.BOLD}{name}{Colors.RESET}")
                else:
                    print(f"    {Colors.CYAN}[{num:>2}]{Colors.RESET} {Colors.BOLD}{name:<20}{Colors.RESET} {Colors.DARK}{desc}{Colors.RESET}")
            
            print(f"\n{Colors.YELLOW}[?] Choix: {Colors.RESET}", end="")
            choice = input().strip()
            
            if choice == "0":
                break
            elif choice in [str(i) for i in range(1, 13)]:
                idx = int(choice) - 1
                name, _, _, cmd = tools[idx]
                if name in ["Maltego", "SpiderFoot"]:
                    self.launch_terminal(f"FBI-OSINT-{name}", cmd, "140x40+0+0")
                else:
                    print(f"{Colors.CYAN}[*] Commande: {cmd}{Colors.RESET}")
                    print(f"{Colors.YELLOW}[*] Cible (domaine/IP/username): {Colors.RESET}", end="")
                    target = input().strip()
                    if target:
                        cmd = cmd.replace("fbi.gov", target).replace("username", target).replace("8.8.8.8", target)
                    self.launch_terminal(f"FBI-OSINT-{name}", cmd, "120x35+50+50")
                input(f"\n{Colors.DARK}[Appuyez sur Entrée...]{Colors.RESET}")
    
    def wireless_menu(self):
        while True:
            os.system("clear")
            self.print_header()
            print(f"{Colors.GREEN}{Colors.BOLD}    [ WIRELESS - Opérations Sans Fil ]{Colors.RESET}\n")
            
            tools = [
                ("1", "Aircrack-ng", "Suite complète WiFi", "aircrack-ng"),
                ("2", "Wifite", "Automatisation WiFi", "sudo wifite"),
                ("3", "Fern WiFi Cracker", "GUI WiFi cracking", "fern-wifi-cracker"),
                ("4", "Kismet", "Détection réseaux sans fil", "sudo kismet"),
                ("5", "Bettercap", "Attaques MITM modernes", "sudo bettercap -iface wlan0"),
                ("6", "WiFi-Pumpkin", "Rogue AP framework", "sudo wifipumpkin3"),
                ("7", "Ghost Phisher", "AP frauduleux + attaques", "sudo ghost-phisher"),
                ("8", "Gqrx", "Récepteur SDR", "gqrx"),
                ("9", "URH", "Analyse RF universelle", "urh"),
                ("10", "RTL_433", "Décodeur RF 433MHz", "rtl_433 -G"),
                ("11", "HackRF", "Outils SDR HackRF", "hackrf_info"),
                ("12", "Bluelog", "Scanner Bluetooth", "sudo bluelog -v"),
                ("0", "Retour", "", ""),
            ]
            
            for num, name, desc, cmd in tools:
                if num == "0":
                    print(f"\n    {Colors.RED}[{num}]{Colors.RESET} {Colors.BOLD}{name}{Colors.RESET}")
                else:
                    print(f"    {Colors.CYAN}[{num:>2}]{Colors.RESET} {Colors.BOLD}{name:<20}{Colors.RESET} {Colors.DARK}{desc}{Colors.RESET}")
            
            print(f"\n{Colors.YELLOW}[?] Choix: {Colors.RESET}", end="")
            choice = input().strip()
            
            if choice == "0":
                break
            elif choice in [str(i) for i in range(1, 13)]:
                idx = int(choice) - 1
                name, _, _, cmd = tools[idx]
                if name in ["Aircrack-ng", "Fern WiFi Cracker", "Kismet", "Gqrx", "URH"]:
                    self.launch_terminal(f"FBI-Wireless-{name}", cmd, "140x40+0+0")
                else:
                    self.launch_terminal(f"FBI-Wireless-{name}", cmd, "120x35+50+50")
                input(f"\n{Colors.DARK}[Appuyez sur Entrée...]{Colors.RESET}")
    
    def webops_menu(self):
        while True:
            os.system("clear")
            self.print_header()
            print(f"{Colors.GREEN}{Colors.BOLD}    [ WEB OPS - Opérations Web & Application ]{Colors.RESET}\n")
            
            tools = [
                ("1", "Burp Suite", "Proxy d'interception web", "burpsuite"),
                ("2", "OWASP ZAP", "Scanner vulnérabilités web", "zaproxy"),
                ("3", "Nikto", "Scanner web", "nikto -h http://target.com"),
                ("4", "Dirb", "Découverte répertoires", "dirb http://target.com /usr/share/wordlists/dirb/common.txt"),
                ("5", "Gobuster", "Enumération web rapide", "gobuster dir -u http://target.com -w wordlist.txt"),
                ("6", "SQLMap", "Injection SQL automatisée", "sqlmap -u 'http://target.com?id=1' --dbs"),
                ("7", "XSStrike", "Détection XSS avancée", "python3 xsstrike.py -u 'http://target.com'"),
                ("8", "WPScan", "Scanner WordPress", "wpscan --url http://target.com"),
                ("9", "Commix", "Injection commandes", "python3 commix.py -u 'http://target.com/cmd.php'"),
                ("10", "WhatWeb", "Identification technologies", "whatweb http://target.com"),
                ("11", "Wafw00f", "Détection WAF", "wafw00f http://target.com"),
                ("12", "CMSMap", "Scanner CMS", "cmsmap -t http://target.com"),
                ("0", "Retour", "", ""),
            ]
            
            for num, name, desc, cmd in tools:
                if num == "0":
                    print(f"\n    {Colors.RED}[{num}]{Colors.RESET} {Colors.BOLD}{name}{Colors.RESET}")
                else:
                    print(f"    {Colors.CYAN}[{num:>2}]{Colors.RESET} {Colors.BOLD}{name:<20}{Colors.RESET} {Colors.DARK}{desc}{Colors.RESET}")
            
            print(f"\n{Colors.YELLOW}[?] Choix: {Colors.RESET}", end="")
            choice = input().strip()
            
            if choice == "0":
                break
            elif choice in [str(i) for i in range(1, 13)]:
                idx = int(choice) - 1
                name, _, _, cmd = tools[idx]
                if name in ["Burp Suite", "OWASP ZAP"]:
                    self.launch_terminal(f"FBI-Web-{name}", cmd, "160x50+0+0")
                else:
                    print(f"{Colors.CYAN}[*] Commande: {cmd}{Colors.RESET}")
                    print(f"{Colors.YELLOW}[*] URL cible: {Colors.RESET}", end="")
                    target = input().strip()
                    if target:
                        cmd = cmd.replace("http://target.com", target)
                    self.launch_terminal(f"FBI-Web-{name}", cmd, "120x35+50+50")
                input(f"\n{Colors.DARK}[Appuyez sur Entrée...]{Colors.RESET}")
    
    def database_menu(self):
        while True:
            os.system("clear")
            self.print_header()
            print(f"{Colors.GREEN}{Colors.BOLD}    [ DATABASE - Forensique Base de Données ]{Colors.RESET}\n")
            
            tools = [
                ("1", "sqlmap", "Injection SQL automatisée", "sqlmap -u 'URL' --dbs"),
                ("2", "SQLite Browser", "GUI SQLite", "sqlitebrowser"),
                ("3", "DBeaver", "Client SQL universel", "dbeaver"),
                ("4", "pgAdmin", "Administration PostgreSQL", "pgadmin4"),
                ("5", "MySQL Workbench", "GUI MySQL", "mysql-workbench"),
                ("6", "MongoDB Compass", "GUI MongoDB", "mongodb-compass"),
                ("7", "Redis Desktop", "GUI Redis", "redis-desktop-manager"),
                ("8", "SQuirreL SQL", "Client JDBC", "squirrel-sql"),
                ("9", "SchemaSpy", "Visualisation schéma", "schemaspy -t pgsql -db database -u user -o output"),
                ("10", "sqlcipher", "Chiffrement SQLite", "sqlcipher encrypted.db"),
                ("11", "DB Browser", "Navigateur BDD", "sqlitebrowser"),
                ("12", "osquery", "SQL sur système", "osqueryi"),
                ("0", "Retour", "", ""),
            ]
            
            for num, name, desc, cmd in tools:
                if num == "0":
                    print(f"\n    {Colors.RED}[{num}]{Colors.RESET} {Colors.BOLD}{name}{Colors.RESET}")
                else:
                    print(f"    {Colors.CYAN}[{num:>2}]{Colors.RESET} {Colors.BOLD}{name:<20}{Colors.RESET} {Colors.DARK}{desc}{Colors.RESET}")
            
            print(f"\n{Colors.YELLOW}[?] Choix: {Colors.RESET}", end="")
            choice = input().strip()
            
            if choice == "0":
                break
            elif choice in [str(i) for i in range(1, 13)]:
                idx = int(choice) - 1
                name, _, _, cmd = tools[idx]
                if name in ["SQLite Browser", "DBeaver", "pgAdmin", "MySQL Workbench", "MongoDB Compass", "Redis Desktop"]:
                    self.launch_terminal(f"FBI-DB-{name}", cmd, "140x40+0+0")
                else:
                    self.launch_terminal(f"FBI-DB-{name}", cmd, "120x35+50+50")
                input(f"\n{Colors.DARK}[Appuyez sur Entrée...]{Colors.RESET}")
    
    def multiterminal_menu(self):
        os.system("clear")
        self.print_header()
        print(f"{Colors.GREEN}{Colors.BOLD}    [ MULTI-TERMINAL - Opérations Simultanées ]{Colors.RESET}\n")
        
        print(f"{Colors.CYAN}[*] Lancement de 4 terminaux de surveillance...{Colors.RESET}")
        
        self.launch_terminal("FBI-NET-MON", "sudo tcpdump -i eth0 -nn -c 100", "80x20+0+0")
        time.sleep(0.5)
        self.launch_terminal("FBI-PROC-MON", "watch -n 1 'ps aux --sort=-%cpu | head -20'", "80x20+600+0")
        time.sleep(0.5)
        self.launch_terminal("FBI-NETSTAT", "watch -n 2 'ss -tuln | head -30'", "80x20+0+450")
        time.sleep(0.5)
        self.launch_terminal("FBI-LOGS", "tail -f /var/log/syslog", "80x20+600+450")
        time.sleep(0.5)
        
        print(f"\n{Colors.GREEN}[+] 4 terminaux lancés en mode surveillance{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Appuyez sur Entrée pour continuer...{Colors.RESET}")
        input()
    
    def system_menu(self):
        while True:
            os.system("clear")
            self.print_header()
            print(f"{Colors.GREEN}{Colors.BOLD}    [ SYSTEM - Outils Système et Configuration ]{Colors.RESET}\n")
            
            tools = [
                ("1", "htop", "Moniteur processus interactif", "htop"),
                ("2", "iotop", "I/O disque par processus", "sudo iotop"),
                ("3", "nmon", "Moniteur système complet", "nmon"),
                ("4", "glances", "Surveillance système avancée", "glances"),
                ("5", "lsof", "Fichiers ouverts", "sudo lsof -i"),
                ("6", "strace", "Trace appels système", "strace -p PID"),
                ("7", "ltrace", "Trace appels bibliothèque", "ltrace -p PID"),
                ("8", "sysdig", "Visibility système", "sudo sysdig"),
                ("9", "dstat", "Statistiques système", "dstat -y --top-io"),
                ("10", "sar", "Rapport activité système", "sar -u 1 10"),
                ("11", "vmstat", "Mémoire virtuelle", "vmstat 1 10"),
                ("12", "iostat", "Statistiques I/O", "iostat -x 1 10"),
                ("0", "Retour", "", ""),
            ]
            
            for num, name, desc, cmd in tools:
                if num == "0":
                    print(f"\n    {Colors.RED}[{num}]{Colors.RESET} {Colors.BOLD}{name}{Colors.RESET}")
                else:
                    print(f"    {Colors.CYAN}[{num:>2}]{Colors.RESET} {Colors.BOLD}{name:<20}{Colors.RESET} {Colors.DARK}{desc}{Colors.RESET}")
            
            print(f"\n{Colors.YELLOW}[?] Choix: {Colors.RESET}", end="")
            choice = input().strip()
            
            if choice == "0":
                break
            elif choice in [str(i) for i in range(1, 13)]:
                idx = int(choice) - 1
                name, _, _, cmd = tools[idx]
                if name in ["htop", "glances", "nmon"]:
                    self.launch_terminal(f"FBI-SYS-{name}", cmd, "120x40+0+0")
                else:
                    self.launch_terminal(f"FBI-SYS-{name}", cmd, "100x30+50+50")
                input(f"\n{Colors.DARK}[Appuyez sur Entrée...]{Colors.RESET}")
    
    def view_logs(self):
        os.system("clear")
        self.print_header()
        print(f"{Colors.GREEN}{Colors.BOLD}    [ LOGS - Historique des Opérations ]{Colors.RESET}\n")
        
        try:
            with open(self.log_file, 'r') as f:
                logs = [json.loads(line) for line in f if line.strip()]
            
            print(f"{Colors.CYAN}[*] Total opérations: {len(logs)}{Colors.RESET}\n")
            
            for log in logs[-50:]:
                ts = log.get('timestamp', 'N/A')
                module = log.get('module', 'N/A')
                action = log.get('action', 'N/A')
                print(f"  {Colors.DARK}[{ts}]{Colors.RESET} {Colors.CYAN}{module:<20}{Colors.RESET} {Colors.GREEN}{action}{Colors.RESET}")
        
        except FileNotFoundError:
            print(f"{Colors.YELLOW}[*] Aucun log disponible{Colors.RESET}")
        
        input(f"\n{Colors.DARK}[Appuyez sur Entrée...]{Colors.RESET}")
    
    def change_clearance(self):
        os.system("clear")
        self.print_header()
        print(f"{Colors.GREEN}{Colors.BOLD}    [ CLEARANCE - Niveau d'Habilitation ]{Colors.RESET}\n")
        
        levels = ["UNCLASSIFIED", "CONFIDENTIAL", "SECRET", "TOP SECRET", "COSMIC TOP SECRET"]
        print(f"{Colors.CYAN}[*] Niveau actuel: {self.clearance_level}{Colors.RESET}\n")
        
        for i, level in enumerate(levels, 1):
            color = Colors.GREEN if level == self.clearance_level else Colors.YELLOW
            print(f"    {color}[{i}] {level}{Colors.RESET}")
        
        print(f"\n{Colors.YELLOW}[?] Sélectionnez le niveau: {Colors.RESET}", end="")
        choice = input().strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(levels):
            self.clearance_level = levels[int(choice) - 1]
            print(f"{Colors.GREEN}[+] Niveau mis à jour: {self.clearance_level}{Colors.RESET}")
            self.log_activity("clearance", f"Changed to {self.clearance_level}")
        
        time.sleep(1)
    
    def shutdown(self):
        os.system("clear")
        print(f"{Colors.RED}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                              ║")
        print("║   FERMETURE DU SYSTÈME FBI CYBER OPS                                         ║")
        print("║   Session terminée - Toutes les données sont chiffrées                       ║")
        print("║                                                                              ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}")
        
        self.log_activity("system", "Session terminated")
        
        for name in list(self.active_terminals.keys()):
            print(f"{Colors.YELLOW}[*] Fermeture terminal: {name}{Colors.RESET}")
        
        time.sleep(2)
        self.running = False
        os.system("echo -e '\033]11;\033\\'")
        os.system("echo -e '\033]10;\033\\'")
        os.system("clear")
        sys.exit(0)
    
    def run(self):
        self.boot_sequence()
        self.show_menu()

if __name__ == "__main__":
    try:
        fbi = FBICyberOps()
        fbi.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Interruption par l'utilisateur{Colors.RESET}")
        sys.exit(0)
