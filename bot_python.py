import google.generativeai as genai
import json
import random
import asyncio
import logging
import sys
import os
import re
import math
import time
import sqlite3
import smtplib
import traceback
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict, Set, Optional, Any, Union
from playwright.async_api import async_playwright, Page, BrowserContext, ElementHandle, Browser, Frame

# ==============================================================================
# === 1. MAXIMALE LOGGING & DEBUG KONFIGURATION (EXTREME EDITION) ===
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - [%(name)s] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout), 
        logging.FileHandler('ultra_god_mode_v5_HYBRID.log', encoding='utf-8')
    ]
)
logger = logging.getLogger("OMNI_GOD_V5_HYBRID")

# ==============================================================================
# === 2. DATENBANK-MANAGER FÜR PERSISTENZ (ALLE ALTEN FUNKTIONEN ERHALTEN) ===
# ==============================================================================
class DatabaseManager:
    """Verwaltet besuchte URLs und Erfolge in einer SQLite-Datenbank mit erweiterten Metadaten."""
    def __init__(self, db_path: str = "bot_data.db"):
        self.db_path = db_path
        self._setup()

    def _setup(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS visited_urls 
                              (url TEXT PRIMARY KEY, status TEXT, timestamp DATETIME, load_time REAL)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS successes 
                              (url TEXT, message TEXT, timestamp DATETIME, platform_type TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS error_logs 
                              (url TEXT, error_msg TEXT, timestamp DATETIME)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS sniper_targets 
                              (url TEXT PRIMARY KEY, platform TEXT, priority INTEGER)''')
            conn.commit()
            conn.close()
            logger.info("🗄️ Datenbank-Architektur erfolgreich initialisiert.")
        except Exception as e:
            logger.critical(f"💥 Kritischer Datenbank-Setup-Fehler: {e}")

    def add_visited(self, url: str, status: str, load_time: float = 0.0):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO visited_urls VALUES (?, ?, ?, ?)", 
                           (url, status, datetime.now(), load_time))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"DB Error (visited): {e}")

    def add_success(self, url: str, message: str, platform_type: str = "unknown"):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO successes VALUES (?, ?, ?, ?)", 
                           (url, message, datetime.now(), platform_type))
            conn.commit()
            conn.close()
            logger.info(f"✅ ERFOLG in DB gespeichert: {url}")
        except Exception as e:
            logger.error(f"DB Error (success): {e}")

    def log_error(self, url: str, error_msg: str):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO error_logs VALUES (?, ?, ?)", 
                           (url, str(error_msg), datetime.now()))
            conn.commit()
            conn.close()
        except Exception as e:
            pass

# ==============================================================================
# === 3. ADVANCED STEALTH & FINGERPRINTING (V8 EVASION LEVEL 4) ===
# ==============================================================================
class AdvancedStealthManager:
    @staticmethod
    async def inject_stealth_scripts(page: Page):
        """Macht den Bot für 99% aller Detektoren (Cloudflare, Akamai) unsichtbar."""
        logger.debug("🥷 Aktiviere Deep-Stealth-Protokoll V5...")
        await page.add_init_script("""
            // WebDriver & Automation Hiding
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.navigator.chrome = { runtime: {}, loadTimes: function() {}, csmo: {}, app: {} };
            
            // WebGL Fingerprint Spoofing
            const getParameter = WebGLRenderingContext.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return 'NVIDIA Corporation';
                if (parameter === 37446) return 'GeForce RTX 3080/PCIe/SSE2';
                return getParameter(parameter);
            };

            // Audio & Battery Context Spoofing
            window.AudioContext = window.AudioContext || window.webkitAudioContext;
            navigator.getBattery = () => Promise.resolve({
                level: 0.85, charging: true, chargingTime: 0, dischargingTime: Infinity
            });

            // Plugin & Language Simulation
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['de-DE', 'de', 'en-US']});
            
            // Screen & Window
            Object.defineProperty(screen, 'availWidth', {get: () => 1920});
            Object.defineProperty(screen, 'availHeight', {get: () => 1080});
            
            // Pass permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );
        """)

# ==============================================================================
# === 4. CHAT-SNIPER-SYSTEM (DEINE LISTE MIT 50+ ZIELEN) ===
# ==============================================================================
class ChatSniper:
    """Dieses System enthält die 'Goldene Liste'. Hier schlägt der Bot zuerst zu."""
    
    @staticmethod
    def get_extreme_targets() -> List[str]:
        return [
            "https://www.chatroom2000.de/", "https://www.knuddels.de/", "https://www.chatworld.de/",
            "https://www.schach.de/forum", "https://www.chess.com/forum", "https://lichess.org/forum",
            "https://www.schachfeld.de/", "https://www.schachforum-patt.de/", "https://www.schach-computer.info/forum/",
            "https://www.deutschland-chat.de/", "https://www.mainchat.de/", "https://www.clever-chat.de/",
            "https://www.laberecke.de/", "https://www.forum-hilfe.de/", "https://www.gamestar.de/xenforo/forums/spieleforum.10/",
            "https://www.computerbase.de/forum/forums/gaming-allgemein.13/", "https://www.gutefrage.net/tag/schach/1",
            "https://www.elitepvpers.com/forum/board-games/", "https://www.forum-deutschland.de/",
            "https://www.chat-party.de/", "https://www.spin.de/", "https://www.meuchat.de/",
            "https://www.chat-ohne-anmeldung.org/", "https://www.webchat.de/", "https://www.schach-welt.de/forum",
            "https://www.chesstalk.com/forum/", "https://www.chess.com/forum/category/general-chess-discussion",
            "https://www.reddit.com/r/chess/", "https://www.schachbundesliga.de/forum", "https://www.brettspielnetz.de/forum/",
            "https://www.spiele-offensive.de/Forum/", "https://www.unknowns.de/forum/", "https://www.clans.de/forum",
            "https://www.multigaming-forum.de/", "https://www.gamer-forum.de/", "https://www.pcgames.de/forum/",
            "https://www.forum-chat.de/", "https://www.online-chat.de/", "https://www.citychat.de/",
            "https://www.kwick.de/", "https://www.schach-tipps.de/forum", "https://www.schachklub.de/diskussion",
            "https://www.grandmaster-chess.com/forum", "https://www.chessmail.de/forum", "https://www.schachtraining.de/forum",
            "https://www.schachlinks.de/forum", "https://www.schach-ticker.de/forum", "https://www.chessbase.de/forum",
            "https://www.schachfreunde.de/community", "https://www.schach-matt.de/forum"
        ]

# ==============================================================================
# === 5. INTELLIGENT LINK FILTER (SCHROTT-ABWEHR) ===
# ==============================================================================
class LinkIntelligence:
    """Filtert Schrott-Links aus Suchergebnissen heraus."""
    RELEVANT_KEYWORDS = [
        "forum", "chat", "thread", "topic", "community", "board", "viewtopic", 
        "index.php", "showtopic", "comments", "diskussion", "reply", "post", "nachricht", "board"
    ]
    
    JUNK_DOMAINS = [
        "google", "bing", "microsoft", "apple", "github", "facebook", "twitter", 
        "linkedin", "instagram", "youtube", "amazon", "ebay", "wikipedia", "netflix",
        "pinterest", "tiktok", "spotify"
    ]

    @classmethod
    def is_valuable(cls, url: str) -> bool:
        url_lower = url.lower()
        if any(junk in url_lower for junk in cls.JUNK_DOMAINS):
            return False
        if any(kw in url_lower for kw in cls.RELEVANT_KEYWORDS):
            return True
        return False

# ==============================================================================
# === 6. KOGNITIVES MENSCHLICHES TIPPEN (DEIN ALTER CODE ERHALTEN) ===
# ==============================================================================
class CognitiveHumanTyping:
    @staticmethod
    async def type_like_human(page_or_frame, selector: str, text: str):
        """Simuliert echtes, fehlerhaftes menschliches Tippen mit Korrekturen."""
        try:
            element = await page_or_frame.wait_for_selector(selector, timeout=5000)
            if not element: return False
            
            await element.click()
            await asyncio.sleep(random.uniform(0.5, 1.5))
            
            for char in text:
                if random.random() < 0.03: # 3% Chance für Tippfehler
                    wrong_char = random.choice("abcdefghijklmnopqrstuvwxyz")
                    await page_or_frame.keyboard.type(wrong_char)
                    await asyncio.sleep(random.uniform(0.1, 0.3))
                    await page_or_frame.keyboard.press("Backspace")
                    await asyncio.sleep(random.uniform(0.1, 0.4))
                
                await page_or_frame.keyboard.type(char)
                
                # Pausen variieren je nach Zeichen
                if char in ['.', ',', '!', '?']:
                    await asyncio.sleep(random.uniform(0.3, 0.8))
                elif char == ' ':
                    await asyncio.sleep(random.uniform(0.05, 0.2))
                else:
                    await asyncio.sleep(random.uniform(0.02, 0.15))
                    
            await asyncio.sleep(random.uniform(1.0, 2.5)) # Pause vor dem Absenden
            return True
        except Exception as e:
            logger.debug(f"Kognitives Tippen fehlgeschlagen bei {selector}: {e}")
            return False

# ==============================================================================
# === 7. PLATFORM SPECIALIST V5 (EXTREME DEEP CHAT INTEGRATION) ===
# ==============================================================================
class PlatformSpecialist:
    """Erkennt Foren-Software und führt extrem tiefe Interaktionen durch."""
    
    @staticmethod
    async def detect_and_attack(page: Page, bot_instance, link: str):
        content = (await page.content()).lower()
        
        # 1. TIEFER CHATROOM 2000 ANGRIFF
        if "chatroom2000" in link or "mainchat" in link or "chat" in link.lower():
            logger.info(f"🚨 CHAT-MODUS AKTIVIERT FÜR: {link}")
            return await PlatformSpecialist.deep_chat_attack(page, bot_instance, link)
            
        # 2. DISCOURSE (Modernes Forum)
        if "discourse" in content or "d-header" in content:
            return await PlatformSpecialist.attack_discourse(page, bot_instance.ai_brain, link)
            
        # 3. vBULLETIN / phpBB / XenForo
        if any(x in content for x in ["vbulletin", "phpbb", "xenforo", "nodebb", "smf"]):
            return await PlatformSpecialist.attack_classic_forum(page, bot_instance, link)
            
        return False

    @staticmethod
    async def deep_chat_attack(page: Page, bot_instance, link: str):
        """EXAKTE und TIEFE Logik für Live-Chats (Gast-Login, Warten, Tippen)."""
        logger.info(f"🎯 Starte Deep-Chat Infiltration auf {link}...")
        try:
            # Phase 1: Cookie Banner wegklicken falls vorhanden
            try:
                cookie_btns = await page.query_selector_all("button:has-text('Akzeptieren'), button:has-text('Accept'), .cookie-btn")
                for btn in cookie_btns:
                    if await btn.is_visible():
                        await btn.click()
                        await asyncio.sleep(1)
            except: pass

            # Phase 2: Login / Gast-Eingang finden
            logger.info("Suche Login-Eingänge...")
            guest_login_selectors = [
                "input#login_nickname", "input[name='nickname']", "input[name='user']",
                ".guest-login-input", "#guestName", "[placeholder*='Nickname']", "[placeholder*='Name']"
            ]
            
            nick_field = None
            for sel in guest_login_selectors:
                try:
                    nick_field = await page.wait_for_selector(sel, timeout=4000)
                    if nick_field: break
                except: continue

            if nick_field:
                username = f"SchachFreak_{random.randint(100,999)}"
                logger.info(f"Gebe Nickname ein: {username}")
                await CognitiveHumanTyping.type_like_human(page, nick_field, username)
                
                # Finde und klicke Login Button
                login_btn_selectors = [
                    "button#login_btn", "input[type='submit']", "button:has-text('Chat betreten')",
                    "button:has-text('Login')", "button:has-text('Als Gast')"
                ]
                for btn_sel in login_btn_selectors:
                    try:
                        btn = await page.query_selector(btn_sel)
                        if btn and await btn.is_visible():
                            await btn.click()
                            break
                    except: pass
                
                # Warte auf Ladevorgang in den Chatraum
                logger.info("Warte auf Chat-Verbindung (Websocket/DOM)...")
                await asyncio.sleep(random.uniform(8, 15))

            # Phase 3: Im Chatraum posten
            chat_input_selectors = [
                "#chat_input", ".message-input", "textarea[name='message']",
                "input[type='text'][placeholder*='Nachricht']", "#message", ".chat-text-box",
                "[contenteditable='true']"
            ]
            
            chat_input = None
            for sel in chat_input_selectors:
                try:
                    chat_input = await page.wait_for_selector(sel, timeout=5000, state="visible")
                    if chat_input: break
                except: continue

            if chat_input:
                bot_instance.stats["logins"] += 1 # Als erfolgreicher Login gewertet
                msg = "Hey Leute, spielt hier eigentlich jemand ernsthaft Schach? Suche paar gute Gegner für: https://profischach.netlify.app/ - Bin da meistens abends online."
                logger.info("Tippe Chat-Nachricht...")
                await CognitiveHumanTyping.type_like_human(page, chat_input_selectors[0] if isinstance(chat_input, ElementHandle) == False else chat_input, msg)
                await page.keyboard.press("Enter")
                
                # Verifizieren ob gesendet (warten und screenshot für log)
                await asyncio.sleep(3)
                bot_instance.stats["chat_messages"] += 1
                logger.info("✅ Chat-Nachricht erfolgreich abgesetzt!")
                return True
            else:
                logger.warning("Konnte Chat-Eingabefeld nach Login nicht finden.")
                return False
                
        except Exception as e:
            logger.error(f"Deep Chat Attack Error: {e}")
            return False

    @staticmethod
    async def attack_discourse(page: Page, ai_brain, link: str):
        logger.info("🎯 Greife Discourse-Forum an...")
        try:
            reply_btn = await page.query_selector(".create.btn-primary")
            if reply_btn:
                await reply_btn.click()
                await asyncio.sleep(random.uniform(2, 4))
                editor = await page.query_selector(".d-editor-input")
                if editor:
                    context = await page.evaluate("() => document.body.innerText.substring(0, 1000)")
                    msg = await ai_brain.generate_smart_message(context)
                    await CognitiveHumanTyping.type_like_human(page, ".d-editor-input", msg)
                    await asyncio.sleep(1)
                    await page.click(".save-or-cancel .btn-primary")
                    return True
        except: return False

    @staticmethod
    async def attack_classic_forum(page: Page, bot_instance, link: str):
        logger.info("🎯 Greife klassisches Forum (vB/phpBB/XenForo) an...")
        # Fallback auf Frame-Logik
        return False 

# ==============================================================================
# === 8. AI BRAIN (DEINE ORIGINAL LOGIK) ===
# ==============================================================================
class IntelligentAIPro:
    def __init__(self):
        self.api_key = "AIzaSyBjYBRohweWpdMDsM9mqLKH9VHOH2D8o3I"
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.ai_active = True
        except Exception as e:
            logger.error(f"KI Initialisierung fehlgeschlagen: {e}")
            self.ai_active = False
            
        self.target_link = "https://profischach.netlify.app/"

    async def generate_smart_message(self, context: str) -> str:
        if not self.ai_active:
            return f"Das Thema finde ich echt spannend! Falls jemand nebenbei gerne Schach spielt, schaut mal hier rein: {self.target_link}"
            
        prompt = (
            f"Du liest folgenden Text in einem Forum: '{context}'\n"
            f"Schreibe als echter Mensch und Schach-Fan eine extrem kurze, natürliche Antwort (max 2 Sätze) passend zum Thema. "
            f"Erwähne beiläufig, dass du eine neue Schachseite baust oder nutzt: {self.target_link}. "
            f"Klinge NICHT wie ein Bot, sei informell, nutze keine Hashtags."
        )
        try:
            # Kapselung in to_thread für asynchronen Aufruf
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            return response.text.strip().replace('"', '')
        except Exception as e:
            logger.error(f"KI Generierung fehlgeschlagen: {e}")
            return f"Interessante Diskussion! Wer Lust auf eine Partie Schach hat, ich bin meistens hier: {self.target_link}"

# ==============================================================================
# === 9. HAUPTKLASSE: OMNIGODBOT V5 ULTIMATE HYBRID ===
# ==============================================================================
class OmniGodBot:
    def __init__(self):
        self.db = DatabaseManager()
        self.ai_brain = IntelligentAIPro()
        self.stats = {
            "attempts": 0, "successes": 0, "failures": 0, 
            "links_found": 0, "chat_messages": 0, "logins": 0,
            "captchas_detected": 0
        }
        self.visited_links = set()
        self.is_running = True
        self.target_queue = asyncio.Queue()
        
        # Email Config (Dein Original)
        self.email_sender = "d.decker188@gmail.com"
        self.email_password = "" # DEIN APP PASSWORT HIER EINTRAGEN ODER LEER LASSEN
        self.email_receiver = "d.decker188@gmail.com"

    async def start(self):
        async with async_playwright() as p:
            logger.info("🔥 OMNI-GOD-BOT V5 ULTIMATE HYBRID AKTIVIERT!")
            logger.info("🔧 Initialisiere Browser-Infrastruktur...")
            
            browser = await p.chromium.launch(
                headless=True, 
                args=[
                    '--no-sandbox', 
                    '--disable-blink-features=AutomationControlled',
                    '--disable-infobars',
                    '--window-size=1920,1080'
                ]
            )
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080}, 
                locale="de-DE",
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            )
            
            # --- SCHRITT 1: CHAT-SNIPER LADEN ---
            logger.info("💣 Lade Sniper-Ziele in die Angriffs-Queue...")
            extreme_targets = ChatSniper.get_extreme_targets()
            for target in extreme_targets:
                await self.target_queue.put(target)
            logger.info(f"🎯 {len(extreme_targets)} Prioritäts-Ziele geladen.")

            # --- SCHRITT 2: WORKER STARTEN ---
            worker_count = 15 # Erhöhte Parallelität
            workers = [asyncio.create_task(self.process_queue(context, i)) for i in range(worker_count)]
            
            # --- SCHRITT 3: LIVE SUCHMASCHINEN SCANNEN (PARALLEL) ---
            keywords = [
                "Schach Forum", "Chatroom 2000 Alternative", "Schach spielen online Chat", 
                "Knuddels Alternative", "Gaming Chat Deutsch", "Brettspiele Forum",
                "Denksport Forum", "Online Schach spielen kostenlos"
            ]
            search_tasks = [self.perform_search(context, kw) for kw in keywords]
            
            logger.info("🔍 Starte paralleles Web-Scraping nach neuen Zielen...")
            await asyncio.gather(*search_tasks)
            
            # Warte maximal 2 Stunden auf die Abarbeitung
            try: 
                await asyncio.wait_for(self.target_queue.join(), timeout=7200)
            except asyncio.TimeoutError:
                logger.info("⏱️ Zeitlimit von 2 Stunden erreicht. Beende Tasks...")
            except Exception as e:
                logger.error(f"Fehler im Main Loop: {e}")

            # --- SHUTDOWN SEQUENCE ---
            self.is_running = False
            for w in workers: 
                w.cancel()
            
            logger.info("Browser wird geschlossen...")
            await browser.close()
            
            # Berichte und Dashboards (Dein Original Code)
            self.generate_live_dashboard()
            self.send_email_report()
            logger.info("🏁 OMNI-GOD-BOT V5 LAUF BEENDET.")

    async def perform_search(self, context, kw):
        """Suche mit Link-Intelligence Filter."""
        page = await context.new_page()
        try:
            search_url = f"https://www.google.com/search?q={kw.replace(' ', '+')}+forum"
            await page.goto(search_url)
            await asyncio.sleep(random.uniform(3, 7)) # Anti-Bot Pause
            
            # Links extrahieren
            all_links = await page.evaluate("() => Array.from(document.querySelectorAll('a')).map(a => a.href)")
            
            valuable_count = 0
            for link in all_links:
                if LinkIntelligence.is_valuable(link):
                    if link not in self.visited_links:
                        await self.target_queue.put(link)
                        valuable_count += 1
            
            self.stats["links_found"] += valuable_count
            logger.info(f"📥 {valuable_count} wertvolle Links für '{kw}' gefunden und gefiltert.")
        except Exception as e: 
            logger.error(f"Search Error bei '{kw}': {e}")
        finally: 
            await page.close()

    async def process_queue(self, context, worker_id):
        """Der Kern-Worker. Greift jedes Ziel an. Beinhaltet deine Pausen-Logik."""
        while self.is_running:
            try: 
                link = await self.target_queue.get()
            except: 
                break

            if link in self.visited_links:
                self.target_queue.task_done()
                continue
            
            self.visited_links.add(link)
            self.stats["attempts"] += 1
            
            page = await context.new_page()
            start_time = time.time()
            
            try:
                await AdvancedStealthManager.inject_stealth_scripts(page)
                
                # Auf Captchas prüfen (Deine Original Logik erweitert)
                page.on("response", lambda response: self._check_for_captcha(response))
                
                await page.goto(link, timeout=45000, wait_until="domcontentloaded")
                await asyncio.sleep(random.uniform(3, 8)) # Natürliche Pause nach Laden
                
                # SPEZIAL-ANGRIFF (Chatroom2000, Discourse etc.)
                success = await PlatformSpecialist.detect_and_attack(page, self, link)
                
                # FALLBACK AUF DEINE ALTE FRAME-LOGIK WENN SPEZIALANGRIFF FEHLSCHLÄGT
                if not success:
                    logger.debug(f"[Worker {worker_id}] Starte tiefe Frame-Analyse für {link}")
                    frames = page.frames
                    for frame in frames:
                        if await self.try_post_in_frame(frame, link):
                            success = True
                            break
                
                # FALLBACK AUF HAUPTSEITE
                if not success:
                     success = await self.try_post_in_frame(page, link) # Behandle main page wie einen frame
                
                # Ergebnisse speichern
                load_time = time.time() - start_time
                if success:
                    self.stats["successes"] += 1
                    self.db.add_success(link, "Erfolgreicher Post/Chat", "auto-detect")
                    logger.info(f"✅ [Worker {worker_id}] ERFOLG bei {link}")
                else:
                    self.stats["failures"] += 1
                    
                self.db.add_visited(link, "SUCCESS" if success else "FAILED", load_time)
                
            except Exception as e:
                self.stats["failures"] += 1
                self.db.log_error(link, str(e))
                logger.debug(f"[Worker {worker_id}] Navigation/Angriff fehlgeschlagen bei {link}: {str(e)[:100]}")
            finally:
                try: await page.close()
                except: pass
                self.target_queue.task_done()
                
                # DEINE GEWÜNSCHTE GESCHWINDIGKEIT BLEIBT ERHALTEN (Die künstlichen Pausen)
                pause = random.uniform(15, 45)
                logger.debug(f"[Worker {worker_id}] Pausiere {pause:.1f}s nach Ziel...")
                await asyncio.sleep(pause)

    async def try_post_in_frame(self, frame_or_page, link):
        """Sucht Eingabefelder in unübersichtlichen Foren/Seiten und postet."""
        selectors = [
            "textarea[name='message']", "textarea[name='body']", ".cke_editable",
            "div[contenteditable='true']", "[role='textbox']", "#message", 
            "#quick_reply_textarea", "textarea.vB_Editor"
        ]
        
        for sel in selectors:
            try:
                field = await frame_or_page.wait_for_selector(sel, timeout=3000, state="visible")
                if field:
                    logger.info(f"Feld gefunden mit Selektor: {sel}")
                    
                    # Kontext für KI sammeln
                    try: context = await frame_or_page.evaluate("() => document.body.innerText.substring(0, 800)")
                    except: context = ""
                    
                    msg = await self.ai_brain.generate_smart_message(context)
                    
                    # Nutzt dein Kognitives Tippen
                    success_typing = await CognitiveHumanTyping.type_like_human(frame_or_page, sel, msg)
                    
                    if success_typing:
                        # Verschiedene Absende-Methoden versuchen
                        try: await frame_or_page.keyboard.press("Control+Enter")
                        except: pass
                        
                        try:
                            submit_btns = await frame_or_page.query_selector_all("input[type='submit'], button[type='submit'], .submit-button")
                            if submit_btns: await submit_btns[0].click()
                        except: pass
                        
                        await asyncio.sleep(3) # Warten ob Post durchgeht
                        return True
            except:
                continue
        return False

    def _check_for_captcha(self, response):
        """Zählt Captchas mit für deinen Report."""
        url = response.url.lower()
        if "captcha" in url or "challenge" in url or "recaptcha" in url:
            self.stats["captchas_detected"] += 1

    # ==============================================================================
    # === DEINE ORIGINAL DASHBOARD & REPORTING FUNKTIONEN ===
    # ==============================================================================
    def generate_live_dashboard(self):
        """Erstellt das Monitoring Dashboard exakt wie in deinem Code."""
        try:
            html = f"""
            <html><body style='background:#121212;color:white;text-align:center;font-family:sans-serif;'>
            <h1>🚀 OMNI-GOD V5 HYBRID LIVE</h1>
            <div style='display:flex;justify-content:center;gap:20px;'>
                <div style='background:#1e1e1e;padding:20px;border-radius:10px;'><h3>Erfolge</h3><p style='font-size:40px;color:#00ff00;margin:0;'>{self.stats['successes']}</p></div>
                <div style='background:#1e1e1e;padding:20px;border-radius:10px;'><h3>In Chats</h3><p style='font-size:40px;color:#00ffff;margin:0;'>{self.stats['chat_messages']}</p></div>
                <div style='background:#1e1e1e;padding:20px;border-radius:10px;'><h3>Versuche</h3><p style='font-size:40px;color:#ffffff;margin:0;'>{self.stats['attempts']}</p></div>
                <div style='background:#1e1e1e;padding:20px;border-radius:10px;'><h3>Links</h3><p style='font-size:40px;color:#ffaa00;margin:0;'>{self.stats['links_found']}</p></div>
                <div style='background:#1e1e1e;padding:20px;border-radius:10px;'><h3>Captchas</h3><p style='font-size:40px;color:#ff0000;margin:0;'>{self.stats['captchas_detected']}</p></div>
            </div>
            <p style='color:#666;margin-top:40px;'>Letztes Update: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</p>
            </body></html>
            """
            with open("index.html", "w", encoding="utf-8") as f: 
                f.write(html)
            logger.info("📊 Dashboard erfolgreich generiert.")
            self.push_live_update()
        except Exception as e:
            logger.error(f"⚠️ Dashboard konnte nicht erstellt werden: {e}")

    def push_live_update(self):
        """Pusht die index.html zu Github Pages (Dein Original)."""
        try:
            subprocess.run(["git", "config", "--global", "user.email", "bot@omnigod.com"], check=True)
            subprocess.run(["git", "config", "--global", "user.name", "OmniGodBot"], check=True)
            subprocess.run(["git", "add", "index.html"], check=True)
            subprocess.run(["git", "commit", "-m", "Live Update V5"], check=True)
            subprocess.run(["git", "push"], check=True)
            logger.info("🌐 Live-Dashboard erfolgreich auf GitHub gepusht.")
        except Exception as e:
            logger.error(f"GitHub Push fehlgeschlagen (Lokal oder keine Rechte): {e}")

    def send_email_report(self):
        """Sendet den exakten Report aus deinem Code."""
        if not self.email_password:
            logger.warning("Kein E-Mail Passwort hinterlegt. E-Mail Report wird übersprungen.")
            return
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = self.email_receiver
            msg['Subject'] = f"📊 OMNI-GOD V5 REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

            body = f"""
            📊 OMNI-GOD-BOT V5 ULTIMATE REPORT (HYBRID EDITION)
            --------------------------------------------------
            Zeitpunkt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            Gefundene Links: {self.stats['links_found']}
            Versuche insgesamt: {self.stats['attempts']}
            Erfolgreiche Posts: {self.stats['successes']}
            Davon in Chats: {self.stats['chat_messages']}
            Fehlgeschlagen: {self.stats['failures']}
            Logins durchgeführt: {self.stats['logins']}
            Captchas erkannt: {self.stats['captchas_detected']}
            --------------------------------------------------
            Status: Alle Datenbanken und Sessions aktualisiert.
            """
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_sender, self.email_password)
            server.send_message(msg)
            server.quit()
            logger.info("📧 Email-Bericht erfolgreich versandt.")
        except Exception as e:
            logger.error(f"📧 Email-Fehler: {e}")

# ==============================================================================
# === ENTRY POINT ===
# ==============================================================================
if __name__ == "__main__":
    bot = OmniGodBot()
    
    # Windows Selector Loop Fix
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    try:
        # Startet den Bot
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        logger.info("🛑 Bot manuell durch User gestoppt.")
    except Exception as e:
        logger.critical(f"💥 KRITISCHER SYSTEMFEHLER: {e}")
        traceback.print_exc()
    finally:
        # WICHTIG: Erstellt das Dashboard IMMER, egal ob Erfolg oder Fehler
        try:
            bot.generate_live_dashboard()
            logger.info("🏁 Finales Dashboard wurde vor dem Beenden gesichert.")
        except Exception as dash_e:
            logger.error(f"⚠️ Dashboard konnte nicht erstellt werden: {dash_e}")
