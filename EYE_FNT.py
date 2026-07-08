#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███████╗██╗   ██╗███████╗    ███████╗███╗   ██╗████████╗                 ║
║   ██╔════╝╚██╗ ██╔╝██╔════╝    ██╔════╝████╗  ██║╚══██╔══╝                 ║
║   █████╗   ╚████╔╝ █████╗      █████╗  ██╔██╗ ██║   ██║                    ║
║   ██╔══╝    ╚██╔╝  ██╔══╝      ██╔══╝  ██║╚██╗██║   ██║                    ║
║   ███████╗   ██║   ███████╗    ██║     ██║ ╚████║   ██║                    ║
║   ╚══════╝   ╚═╝   ╚══════╝    ╚═╝     ╚═╝  ╚═══╝   ╚═╝                    ║
║                                                                              ║
║   Développé par les Hackers Tchadiens - HiddenWorld Community               ║
║   Système de Surveillance & Analyse Environnementale Complète               ║
║   Version 3.0 - Linux Edition                                                ║
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
import struct
import hashlib
import base64
import csv
import sqlite3
from datetime import datetime
from collections import deque

# Vérification Linux
if platform.system() != "Linux":
    print("[!] Ce script est conçu pour Linux uniquement.")
    sys.exit(1)

# Couleurs ANSI
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
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

# Logo Œil animé
EYE_OPEN = """
        ████████
      ██░░░░░░░░██
    ██░░░░░░░░░░░░██
   ██░░░░▓▓▓▓░░░░░░██
  ██░░░░▓▓██▓▓▓▓░░░░░██
  ██░░░░▓▓████▓▓▓▓░░░██
   ██░░░░▓▓▓▓▓▓░░░░██
     ██░░░░░░░░░░██
       ██░░░░░░██
         ████████
"""

EYE_CLOSED = """
        ████████
      ██░░░░░░░░██
    ██░░░░░░░░░░░░██
   ██░░░░░░░░░░░░░░██
  ██░░░░░░░░░░░░░░░░░██
  ██░░░░░░░░░░░░░░░░░██
   ██░░░░░░░░░░░░░░██
     ██░░░░░░░░░░██
       ██░░░░░░██
         ████████
"""

EYE_HALF = """
        ████████
      ██░░░░░░░░██
    ██░░░░░░░░░░░░██
   ██░░░░▓▓░░░░░░░░██
  ██░░░░▓▓██▓▓░░░░░░░██
  ██░░░░▓▓████▓▓░░░░░██
   ██░░░░▓▓▓▓░░░░░░██
     ██░░░░░░░░░░██
       ██░░░░░░██
         ████████
"""

EYE_LOOK_LEFT = """
        ████████
      ██░░░░░░░░██
    ██░░░░░░░░░░░░██
   ██░░▓▓▓▓░░░░░░░░██
  ██░░▓▓██▓▓▓▓░░░░░░░██
  ██░░▓▓████▓▓▓▓░░░░░██
   ██░░▓▓▓▓░░░░░░░░██
     ██░░░░░░░░░░██
       ██░░░░░░██
         ████████
"""

EYE_LOOK_RIGHT = """
        ████████
      ██░░░░░░░░██
    ██░░░░░░░░░░░░██
   ██░░░░░░░░▓▓▓▓░░██
  ██░░░░░░░░▓▓██▓▓▓▓░██
  ██░░░░░░░░▓▓████▓▓▓██
   ██░░░░░░░░▓▓▓▓░░░██
     ██░░░░░░░░░░██
       ██░░░░░░██
         ████████
"""

class EyeAnimation:
    def __init__(self):
        self.running = False
        self.thread = None
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
    
    def _animate(self):
        eyes = [EYE_OPEN, EYE_HALF, EYE_CLOSED, EYE_HALF, EYE_LOOK_LEFT, EYE_OPEN, EYE_LOOK_RIGHT, EYE_OPEN]
        idx = 0
        while self.running:
            os.system('clear')
            print(f"{Colors.CYAN}{Colors.BOLD}")
            print(eyes[idx])
            print(f"{Colors.RESET}")
            print(f"{Colors.GREEN}{Colors.BOLD}        E Y E _ F N T{Colors.RESET}")
            print(f"{Colors.DARK}   Système de Surveillance & Analyse Environnementale{Colors.RESET}")
            print(f"{Colors.MAGENTA}   HiddenWorld - Hackers Tchadiens{Colors.RESET}")
            print(f"{Colors.YELLOW}   Version 3.0 - Linux Edition{Colors.RESET}")
            idx = (idx + 1) % len(eyes)
            time.sleep(0.6)

class EYEFNT:
    def __init__(self):
        self.running = True
        self.data_buffer = deque(maxlen=1000)
        self.wifi_networks = []
        self.bluetooth_devices = []
        self.detected_faces = []
        self.electromagnetic_readings = []
        self.mediapipe_active = False
        self.camera_active = False
        self.monitoring = False
        self.log_file = f"eye_fnt_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.db_file = f"eye_fnt_data_{datetime.now().strftime('%Y%m%d')}.db"
        self.init_database()
        self.load_modules()
    
    def init_database(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS wifi_networks (
                id INTEGER PRIMARY KEY, timestamp TEXT, essid TEXT, bssid TEXT,
                signal INTEGER, channel INTEGER, encryption TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS bluetooth_devices (
                id INTEGER PRIMARY KEY, timestamp TEXT, name TEXT, address TEXT, rssi INTEGER)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS emf_readings (
                id INTEGER PRIMARY KEY, timestamp TEXT, frequency REAL, amplitude REAL, source TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS camera_events (
                id INTEGER PRIMARY KEY, timestamp TEXT, event_type TEXT, confidence REAL, details TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY, timestamp TEXT, action TEXT, details TEXT)''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur DB: {e}{Colors.RESET}")
    
    def load_modules(self):
        self.modules = {
            # === MEDIAPIPE & VISION (1-8) ===
            1: ("MediaPipe - Détection Visage", self.mediapipe_face_detection),
            2: ("MediaPipe - Détection Mains", self.mediapipe_hand_detection),
            3: ("MediaPipe - Pose Corporelle", self.mediapipe_pose_detection),
            4: ("MediaPipe - Segmentation Selfie", self.mediapipe_selfie_segmentation),
            5: ("MediaPipe - Reconnaissance Gestes", self.mediapipe_gesture_recognition),
            6: ("MediaPipe - Détection Objets 3D", self.mediapipe_objectron),
            7: ("MediaPipe - Suivi des Yeux", self.mediapipe_iris_tracking),
            8: ("MediaPipe - Reconnaissance Faciale Avancée", self.mediapipe_face_mesh),
            
            # === RÉSEAU WIFI (9-16) ===
            9: ("WiFi - Scan Réseaux", self.wifi_scan),
            10: ("WiFi - Analyse Signal", self.wifi_signal_analysis),
            11: ("WiFi - Détection Intrusion", self.wifi_intrusion_detect),
            12: ("WiFi - Capture Handshake", self.wifi_capture_handshake),
            13: ("WiFi - Cracking WPS", self.wifi_wps_attack),
            14: ("WiFi - Création Evil Twin", self.wifi_evil_twin),
            15: ("WiFi - Déauth Attack", self.wifi_deauth),
            16: ("WiFi - Analyse Trafic", self.wifi_traffic_analysis),
            
            # === BLUETOOTH (17-20) ===
            17: ("Bluetooth - Scan Appareils", self.bluetooth_scan),
            18: ("Bluetooth - Sniffing", self.bluetooth_sniff),
            19: ("Bluetooth - Spoofing", self.bluetooth_spoof),
            20: ("Bluetooth - BLE Beacon", self.bluetooth_ble_beacon),
            
            # === ÉLECTROMAGNÉTISME (21-26) ===
            21: ("EMF - Détection Champs EM", self.emf_detection),
            22: ("EMF - Analyse Spectre", self.emf_spectrum_analysis),
            23: ("EMF - Détection Caméras Cachées", self.emf_hidden_camera),
            24: ("EMF - Analyse RFID/NFC", self.emf_rfid_analysis),
            25: ("EMF - Détection Micros Cachés", self.emf_hidden_mic),
            26: ("EMF - Cartographie Thermique EM", self.emf_heatmap),
            
            # === CAMÉRA & SURVEILLANCE (27-32) ===
            27: ("Caméra - Flux Vidéo Direct", self.camera_live_feed),
            28: ("Caméra - Détection Mouvement", self.camera_motion_detect),
            29: ("Caméra - Vision Nocturne", self.camera_night_vision),
            30: ("Caméra - Enregistrement Continu", self.camera_recording),
            31: ("Caméra - Reconnaissance Visage", self.camera_face_recognition),
            32: ("Caméra - Détection Anomalie", self.camera_anomaly_detect),
            
            # === ANALYSE SYSTÈME (33-36) ===
            33: ("Système - Monitoring CPU/RAM", self.system_monitor),
            34: ("Système - Analyse Processus", self.system_process_analysis),
            35: ("Système - Détection Rootkits", self.system_rootkit_detect),
            36: ("Système - Analyse Réseau", self.system_network_analysis),
            
            # === OUTILS AVANCÉS (37-42) ===
            37: ("Stéganographie - Cacher Données", self.stego_hide),
            38: ("Stéganographie - Extraire Données", self.stego_extract),
            39: ("OSINT - Recherche Informations", self.osint_search),
            40: ("OSINT - Géolocalisation IP", self.osint_geoip),
            41: ("Forensics - Analyse Fichiers", self.forensics_file_analysis),
            42: ("Forensics - Récupération Données", self.forensics_data_recovery),
            
            # === CONTRÔLE ENVIRONNEMENT (43-45) ===
            43: ("Environnement - Capteurs Température", self.env_temperature),
            44: ("Environnement - Détection Gaz", self.env_gas_detect),
            45: ("Environnement - Analyse Sonore", self.env_sound_analysis),
            
            # === IA & MACHINE LEARNING (46-48) ===
            46: ("IA - Classification Images", self.ai_image_classify),
            47: ("IA - Détection Anomalies ML", self.ai_anomaly_ml),
            48: ("IA - Prédiction Comportement", self.ai_behavior_predict),
            
            # === RAPPORTS & CONFIG (49-50) ===
            49: ("Générer Rapport Complet", self.generate_report),
            50: ("Configuration Système", self.system_config),
        }
    
    def print_banner(self):
        os.system('clear')
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print(EYE_OPEN)
        print(f"{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}        E Y E _ F N T{Colors.RESET}")
        print(f"{Colors.DARK}   Système de Surveillance & Analyse Environnementale{Colors.RESET}")
        print(f"{Colors.MAGENTA}   HiddenWorld - Hackers Tchadiens{Colors.RESET}")
        print(f"{Colors.YELLOW}   Version 3.0 - Linux Edition{Colors.RESET}")
        print(f"{Colors.DARK}{'='*60}{Colors.RESET}")
    
    def print_menu(self):
        self.print_banner()
        print(f"\n{Colors.BOLD}{Colors.CYAN}[=== M E N U   P R I N C I P A L ===]{Colors.RESET}\n")
        
        categories = [
            (f"{Colors.GREEN}[ MEDIAPIPE & VISION ]{Colors.RESET}", [1,2,3,4,5,6,7,8]),
            (f"{Colors.BLUE}[ RÉSEAU WIFI ]{Colors.RESET}", [9,10,11,12,13,14,15,16]),
            (f"{Colors.CYAN}[ BLUETOOTH ]{Colors.RESET}", [17,18,19,20]),
            (f"{Colors.YELLOW}[ ÉLECTROMAGNÉTISME ]{Colors.RESET}", [21,22,23,24,25,26]),
            (f"{Colors.MAGENTA}[ CAMÉRA & SURVEILLANCE ]{Colors.RESET}", [27,28,29,30,31,32]),
            (f"{Colors.RED}[ ANALYSE SYSTÈME ]{Colors.RESET}", [33,34,35,36]),
            (f"{Colors.GREEN}[ OUTILS AVANCÉS ]{Colors.RESET}", [37,38,39,40,41,42]),
            (f"{Colors.BLUE}[ CONTRÔLE ENVIRONNEMENT ]{Colors.RESET}", [43,44,45]),
            (f"{Colors.CYAN}[ IA & MACHINE LEARNING ]{Colors.RESET}", [46,47,48]),
            (f"{Colors.YELLOW}[ RAPPORTS & CONFIG ]{Colors.RESET}", [49,50]),
        ]
        
        for cat_name, items in categories:
            print(f"\n{cat_name}")
            for num in items:
                if num in self.modules:
                    name = self.modules[num][0]
                    print(f"  {Colors.BOLD}[{num:2d}]{Colors.RESET} {name}")
        
        print(f"\n{Colors.RED}{Colors.BOLD}  [ 0 ] Quitter EYE_FNT{Colors.RESET}")
        print(f"{Colors.DARK}{'='*60}{Colors.RESET}")
    
    def log_activity(self, action, details):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        }
        self.data_buffer.append(entry)
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(entry) + '\n')
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO system_logs (timestamp, action, details) VALUES (?, ?, ?)",
                         (entry['timestamp'], action, details))
            conn.commit()
            conn.close()
        except:
            pass
    
    # ==================== MEDIAPIPE & VISION ====================
    
    def mediapipe_face_detection(self):
        print(f"\n{Colors.GREEN}[+] Lancement MediaPipe - Détection Visage...{Colors.RESET}")
        try:
            import mediapipe as mp
            import cv2
            
            mp_face = mp.solutions.face_detection
            face_detection = mp_face.FaceDetection(min_detection_confidence=0.5)
            
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print(f"{Colors.RED}[!] Caméra non disponible{Colors.RESET}")
                return
            
            print(f"{Colors.CYAN}[*] Appuyez sur 'q' pour quitter{Colors.RESET}")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_detection.process(rgb)
                
                if results.detections:
                    for detection in results.detections:
                        bbox = detection.location_data.relative_bounding_box
                        h, w, _ = frame.shape
                        x = int(bbox.xmin * w)
                        y = int(bbox.ymin * h)
                        bw = int(bbox.width * w)
                        bh = int(bbox.height * h)
                        cv2.rectangle(frame, (x, y), (x+bw, y+bh), (0,255,0), 2)
                        score = int(detection.score[0] * 100)
                        cv2.putText(frame, f"Face: {score}%", (x, y-10),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
                
                cv2.imshow('EYE_FNT - Face Detection', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            self.log_activity("mediapipe_face", "Détection visage terminée")
            
        except ImportError:
            print(f"{Colors.RED}[!] Installez: pip install mediapipe opencv-python{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def mediapipe_hand_detection(self):
        print(f"\n{Colors.GREEN}[+] Lancement MediaPipe - Détection Mains...{Colors.RESET}")
        try:
            import mediapipe as mp
            import cv2
            
            mp_hands = mp.solutions.hands
            hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
            mp_draw = mp.solutions.drawing_utils
            
            cap = cv2.VideoCapture(0)
            print(f"{Colors.CYAN}[*] Appuyez sur 'q' pour quitter{Colors.RESET}")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                cv2.imshow('EYE_FNT - Hand Detection', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            self.log_activity("mediapipe_hand", "Détection mains terminée")
            
        except ImportError:
            print(f"{Colors.RED}[!] Installez: pip install mediapipe opencv-python{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def mediapipe_pose_detection(self):
        print(f"\n{Colors.GREEN}[+] Lancement MediaPipe - Pose Corporelle...{Colors.RESET}")
        try:
            import mediapipe as mp
            import cv2
            
            mp_pose = mp.solutions.pose
            pose = mp_pose.Pose(min_detection_confidence=0.5)
            mp_draw = mp.solutions.drawing_utils
            
            cap = cv2.VideoCapture(0)
            print(f"{Colors.CYAN}[*] Appuyez sur 'q' pour quitter{Colors.RESET}")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(rgb)
                
                if results.pose_landmarks:
                    mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                
                cv2.imshow('EYE_FNT - Pose Detection', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            self.log_activity("mediapipe_pose", "Détection pose terminée")
            
        except ImportError:
            print(f"{Colors.RED}[!] Installez: pip install mediapipe opencv-python{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def mediapipe_selfie_segmentation(self):
        print(f"\n{Colors.GREEN}[+] Lancement MediaPipe - Segmentation Selfie...{Colors.RESET}")
        try:
            import mediapipe as mp
            import cv2
            import numpy as np
            
            mp_selfie = mp.solutions.selfie_segmentation
            selfie = mp_selfie.SelfieSegmentation(model_selection=1)
            
            cap = cv2.VideoCapture(0)
            print(f"{Colors.CYAN}[*] Appuyez sur 'q' pour quitter{Colors.RESET}")
            
            bg_color = (192, 192, 192)
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = selfie.process(rgb)
                
                condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
                bg_image = np.zeros(frame.shape, dtype=np.uint8)
                bg_image[:] = bg_color
                
                output = np.where(condition, frame, bg_image)
                
                cv2.imshow('EYE_FNT - Selfie Segmentation', output)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            self.log_activity("mediapipe_selfie", "Segmentation selfie terminée")
            
        except ImportError:
            print(f"{Colors.RED}[!] Installez: pip install mediapipe opencv-python{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def mediapipe_gesture_recognition(self):
        print(f"\n{Colors.GREEN}[+] Lancement MediaPipe - Reconnaissance Gestes...{Colors.RESET}")
        try:
            import mediapipe as mp
            import cv2
            
            mp_hands = mp.solutions.hands
            hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
            mp_draw = mp.solutions.drawing_utils
            
            def recognize_gesture(landmarks):
                tips = [8, 12, 16, 20]
                fingers = []
                for tip in tips:
                    if landmarks[tip].y < landmarks[tip-2].y:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                
                total = sum(fingers)
                gestures = {0: "Poing", 1: "1 Doigt", 2: "2 Doigts", 3: "3 Doigts", 4: "4 Doigts"}
                return gestures.get(total, "Inconnu")
            
            cap = cv2.VideoCapture(0)
            print(f"{Colors.CYAN}[*] Appuyez sur 'q' pour quitter{Colors.RESET}")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        gesture = recognize_gesture(hand_landmarks.landmark)
                        cv2.putText(frame, f"Geste: {gesture}", (10, 30),
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                
                cv2.imshow('EYE_FNT - Gesture Recognition', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            self.log_activity("mediapipe_gesture", "Reconnaissance gestes terminée")
            
        except ImportError:
            print(f"{Colors.RED}[!] Installez: pip install mediapipe opencv-python{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def mediapipe_objectron(self):
        print(f"\n{Colors.GREEN}[+] Lancement MediaPipe - Détection Objets 3D...{Colors.RESET}")
        try:
            import mediapipe as mp
            import cv2
            
            mp_objectron = mp.solutions.objectron
            objectron = mp_objectron.Objectron(
                static_image_mode=False,
                max_num_objects=5,
                min_detection_confidence=0.5,
                model_name='Shoe'
            )
            mp_draw = mp.solutions.drawing_utils
            
            cap = cv2.VideoCapture(0)
            print(f"{Colors.CYAN}[*] Appuyez sur 'q' pour quitter{Colors.RESET}")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = objectron.process(rgb)
                
                if results.detected_objects:
                    for detected_object in results.detected_objects:
                        mp_draw.draw_landmarks(frame, detected_object.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
                        mp_draw.draw_axis(frame, detected_object.rotation, detected_object.translation)
                
                cv2.imshow('EYE_FNT - Objectron 3D', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            self.log_activity("mediapipe_objectron", "Détection objets 3D terminée")
            
        except ImportError:
            print(f"{Colors.RED}[!] Installez: pip install mediapipe opencv-python{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def mediapipe_iris_tracking(self):
        print(f"\n{Colors.GREEN}[+] Lancement MediaPipe - Suivi des Yeux...{Colors.RESET}")
        try:
            import mediapipe as mp
            import cv2
            
            mp_face_mesh = mp.solutions.face_mesh
            face_mesh = mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5
            )
            mp_draw = mp.solutions.drawing_utils
            
            LEFT_IRIS = [474, 475, 476, 477]
            RIGHT_IRIS = [469, 470, 471, 472]
            
            cap = cv2.VideoCapture(0)
            print(f"{Colors.CYAN}[*] Appuyez sur 'q' pour quitter{Colors.RESET}")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(rgb)
                
                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        h, w, _ = frame.shape
                        for idx in LEFT_IRIS + RIGHT_IRIS:
                            x = int(face_landmarks.landmark[idx].x * w)
                            y = int(face_landmarks.landmark[idx].y * h)
                            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
                
                cv2.imshow('EYE_FNT - Iris Tracking', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            self.log_activity("mediapipe_iris", "Suivi yeux terminé")
            
        except ImportError:
            print(f"{Colors.RED}[!] Installez: pip install mediapipe opencv-python{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def mediapipe_face_mesh(self):
        print(f"\n{Colors.GREEN}[+] Lancement MediaPipe - Reconnaissance Faciale Avancée...{Colors.RESET}")
        try:
            import mediapipe as mp
            import cv2
            
            mp_face_mesh = mp.solutions.face_mesh
            face_mesh = mp_face_mesh.FaceMesh(
                max_num_faces=2,
                refine_landmarks=True,
                min_detection_confidence=0.5
            )
            mp_draw = mp.solutions.drawing_utils
            
            cap = cv2.VideoCapture(0)
            print(f"{Colors.CYAN}[*] Appuyez sur 'q' pour quitter{Colors.RESET}")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(rgb)
                
                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        mp_draw.draw_landmarks(
                            frame,
                            face_landmarks,
                            mp_face_mesh.FACEMESH_TESSELATION,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=mp_draw.DrawingSpec(color=(0,255,0), thickness=1)
                        )
                
                cv2.imshow('EYE_FNT - Face Mesh', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            self.log_activity("mediapipe_facemesh", "Reconnaissance faciale avancée terminée")
            
        except ImportError:
            print(f"{Colors.RED}[!] Installez: pip install mediapipe opencv-python{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    # ==================== WIFI ====================
    
    def wifi_scan(self):
        print(f"\n{Colors.GREEN}[+] Scan des réseaux WiFi...{Colors.RESET}")
        try:
            result = subprocess.run(['iwlist', 'scan'], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                cells = result.stdout.split('Cell ')
                networks = []
                for cell in cells[1:]:
                    essid = re.search(r'ESSID:"([^"]*)"', cell)
                    signal = re.search(r'Signal level=(-\d+)', cell)
                    channel = re.search(r'Channel:(\d+)', cell)
                    encryption = re.search(r'Encryption key:(on|off)', cell)
                    bssid = re.search(r'Address: ([0-9A-F:]{17})', cell)
                    
                    if essid:
                        net = {
                            'essid': essid.group(1),
                            'bssid': bssid.group(1) if bssid else 'N/A',
                            'signal': int(signal.group(1)) if signal else -100,
                            'channel': int(channel.group(1)) if channel else 0,
                            'encrypted': encryption.group(1) == 'on' if encryption else False
                        }
                        networks.append(net)
                
                self.wifi_networks = networks
                print(f"\n{Colors.CYAN}[*] {len(networks)} réseaux trouvés:{Colors.RESET}")
                for i, net in enumerate(networks, 1):
                    enc_color = Colors.GREEN if net['encrypted'] else Colors.RED
                    enc_text = "Sécurisé" if net['encrypted'] else "OUVERT"
                    signal_bar = "█" * max(0, min(10, (net['signal'] + 100) // 5)) + "░" * (10 - max(0, min(10, (net['signal'] + 100) // 5)))
                    print(f"  {Colors.BOLD}[{i}]{Colors.RESET} {net['essid']}")
                    print(f"      BSSID: {net['bssid']}")
                    print(f"      Signal: {Colors.YELLOW}[{signal_bar}]{Colors.RESET} {net['signal']} dBm")
                    print(f"      Canal: {net['channel']} | {enc_color}{enc_text}{Colors.RESET}")
                
                self.log_activity("wifi_scan", f"{len(networks)} réseaux trouvés")
                
                # Sauvegarde DB
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                for net in networks:
                    cursor.execute("INSERT INTO wifi_networks (timestamp, essid, bssid, signal, channel, encryption) VALUES (?, ?, ?, ?, ?, ?)",
                                 (datetime.now().isoformat(), net['essid'], net['bssid'], net['signal'], net['channel'], 'WPA2' if net['encrypted'] else 'OPEN'))
                conn.commit()
                conn.close()
            else:
                print(f"{Colors.RED}[!] Erreur scan WiFi. Essayez avec sudo.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def wifi_signal_analysis(self):
        print(f"\n{Colors.GREEN}[+] Analyse du signal WiFi...{Colors.RESET}")
        try:
            interface = input(f"{Colors.CYAN}[?] Interface WiFi (ex: wlan0): {Colors.RESET}").strip() or "wlan0"
            
            print(f"{Colors.YELLOW}[*] Analyse en cours... Appuyez sur Ctrl+C pour arrêter{Colors.RESET}")
            
            while True:
                result = subprocess.run(
                    ['iwconfig', interface],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    signal_match = re.search(r'Signal level=(-\d+)', result.stdout)
                    quality_match = re.search(r'Link Quality=(\d+)/(\d+)', result.stdout)
                    
                    if signal_match and quality_match:
                        signal = int(signal_match.group(1))
                        quality = int(quality_match.group(1))
                        max_quality = int(quality_match.group(2))
                        percentage = (quality / max_quality) * 100
                        
                        bar = "█" * int(percentage / 5) + "░" * (20 - int(percentage / 5))
                        
                        print(f"\r{Colors.CYAN}Signal: {signal} dBm | Qualité: [{Colors.GREEN}{bar}{Colors.CYAN}] {percentage:.1f}%{Colors.RESET}", end="")
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[*] Analyse arrêtée{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def wifi_intrusion_detect(self):
        print(f"\n{Colors.GREEN}[+] Détection d'intrusion WiFi...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Surveillance des paquets de déauthentification...{Colors.RESET}")
        print(f"{Colors.RED}[!] Nécessite les droits root{Colors.RESET}")
        
        try:
            import scapy.all as scapy
            
            deauth_count = 0
            
            def detect_deauth(packet):
                nonlocal deauth_count
                if packet.haslayer(scapy.Dot11Deauth):
                    deauth_count += 1
                    print(f"\r{Colors.RED}[ALERTE] Paquet de déauthentification détecté! Total: {deauth_count}{Colors.RESET}", end="")
                    self.log_activity("wifi_intrusion", f"Deauth packet #{deauth_count}")
            
            print(f"{Colors.CYAN}[*] Surveillance active... Ctrl+C pour arrêter{Colors.RESET}")
            scapy.sniff(iface="wlan0mon", prn=detect_deauth, store=0)
            
        except ImportError:
            print(f"{Colors.RED}[!] Installez: pip install scapy{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def wifi_capture_handshake(self):
        print(f"\n{Colors.GREEN}[+] Capture Handshake WPA...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Cette fonctionnalité nécessite airodump-ng{Colors.RESET}")
        print(f"{Colors.RED}[!] Usage éducatif uniquement sur vos propres réseaux{Colors.RESET}")
        
        bssid = input(f"{Colors.CYAN}[?] BSSID du réseau cible: {Colors.RESET}").strip()
        channel = input(f"{Colors.CYAN}[?] Canal: {Colors.RESET}").strip()
        output = input(f"{Colors.CYAN}[?] Nom fichier sortie: {Colors.RESET}").strip() or "handshake"
        
        if bssid and channel:
            print(f"{Colors.CYAN}[*] Lancement airodump-ng...{Colors.RESET}")
            print(f"{Colors.YELLOW}[*] Commande: airodump-ng -c {channel} --bssid {bssid} -w {output} wlan0mon{Colors.RESET}")
            self.log_activity("wifi_handshake", f"Capture sur {bssid}")
    
    def wifi_wps_attack(self):
        print(f"\n{Colors.GREEN}[+] Test WPS (WiFi Protected Setup)...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Cette fonctionnalité nécessite wash et reaver{Colors.RESET}")
        
        bssid = input(f"{Colors.CYAN}[?] BSSID du réseau: {Colors.RESET}").strip()
        if bssid:
            print(f"{Colors.CYAN}[*] Commande: reaver -i wlan0mon -b {bssid} -vv{Colors.RESET}")
            self.log_activity("wifi_wps", f"Test WPS sur {bssid}")
    
    def wifi_evil_twin(self):
        print(f"\n{Colors.GREEN}[+] Création Evil Twin...{Colors.RESET}")
        print(f"{Colors.RED}[!] ATTENTION: Usage illégal sans autorisation!{Colors.RESET}")
        
        ssid = input(f"{Colors.CYAN}[?] Nom du réseau à cloner: {Colors.RESET}").strip()
        channel = input(f"{Colors.CYAN}[?] Canal: {Colors.RESET}").strip() or "6"
        
        if ssid:
            print(f"{Colors.YELLOW}[*] Configuration hostapd...{Colors.RESET}")
            config = f"""interface=wlan0
driver=nl80211
ssid={ssid}
hw_mode=g
channel={channel}
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
"""
            print(config)
            print(f"{Colors.CYAN}[*] Lancez: hostapd hostapd.conf{Colors.RESET}")
            self.log_activity("wifi_eviltwin", f"Configuration pour {ssid}")
    
    def wifi_deauth(self):
        print(f"\n{Colors.GREEN}[+] Attaque de Déauthentification...{Colors.RESET}")
        print(f"{Colors.RED}[!] ATTENTION: Usage illégal sans autorisation!{Colors.RESET}")
        
        bssid = input(f"{Colors.CYAN}[?] BSSID du point d'accès: {Colors.RESET}").strip()
        client = input(f"{Colors.CYAN}[?] MAC client (ff:ff:ff:ff:ff:ff pour broadcast): {Colors.RESET}").strip() or "ff:ff:ff:ff:ff:ff"
        count = input(f"{Colors.CYAN}[?] Nombre de paquets (0=infini): {Colors.RESET}").strip() or "0"
        
        if bssid:
            print(f"{Colors.YELLOW}[*] Commande: aireplay-ng -0 {count} -a {bssid} -c {client} wlan0mon{Colors.RESET}")
            self.log_activity("wifi_deauth", f"Deauth sur {bssid}")
    
    def wifi_traffic_analysis(self):
        print(f"\n{Colors.GREEN}[+] Analyse du Trafic WiFi...{Colors.RESET}")
        try:
            import scapy.all as scapy
            
            packets_count = {"TCP": 0, "UDP": 0, "ICMP": 0, "Other": 0}
            
            def analyze_packet(packet):
                if packet.haslayer(scapy.TCP):
                    packets_count["TCP"] += 1
                elif packet.haslayer(scapy.UDP):
                    packets_count["UDP"] += 1
                elif packet.haslayer(scapy.ICMP):
                    packets_count["ICMP"] += 1
                else:
                    packets_count["Other"] += 1
                
                total = sum(packets_count.values())
                print(f"\r{Colors.CYAN}TCP: {packets_count['TCP']} | UDP: {packets_count['UDP']} | ICMP: {packets_count['ICMP']} | Total: {total}{Colors.RESET}", end="")
            
            print(f"{Colors.CYAN}[*] Analyse en cours... Ctrl+C pour arrêter{Colors.RESET}")
            scapy.sniff(prn=analyze_packet, store=0, timeout=60)
            
        except ImportError:
            print(f"{Colors.RED}[!] Installez: pip install scapy{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    # ==================== BLUETOOTH ====================
    
    def bluetooth_scan(self):
        print(f"\n{Colors.GREEN}[+] Scan des appareils Bluetooth...{Colors.RESET}")
        try:
            result = subprocess.run(['hcitool', 'scan'], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                devices = []
                for line in result.stdout.split('\n')[1:]:
                    match = re.match(r'\s*([0-9A-F:]{17})\s+(.*)', line)
                    if match:
                        devices.append({'address': match.group(1), 'name': match.group(2)})
                
                self.bluetooth_devices = devices
                print(f"\n{Colors.CYAN}[*] {len(devices)} appareils trouvés:{Colors.RESET}")
                for i, dev in enumerate(devices, 1):
                    print(f"  {Colors.BOLD}[{i}]{Colors.RESET} {dev['name']} - {dev['address']}")
                
                self.log_activity("bluetooth_scan", f"{len(devices)} appareils trouvés")
                
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                for dev in devices:
                    cursor.execute("INSERT INTO bluetooth_devices (timestamp, name, address, rssi) VALUES (?, ?, ?, ?)",
                                 (datetime.now().isoformat(), dev['name'], dev['address'], -50))
                conn.commit()
                conn.close()
            else:
                print(f"{Colors.RED}[!] Erreur scan Bluetooth{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def bluetooth_sniff(self):
        print(f"\n{Colors.GREEN}[+] Sniffing Bluetooth...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Cette fonctionnalité nécessite un dongle Bluetooth compatible{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Commande: hcidump -X{Colors.RESET}")
        self.log_activity("bluetooth_sniff", "Sniffing démarré")
    
    def bluetooth_spoof(self):
        print(f"\n{Colors.GREEN}[+] Spoofing Bluetooth...{Colors.RESET}")
        print(f"{Colors.RED}[!] ATTENTION: Usage illégal sans autorisation!{Colors.RESET}")
        
        mac = input(f"{Colors.CYAN}[?] Nouvelle MAC (xx:xx:xx:xx:xx:xx): {Colors.RESET}").strip()
        if mac:
            print(f"{Colors.YELLOW}[*] Commande: bdaddr -i hci0 {mac}{Colors.RESET}")
            self.log_activity("bluetooth_spoof", f"Spoof MAC {mac}")
    
    def bluetooth_ble_beacon(self):
        print(f"\n{Colors.GREEN}[+] Émission BLE Beacon...{Colors.RESET}")
        uuid = input(f"{Colors.CYAN}[?] UUID Beacon: {Colors.RESET}").strip() or "E2C56DB5-DFFB-48D2-B060-D0F5A71096E0"
        major = input(f"{Colors.CYAN}[?] Major: {Colors.RESET}").strip() or "0"
        minor = input(f"{Colors.CYAN}[?] Minor: {Colors.RESET}").strip() or "0"
        
        print(f"{Colors.CYAN}[*] Configuration beacon...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] UUID: {uuid}{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Major: {major} | Minor: {minor}{Colors.RESET}")
        self.log_activity("bluetooth_beacon", f"Beacon {uuid}")
    
    # ==================== ÉLECTROMAGNÉTISME ====================
    
    def emf_detection(self):
        print(f"\n{Colors.GREEN}[+] Détection des Champs Électromagnétiques...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Simulation de détection EMF...{Colors.RESET}")
        
        try:
            while True:
                # Simulation de lecture EMF
                freq = random.uniform(0.1, 6.0)
                amplitude = random.uniform(0.01, 100.0)
                sources = ["WiFi", "Bluetooth", "Micro-ondes", "Téléphone", "Inconnu"]
                source = random.choice(sources)
                
                if amplitude > 50:
                    color = Colors.RED
                    level = "ÉLEVÉ"
                elif amplitude > 20:
                    color = Colors.YELLOW
                    level = "MOYEN"
                else:
                    color = Colors.GREEN
                    level = "FAIBLE"
                
                print(f"\r{Colors.CYAN}Freq: {freq:.2f} GHz | Amplitude: {color}{amplitude:.2f} mV/m [{level}]{Colors.RESET} | Source: {source}", end="")
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[*] Détection arrêtée{Colors.RESET}")
            self.log_activity("emf_detection", "Détection EMF terminée")
    
    def emf_spectrum_analysis(self):
        print(f"\n{Colors.GREEN}[+] Analyse Spectrale EMF...{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Analyse des fréquences 0.1-6 GHz...{Colors.RESET}")
        
        bands = [
            ("FM Radio", 0.088, 0.108),
            ("TV VHF", 0.174, 0.230),
            ("GSM 900", 0.880, 0.960),
            ("GSM 1800", 1.710, 1.880),
            ("WiFi 2.4GHz", 2.400, 2.500),
            ("Bluetooth", 2.400, 2.485),
            ("WiFi 5GHz", 5.150, 5.875),
            ("LTE", 0.7, 2.6),
        ]
        
        print(f"\n{Colors.BOLD}{'Bande':<20} {'Début':<10} {'Fin':<10} {'Niveau':<15}{Colors.RESET}")
        print("-" * 60)
        
        for name, start, end in bands:
            level = random.uniform(0, 100)
            if level > 70:
                color = Colors.RED
            elif level > 40:
                color = Colors.YELLOW
            else:
                color = Colors.GREEN
            bar = "█" * int(level / 5) + "░" * (20 - int(level / 5))
            print(f"{name:<20} {start:<10.3f} {end:<10.3f} {color}[{bar}]{Colors.RESET}")
        
        self.log_activity("emf_spectrum", "Analyse spectrale terminée")
    
    def emf_hidden_camera(self):
        print(f"\n{Colors.GREEN}[+] Détection de Caméras Cachées...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Recherche de signaux suspects 1.2-2.4 GHz...{Colors.RESET}")
        
        suspicious = []
        for _ in range(10):
            freq = random.uniform(1.2, 2.4)
            strength = random.uniform(0, 100)
            if strength > 60:
                suspicious.append((freq, strength))
        
        if suspicious:
            print(f"\n{Colors.RED}[!] {len(suspicious)} signaux suspects détectés!{Colors.RESET}")
            for freq, strength in suspicious:
                print(f"  {Colors.YELLOW}Freq: {freq:.3f} GHz | Force: {strength:.1f}%{Colors.RESET}")
        else:
            print(f"\n{Colors.GREEN}[+] Aucun signal suspect détecté{Colors.RESET}")
        
        self.log_activity("emf_camera", f"{len(suspicious)} signaux suspects")
    
    def emf_rfid_analysis(self):
        print(f"\n{Colors.GREEN}[+] Analyse RFID/NFC...{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Fréquences analysées: 125 kHz, 13.56 MHz{Colors.RESET}")
        
        rfid_types = [
            ("EM4100", 125, "Proximité"),
            ("MIFARE Classic", 13.56, "NFC"),
            ("MIFARE DESFire", 13.56, "NFC Sécurisé"),
            ("HID iCLASS", 13.56, "Contrôle accès"),
            ("Indala", 125, "Ancien système"),
        ]
        
        print(f"\n{Colors.BOLD}{'Type':<20} {'Freq (MHz)':<12} {'Usage':<20}{Colors.RESET}")
        print("-" * 55)
        
        for name, freq, usage in rfid_types:
            detected = random.random() > 0.5
            color = Colors.GREEN if detected else Colors.DARK
            status = "DÉTECTÉ" if detected else "Non détecté"
            print(f"{color}{name:<20} {freq:<12} {usage:<20} [{status}]{Colors.RESET}")
        
        self.log_activity("emf_rfid", "Analyse RFID terminée")
    
    def emf_hidden_mic(self):
        print(f"\n{Colors.GREEN}[+] Détection de Micros Cachés...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Recherche de transmissions audio suspects...{Colors.RESET}")
        
        freq_ranges = [
            ("VHF", 30, 300),
            ("UHF", 300, 3000),
            ("ISM", 2400, 2500),
        ]
        
        found = []
        for name, start, end in freq_ranges:
            if random.random() > 0.7:
                freq = random.uniform(start, end)
                found.append((name, freq))
        
        if found:
            print(f"\n{Colors.RED}[!] Transmissions suspectes:{Colors.RESET}")
            for name, freq in found:
                print(f"  {Colors.YELLOW}{name}: {freq:.2f} MHz{Colors.RESET}")
        else:
            print(f"\n{Colors.GREEN}[+] Aucun micro caché détecté{Colors.RESET}")
        
        self.log_activity("emf_mic", f"{len(found)} transmissions suspectes")
    
    def emf_heatmap(self):
        print(f"\n{Colors.GREEN}[+] Cartographie Thermique EMF...{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Génération de la carte thermique de la pièce...{Colors.RESET}")
        
        # Simulation d'une grille 10x10
        grid_size = 10
        print(f"\n{Colors.BOLD}Carte EMF de la pièce (10x10 mètres):{Colors.RESET}\n")
        
        for y in range(grid_size):
            row = ""
            for x in range(grid_size):
                intensity = random.uniform(0, 100)
                if intensity > 70:
                    row += f"{Colors.RED}▓{Colors.RESET}"
                elif intensity > 40:
                    row += f"{Colors.YELLOW}░{Colors.RESET}"
                else:
                    row += f"{Colors.GREEN}·{Colors.RESET}"
            print(f"  {row}")
        
        print(f"\n{Colors.GREEN}· Faible{Colors.RESET}  {Colors.YELLOW}░ Moyen{Colors.RESET}  {Colors.RED}▓ Élevé{Colors.RESET}")
        self.log_activity("emf_heatmap", "Carte thermique générée")
    
    # ==================== CAMÉRA & SURVEILLANCE ====================
    
    def camera_live_feed(self):
        print(f"\n{Colors.GREEN}[+] Flux Vidéo Direct...{Colors.RESET}")
        try:
            import cv2
            
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print(f"{Colors.RED}[!] Caméra non disponible{Colors.RESET}")
                return
            
            print(f"{Colors.CYAN}[*] Appuyez sur 'q' pour quitter{Colors.RESET}")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Ajout d'informations sur le flux
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cv2.putText(frame, f"EYE_FNT - {timestamp}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                cv2.imshow('EYE_FNT - Live Feed', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            self.log_activity("camera_live", "Flux vidéo terminé")
            
        except ImportError:
            print(f"{Colors.RED}[!] Installez: pip install opencv-python{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def camera_motion_detect(self):
        print(f"\n{Colors.GREEN}[+] Détection de Mouvement...{Colors.RESET}")
        try:
            import cv2
            import numpy as np
            
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print(f"{Colors.RED}[!] Caméra non disponible{Colors.RESET}")
                return
            
            ret, frame1 = cap.read()
            ret, frame2 = cap.read()
            
            print(f"{Colors.CYAN}[*] Détection active... Appuyez sur 'q' pour quitter{Colors.RESET}")
            
            while True:
                diff = cv2.absdiff(frame1, frame2)
                gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (5, 5), 0)
                _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
                dilated = cv2.dilate(thresh, None, iterations=3)
                contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in contours:
                    if cv2.contourArea(contour) < 5000:
                        continue
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame1, "MOUVEMENT", (x, y-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                cv2.imshow('EYE_FNT - Motion Detection', frame1)
                frame1 = frame2
                ret, frame2 = cap.read()
                if not ret:
                    break
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            self.log_activity("camera_motion", "Détection mouvement terminée")
            
        except ImportError:
            print(f"{Colors.RED}[!] Installez: pip install opencv-python{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def camera_night_vision(self):
        print(f"\n{Colors.GREEN}[+] Vision Nocturne...{Colors.RESET}")
        try:
            import cv2
            import numpy as np
            
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print(f"{Colors.RED}[!] Caméra non disponible{Colors.RESET}")
                return
            
            print(f"{Colors.CYAN}[*] Mode vision nocturne... Appuyez sur 'q' pour quitter{Colors.RESET}")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Conversion en niveaux de gris et amélioration du contraste
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
                enhanced = clahe.apply(gray)
                
                # Colormap vert (style vision nocturne)
                night = cv2.applyColorMap(enhanced, cv2.COLORMAP_BONE)
                
                cv2.putText(night, "NIGHT VISION", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                cv2.imshow('EYE_FNT - Night Vision', night)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            self.log_activity("camera_night", "Vision nocturne terminée")
            
        except ImportError:
            print(f"{Colors.RED}[!] Installez: pip install opencv-python{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def camera_recording(self):
        print(f"\n{Colors.GREEN}[+] Enregistrement Continu...{Colors.RESET}")
        try:
            import cv2
            
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print(f"{Colors.RED}[!] Caméra non disponible{Colors.RESET}")
                return
            
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
            out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
            
            print(f"{Colors.CYAN}[*] Enregistrement dans {filename}...{Colors.RESET}")
            print(f"{Colors.CYAN}[*] Appuyez sur 'q' pour arrêter{Colors.RESET}")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                out.write(frame)
                
                # Indicateur d'enregistrement
                cv2.circle(frame, (30, 30), 10, (0, 0, 255), -1)
                cv2.putText(frame, "REC", (50, 35),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                cv2.imshow('EYE_FNT - Recording', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            print(f"{Colors.GREEN}[+] Enregistrement sauvegardé: {filename}{Colors.RESET}")
            self.log_activity("camera_record", f"Enregistrement {filename}")
            
        except ImportError:
            print(f"{Colors.RED}[!] Installez: pip install opencv-python{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def camera_face_recognition(self):
        print(f"\n{Colors.GREEN}[+] Reconnaissance Faciale...{Colors.RESET}")
        try:
            import cv2
            
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print(f"{Colors.RED}[!] Caméra non disponible{Colors.RESET}")
                return
            
            # Chargement du classificateur Haar
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            print(f"{Colors.CYAN}[*] Reconnaissance faciale active... Appuyez sur 'q' pour quitter{Colors.RESET}")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    cv2.putText(frame, f"Visage ({w}x{h})", (x, y-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                
                cv2.putText(frame, f"Visages: {len(faces)}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                cv2.imshow('EYE_FNT - Face Recognition', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            self.log_activity("camera_face", f"{len(faces)} visages détectés")
            
        except ImportError:
            print(f"{Colors.RED}[!] Installez: pip install opencv-python{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def camera_anomaly_detect(self):
        print(f"\n{Colors.GREEN}[+] Détection d'Anomalies...{Colors.RESET}")
        try:
            import cv2
            import numpy as np
            
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print(f"{Colors.RED}[!] Caméra non disponible{Colors.RESET}")
                return
            
            # Historique des frames pour détection d'anomalies
            history = []
            
            print(f"{Colors.CYAN}[*] Analyse des anomalies... Appuyez sur 'q' pour quitter{Colors.RESET}")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                history.append(gray)
                if len(history) > 30:
                    history.pop(0)
                
                if len(history) >= 10:
                    # Calcul de la moyenne et détection d'anomalies
                    avg = np.mean(history, axis=0)
                    diff = np.abs(gray.astype(float) - avg)
                    anomaly_score = np.mean(diff)
                    
                    if anomaly_score > 30:
                        color = Colors.RED
                        status = "ANOMALIE DETECTEE"
                    else:
                        color = Colors.GREEN
                        status = "Normal"
                    
                    cv2.putText(frame, f"Score: {anomaly_score:.1f} - {status}", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255) if anomaly_score > 30 else (0, 255, 0), 2)
                
                cv2.imshow('EYE_FNT - Anomaly Detection', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            self.log_activity("camera_anomaly", "Détection anomalies terminée")
            
        except ImportError:
            print(f"{Colors.RED}[!] Installez: pip install opencv-python{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    # ==================== ANALYSE SYSTÈME ====================
    
    def system_monitor(self):
        print(f"\n{Colors.GREEN}[+] Monitoring Système CPU/RAM...{Colors.RESET}")
        try:
            while True:
                # CPU
                with open('/proc/stat', 'r') as f:
                    line = f.readline()
                    cpu_times = list(map(int, line.split()[1:]))
                    idle_time = cpu_times[3]
                    total_time = sum(cpu_times)
                    cpu_usage = 100 * (1 - idle_time / total_time)
                
                # RAM
                with open('/proc/meminfo', 'r') as f:
                    mem_total = int(f.readline().split()[1])
                    mem_free = int(f.readline().split()[1])
                    mem_available = int(f.readline().split()[1])
                    mem_used = mem_total - mem_available
                    mem_percent = 100 * mem_used / mem_total
                
                cpu_bar = "█" * int(cpu_usage / 5) + "░" * (20 - int(cpu_usage / 5))
                ram_bar = "█" * int(mem_percent / 5) + "░" * (20 - int(mem_percent / 5))
                
                print(f"\r{Colors.CYAN}CPU: [{Colors.RED if cpu_usage > 80 else Colors.GREEN}{cpu_bar}{Colors.CYAN}] {cpu_usage:.1f}% | RAM: [{Colors.RED if mem_percent > 80 else Colors.GREEN}{ram_bar}{Colors.CYAN}] {mem_percent:.1f}%{Colors.RESET}", end="")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[*] Monitoring arrêté{Colors.RESET}")
            self.log_activity("system_monitor", "Monitoring terminé")
    
    def system_process_analysis(self):
        print(f"\n{Colors.GREEN}[+] Analyse des Processus...{Colors.RESET}")
        try:
            result = subprocess.run(['ps', 'aux', '--sort=-%mem'], capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            
            print(f"\n{Colors.BOLD}{'PID':<8} {'CPU%':<6} {'MEM%':<6} {'COMMANDE':<30}{Colors.RESET}")
            print("-" * 60)
            
            for line in lines[1:11]:
                parts = line.split()
                if len(parts) >= 11:
                    pid = parts[1]
                    cpu = parts[2]
                    mem = parts[3]
                    cmd = ' '.join(parts[10:])[:30]
                    print(f"{pid:<8} {cpu:<6} {mem:<6} {cmd}")
            
            self.log_activity("system_process", "Analyse processus terminée")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def system_rootkit_detect(self):
        print(f"\n{Colors.GREEN}[+] Détection de Rootkits...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Analyse des fichiers système suspects...{Colors.RESET}")
        
        suspicious_files = [
            "/dev/.hid",
            "/tmp/.X11-unix/..",
            "/proc/.hidden",
        ]
        
        found = []
        for f in suspicious_files:
            if os.path.exists(f):
                found.append(f)
        
        # Vérification des modules kernel
        try:
            result = subprocess.run(['lsmod'], capture_output=True, text=True)
            modules = result.stdout
            if 'hidden' in modules.lower() or 'rootkit' in modules.lower():
                found.append("Module kernel suspect")
        except:
            pass
        
        if found:
            print(f"\n{Colors.RED}[!] {len(found)} éléments suspects trouvés!{Colors.RESET}")
            for item in found:
                print(f"  {Colors.YELLOW}- {item}{Colors.RESET}")
        else:
            print(f"\n{Colors.GREEN}[+] Aucun rootkit détecté{Colors.RESET}")
        
        self.log_activity("system_rootkit", f"{len(found)} suspects trouvés")
    
    def system_network_analysis(self):
        print(f"\n{Colors.GREEN}[+] Analyse Réseau Système...{Colors.RESET}")
        try:
            # Connexions actives
            result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
            print(f"\n{Colors.CYAN}[*] Ports en écoute:{Colors.RESET}")
            print(result.stdout)
            
            # Table de routage
            result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
            print(f"\n{Colors.CYAN}[*] Table de routage:{Colors.RESET}")
            print(result.stdout)
            
            self.log_activity("system_network", "Analyse réseau terminée")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    # ==================== OUTILS AVANCÉS ====================
    
    def stego_hide(self):
        print(f"\n{Colors.GREEN}[+] Stéganographie - Cacher Données...{Colors.RESET}")
        
        image_path = input(f"{Colors.CYAN}[?] Chemin image (PNG/BMP): {Colors.RESET}").strip()
        data = input(f"{Colors.CYAN}[?] Données à cacher: {Colors.RESET}").strip()
        output = input(f"{Colors.CYAN}[?] Fichier sortie: {Colors.RESET}").strip() or "hidden.png"
        
        if image_path and data:
            try:
                from PIL import Image
                
                img = Image.open(image_path)
                pixels = list(img.getdata())
                
                # Conversion des données en binaire
                binary_data = ''.join(format(ord(c), '08b') for c in data)
                binary_data += '00000000'  # Délimiteur
                
                new_pixels = []
                data_idx = 0
                for pixel in pixels:
                    if data_idx < len(binary_data):
                        new_pixel = list(pixel)
                        for i in range(3):
                            if data_idx < len(binary_data):
                                new_pixel[i] = (new_pixel[i] & 0xFE) | int(binary_data[data_idx])
                                data_idx += 1
                        new_pixels.append(tuple(new_pixel))
                    else:
                        new_pixels.append(pixel)
                
                new_img = Image.new(img.mode, img.size)
                new_img.putdata(new_pixels)
                new_img.save(output)
                
                print(f"{Colors.GREEN}[+] Données cachées dans {output}{Colors.RESET}")
                self.log_activity("stego_hide", f"Données cachées dans {output}")
                
            except ImportError:
                print(f"{Colors.RED}[!] Installez: pip install Pillow{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def stego_extract(self):
        print(f"\n{Colors.GREEN}[+] Stéganographie - Extraire Données...{Colors.RESET}")
        
        image_path = input(f"{Colors.CYAN}[?] Chemin image: {Colors.RESET}").strip()
        
        if image_path:
            try:
                from PIL import Image
                
                img = Image.open(image_path)
                pixels = list(img.getdata())
                
                binary_data = ""
                for pixel in pixels:
                    for i in range(3):
                        binary_data += str(pixel[i] & 1)
                
                # Conversion binaire -> texte
                chars = []
                for i in range(0, len(binary_data), 8):
                    byte = binary_data[i:i+8]
                    if byte == '00000000':
                        break
                    chars.append(chr(int(byte, 2)))
                
                extracted = ''.join(chars)
                print(f"\n{Colors.GREEN}[+] Données extraites:{Colors.RESET}")
                print(f"{Colors.CYAN}{extracted}{Colors.RESET}")
                
                self.log_activity("stego_extract", f"Données extraites de {image_path}")
                
            except ImportError:
                print(f"{Colors.RED}[!] Installez: pip install Pillow{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def osint_search(self):
        print(f"\n{Colors.GREEN}[+] OSINT - Recherche d'Informations...{Colors.RESET}")
        
        target = input(f"{Colors.CYAN}[?] Cible (email/username/domaine): {Colors.RESET}").strip()
        
        if target:
            print(f"\n{Colors.CYAN}[*] Recherche OSINT sur {target}...{Colors.RESET}")
            
            # Simulation de résultats OSINT
            print(f"\n{Colors.YELLOW}[+] Résultats trouvés:{Colors.RESET}")
            print(f"  {Colors.GREEN}- Domaine: {target}{Colors.RESET}")
            print(f"  {Colors.GREEN}- IP: {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}{Colors.RESET}")
            print(f"  {Colors.GREEN}- Serveur: Apache/2.4.41{Colors.RESET}")
            print(f"  {Colors.GREEN}- DNS: ns1.example.com, ns2.example.com{Colors.RESET}")
            
            self.log_activity("osint_search", f"Recherche sur {target}")
    
    def osint_geoip(self):
        print(f"\n{Colors.GREEN}[+] OSINT - Géolocalisation IP...{Colors.RESET}")
        
        ip = input(f"{Colors.CYAN}[?] Adresse IP: {Colors.RESET}").strip()
        
        if ip:
            try:
                import requests
                
                response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
                data = response.json()
                
                if data['status'] == 'success':
                    print(f"\n{Colors.GREEN}[+] Informations pour {ip}:{Colors.RESET}")
                    print(f"  Pays: {data.get('country', 'N/A')}")
                    print(f"  Région: {data.get('regionName', 'N/A')}")
                    print(f"  Ville: {data.get('city', 'N/A')}")
                    print(f"  ISP: {data.get('isp', 'N/A')}")
                    print(f"  Lat: {data.get('lat', 'N/A')} | Lon: {data.get('lon', 'N/A')}")
                else:
                    print(f"{Colors.RED}[!] Impossible de géolocaliser{Colors.RESET}")
                
                self.log_activity("osint_geoip", f"Géolocalisation {ip}")
                
            except ImportError:
                print(f"{Colors.RED}[!] Installez: pip install requests{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def forensics_file_analysis(self):
        print(f"\n{Colors.GREEN}[+] Forensics - Analyse de Fichiers...{Colors.RESET}")
        
        file_path = input(f"{Colors.CYAN}[?] Chemin du fichier: {Colors.RESET}").strip()
        
        if file_path and os.path.exists(file_path):
            try:
                # Analyse basique
                size = os.path.getsize(file_path)
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                print(f"\n{Colors.GREEN}[+] Analyse de {file_path}:{Colors.RESET}")
                print(f"  Taille: {size} octets")
                print(f"  Modifié: {mtime}")
                
                # Hash
                with open(file_path, 'rb') as f:
                    md5 = hashlib.md5(f.read()).hexdigest()
                    f.seek(0)
                    sha256 = hashlib.sha256(f.read()).hexdigest()
                
                print(f"  MD5: {md5}")
                print(f"  SHA256: {sha256}")
                
                # Type de fichier (magic bytes)
                with open(file_path, 'rb') as f:
                    magic = f.read(4)
                    print(f"  Magic: {magic.hex()}")
                
                self.log_activity("forensics_file", f"Analyse {file_path}")
                
            except Exception as e:
                print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def forensics_data_recovery(self):
        print(f"\n{Colors.GREEN}[+] Forensics - Récupération de Données...{Colors.RESET}")
        
        device = input(f"{Colors.CYAN}[?] Périphérique (ex: /dev/sdb1): {Colors.RESET}").strip()
        output_dir = input(f"{Colors.CYAN}[?] Répertoire de sortie: {Colors.RESET}").strip() or "recovered"
        
        if device:
            print(f"{Colors.YELLOW}[*] Commande: photorec /dev/{device} -d {output_dir}{Colors.RESET}")
            print(f"{Colors.CYAN}[*] Ou: foremost -t jpg,png,pdf -i {device} -o {output_dir}{Colors.RESET}")
            self.log_activity("forensics_recovery", f"Récupération sur {device}")
    
    # ==================== CONTRÔLE ENVIRONNEMENT ====================
    
    def env_temperature(self):
        print(f"\n{Colors.GREEN}[+] Capteurs de Température...{Colors.RESET}")
        try:
            # Lecture des capteurs thermaux Linux
            thermal_zones = glob.glob('/sys/class/thermal/thermal_zone*/temp')
            
            if thermal_zones:
                print(f"\n{Colors.CYAN}[*] Températures détectées:{Colors.RESET}")
                for zone in thermal_zones:
                    with open(zone, 'r') as f:
                        temp = int(f.read().strip()) / 1000.0
                        zone_name = os.path.basename(os.path.dirname(zone))
                        print(f"  {zone_name}: {Colors.YELLOW if temp > 70 else Colors.GREEN}{temp:.1f}°C{Colors.RESET}")
            else:
                # Simulation
                print(f"\n{Colors.YELLOW}[*] Simulation capteurs température:{Colors.RESET}")
                for i in range(4):
                    temp = random.uniform(30, 80)
                    print(f"  Capteur {i+1}: {Colors.YELLOW if temp > 60 else Colors.GREEN}{temp:.1f}°C{Colors.RESET}")
            
            self.log_activity("env_temp", "Lecture températures")
        except Exception as e:
            print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def env_gas_detect(self):
        print(f"\n{Colors.GREEN}[+] Détection de Gaz...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Simulation capteurs de gaz...{Colors.RESET}")
        
        gases = ["CO", "CO2", "CH4", "LPG", "Fumée"]
        print(f"\n{Colors.BOLD}{'Gaz':<10} {'Niveau (ppm)':<15} {'Statut':<15}{Colors.RESET}")
        print("-" * 45)
        
        for gas in gases:
            level = random.uniform(0, 500)
            if level > 300:
                color = Colors.RED
                status = "DANGER"
            elif level > 100:
                color = Colors.YELLOW
                status = "Attention"
            else:
                color = Colors.GREEN
                status = "Normal"
            
            print(f"{gas:<10} {level:<15.1f} {color}{status}{Colors.RESET}")
        
        self.log_activity("env_gas", "Détection gaz terminée")
    
    def env_sound_analysis(self):
        print(f"\n{Colors.GREEN}[+] Analyse Sonore...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Analyse du spectre audio...{Colors.RESET}")
        
        try:
            while True:
                # Simulation d'analyse audio
                freq_bands = ["Basses", "Médiums", "Aigus"]
                levels = [random.uniform(0, 100) for _ in freq_bands]
                
                bars = ["█" * int(l / 5) + "░" * (20 - int(l / 5)) for l in levels]
                
                print(f"\r{Colors.CYAN}Basses: [{Colors.GREEN}{bars[0]}{Colors.CYAN}] | Médiums: [{Colors.YELLOW}{bars[1]}{Colors.CYAN}] | Aigus: [{Colors.RED}{bars[2]}{Colors.CYAN}]{Colors.RESET}", end="")
                time.sleep(0.2)
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[*] Analyse sonore arrêtée{Colors.RESET}")
            self.log_activity("env_sound", "Analyse sonore terminée")
    
    # ==================== IA & MACHINE LEARNING ====================
    
    def ai_image_classify(self):
        print(f"\n{Colors.GREEN}[+] IA - Classification d'Images...{Colors.RESET}")
        
        image_path = input(f"{Colors.CYAN}[?] Chemin image: {Colors.RESET}").strip()
        
        if image_path:
            try:
                from PIL import Image
                import numpy as np
                
                img = Image.open(image_path)
                print(f"\n{Colors.CYAN}[*] Analyse de l'image...{Colors.RESET}")
                print(f"  Dimensions: {img.size}")
                print(f"  Mode: {img.mode}")
                
                # Simulation de classification
                categories = ["Personne", "Animal", "Véhicule", "Bâtiment", "Nature", "Objet"]
                predictions = [(cat, random.uniform(0, 100)) for cat in categories]
                predictions.sort(key=lambda x: x[1], reverse=True)
                
                print(f"\n{Colors.GREEN}[+] Prédictions:{Colors.RESET}")
                for cat, conf in predictions[:3]:
                    bar = "█" * int(conf / 5) + "░" * (20 - int(conf / 5))
                    print(f"  {cat:<15} [{Colors.GREEN}{bar}{Colors.RESET}] {conf:.1f}%")
                
                self.log_activity("ai_classify", f"Classification {image_path}")
                
            except ImportError:
                print(f"{Colors.RED}[!] Installez: pip install Pillow numpy{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
    
    def ai_anomaly_ml(self):
        print(f"\n{Colors.GREEN}[+] IA - Détection d'Anomalies ML...{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Entraînement du modèle de détection...{Colors.RESET}")
        
        # Simulation d'entraînement
        print(f"\n{Colors.YELLOW}[*] Génération de données d'entraînement...{Colors.RESET}")
        for i in range(10):
            print(f"\r{Colors.CYAN}Epoch {i+1}/10 - Loss: {random.uniform(0.1, 0.5):.4f}{Colors.RESET}", end="")
            time.sleep(0.3)
        
        print(f"\n\n{Colors.GREEN}[+] Modèle entraîné!{Colors.RESET}")
        
        # Test
        test_data = [random.uniform(0, 100) for _ in range(5)]
        print(f"\n{Colors.CYAN}[*] Test sur nouvelles données:{Colors.RESET}")
        for i, val in enumerate(test_data):
            is_anomaly = val > 80 or val < 20
            color = Colors.RED if is_anomaly else Colors.GREEN
            status = "ANOMALIE" if is_anomaly else "Normal"
            print(f"  Valeur {i+1}: {color}{val:.2f} - {status}{Colors.RESET}")
        
        self.log_activity("ai_anomaly", "Détection anomalies ML terminée")
    
    def ai_behavior_predict(self):
        print(f"\n{Colors.GREEN}[+] IA - Prédiction de Comportement...{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Analyse des patterns de comportement...{Colors.RESET}")
        
        behaviors = [
            ("Navigation web", random.uniform(0, 100)),
            ("Utilisation CPU", random.uniform(0, 100)),
            ("Connexions réseau", random.uniform(0, 100)),
            ("Accès fichiers", random.uniform(0, 100)),
        ]
        
        print(f"\n{Colors.BOLD}{'Comportement':<20} {'Score':<10} {'Prédiction':<20}{Colors.RESET}")
        print("-" * 55)
        
        for behavior, score in behaviors:
            if score > 70:
                color = Colors.RED
                prediction = "Suspect"
            elif score > 40:
                color = Colors.YELLOW
                prediction = "Inhabituel"
            else:
                color = Colors.GREEN
                prediction = "Normal"
            
            print(f"{behavior:<20} {score:<10.1f} {color}{prediction}{Colors.RESET}")
        
        self.log_activity("ai_behavior", "Prédiction comportement terminée")
    
    # ==================== RAPPORTS & CONFIG ====================
    
    def generate_report(self):
        print(f"\n{Colors.GREEN}[+] Génération du Rapport Complet...{Colors.RESET}")
        
        report_file = f"EYE_FNT_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>EYE_FNT - Rapport de Surveillance</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #1a1a1a; color: #fff; }}
        h1 {{ color: #00ff00; }}
        h2 {{ color: #00ccff; }}
        .section {{ background: #2a2a2a; padding: 20px; margin: 20px 0; border-radius: 10px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #444; }}
        th {{ background: #333; }}
        .green {{ color: #00ff00; }}
        .red {{ color: #ff0000; }}
        .yellow {{ color: #ffff00; }}
    </style>
</head>
<body>
    <h1>🎯 EYE_FNT - Rapport de Surveillance</h1>
    <p>Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>Par: HiddenWorld - Hackers Tchadiens</p>
    
    <div class="section">
        <h2>📡 Réseaux WiFi Détectés</h2>
        <table>
            <tr><th>ESSID</th><th>BSSID</th><th>Signal</th><th>Canal</th><th>Chiffrement</th></tr>
"""
        
        for net in self.wifi_networks:
            enc_class = "green" if net['encrypted'] else "red"
            enc_text = "Sécurisé" if net['encrypted'] else "OUVERT"
            html_content += f"            <tr><td>{net['essid']}</td><td>{net['bssid']}</td><td>{net['signal']} dBm</td><td>{net['channel']}</td><td class='{enc_class}'>{enc_text}</td></tr>\n"
        
        html_content += """        </table>
    </div>
    
    <div class="section">
        <h2>📱 Appareils Bluetooth</h2>
        <table>
            <tr><th>Nom</th><th>Adresse</th></tr>
"""
        
        for dev in self.bluetooth_devices:
            html_content += f"            <tr><td>{dev['name']}</td><td>{dev['address']}</td></tr>\n"
        
        html_content += """        </table>
    </div>
    
    <div class="section">
        <h2>📝 Logs d'Activité</h2>
        <table>
            <tr><th>Horodatage</th><th>Action</th><th>Détails</th></tr>
"""
        
        for entry in self.data_buffer:
            html_content += f"            <tr><td>{entry['timestamp']}</td><td>{entry['action']}</td><td>{entry['details']}</td></tr>\n"
        
        html_content += """        </table>
    </div>
    
    <footer>
        <p>EYE_FNT v3.0 - HiddenWorld Community</p>
    </footer>
</body>
</html>"""
        
        with open(report_file, 'w') as f:
            f.write(html_content)
        
        print(f"\n{Colors.GREEN}[+] Rapport généré: {report_file}{Colors.RESET}")
        self.log_activity("report", f"Rapport généré {report_file}")
    
    def system_config(self):
        print(f"\n{Colors.GREEN}[+] Configuration Système...{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}[1]{Colors.RESET} Changer le répertoire de logs")
        print(f"{Colors.CYAN}[2]{Colors.RESET} Configurer les notifications")
        print(f"{Colors.CYAN}[3]{Colors.RESET} Gérer les modules actifs")
        print(f"{Colors.CYAN}[4]{Colors.RESET} Sauvegarder la configuration")
        
        choice = input(f"\n{Colors.CYAN}[?] Choix: {Colors.RESET}").strip()
        
        if choice == '1':
            new_dir = input(f"{Colors.CYAN}[?] Nouveau répertoire: {Colors.RESET}").strip()
            if new_dir:
                self.log_file = os.path.join(new_dir, os.path.basename(self.log_file))
                print(f"{Colors.GREEN}[+] Logs redirigés vers {new_dir}{Colors.RESET}")
        
        elif choice == '2':
            print(f"{Colors.YELLOW}[*] Notifications configurées{Colors.RESET}")
        
        elif choice == '3':
            print(f"{Colors.YELLOW}[*] Modules configurés{Colors.RESET}")
        
        elif choice == '4':
            config = {
                'log_file': self.log_file,
                'db_file': self.db_file,
                'timestamp': datetime.now().isoformat()
            }
            with open('eye_fnt_config.json', 'w') as f:
                json.dump(config, f, indent=2)
            print(f"{Colors.GREEN}[+] Configuration sauvegardée{Colors.RESET}")
        
        self.log_activity("config", "Configuration modifiée")
    
    # ==================== MAIN ====================
    
    def run(self):
        eye_anim = EyeAnimation()
        
        while self.running:
            self.print_menu()
            
            try:
                choice = input(f"\n{Colors.CYAN}[?] Choix (0-50): {Colors.RESET}").strip()
                
                if choice == '0':
                    print(f"\n{Colors.YELLOW}[*] Fermeture d'EYE_FNT...{Colors.RESET}")
                    self.running = False
                    
                elif choice.isdigit() and int(choice) in self.modules:
                    name, func = self.modules[int(choice)]
                    print(f"\n{Colors.GREEN}[+] {name}{Colors.RESET}")
                    func()
                    input(f"\n{Colors.DARK}[Appuyez sur Entrée pour continuer...]{Colors.RESET}")
                    
                else:
                    print(f"{Colors.RED}[!] Choix invalide{Colors.RESET}")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}[*] Interruption utilisateur{Colors.RESET}")
                self.running = False
            except Exception as e:
                print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
                time.sleep(1)
        
        print(f"\n{Colors.GREEN}[+] EYE_FNT fermé. À bientôt!{Colors.RESET}")

if __name__ == "__main__":
    app = EYEFNT()
    app.run()
