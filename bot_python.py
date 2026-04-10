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
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict, Set, Optional, Any, Union
from playwright.async_api import async_playwright, Page, BrowserContext, ElementHandle, Browser, Frame

# ==============================================================================
# === MAXIMALE LOGGING & DEBUG KONFIGURATION (ERWEITERT) ===
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - [%(name)s] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout), 
        logging.FileHandler('ultra_god_mode_v3_EXTREME.log', encoding='utf-8')
    ]
)
logger = logging.getLogger("ULTRA_GOD_MODE_V3_ULTIMATE")

# ==============================================================================
# === DATENBANK-MANAGER FÜR PERSISTENZ (BESTEHEND & ERWEITERT) ===
# ==============================================================================
class DatabaseManager:
    """Verwaltet besuchte URLs und Erfolge in einer SQLite-Datenbank mit erweiterten Metadaten."""
    def __init__(self, db_path: str = "bot_data.db"):
        self.db_path = db_path
        self._setup()

    def _setup(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Bestehende Tabellen
        cursor.execute('''CREATE TABLE IF NOT EXISTS visited_urls 
                          (url TEXT PRIMARY KEY, status TEXT, timestamp DATETIME)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS successes 
                          (url TEXT, message TEXT, timestamp DATETIME)''')
        # Neue Analytik-Tabellen für die Expansion
        cursor.execute('''CREATE TABLE IF NOT EXISTS platform_types 
                          (domain TEXT PRIMARY KEY, type TEXT, last_seen DATETIME)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS captcha_events 
                          (url TEXT, detected_at DATETIME, solved BOOLEAN)''')
        conn.commit()
        conn.close()

    def add_visited(self, url: str, status: str):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO visited_urls VALUES (?, ?, ?)", 
                           (url, status, datetime.now()))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"DB Error (visited): {e}")

    def add_success(self, url: str, message: str):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO successes VALUES (?, ?, ?)", 
                           (url, message, datetime.now()))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"DB Error (success): {e}")

    def log_platform(self, domain: str, p_type: str):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO platform_types VALUES (?, ?, ?)", 
                           (domain, p_type, datetime.now()))
            conn.commit()
            conn.close()
        except: pass

# ==============================================================================
# === EMAIL-NOTIFIKATIONSSYSTEM (BESTEHEND) ===
# ==============================================================================
class NotificationManager:
    """Sendet Berichte an den hinterlegten Google-Account."""
    def __init__(self, email: str = "max.schule13@gmail.com"):
        self.receiver_email = email
        self.sender_email = email
        self.password = "Max1234567890123" # Muss durch ein App-Passwort ersetzt werden

    def send_report(self, subject: str, body: str):
        if self.password == "Umbekannt" or not self.password:
            logger.warning("📧 Email-Passwort nicht gesetzt. Überspringe Versand.")
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.password)
            server.send_message(msg)
            server.quit()
            logger.info(f"📧 Report erfolgreich an {self.receiver_email} gesendet.")
        except Exception as e:
            logger.error(f"📧 Email-Fehler: {e}")

# ==============================================================================
# === ADVANCED PROXY ROTATOR (BESTEHEND) ===
# ==============================================================================
class ProxyManager:
    """Verwaltet eine Liste von Proxies für maximale Anonymität."""
    def __init__(self, proxy_file: str = "proxies.txt"):
        self.proxy_file = proxy_file
        self.proxies = self._load_proxies()

    def _load_proxies(self) -> List[str]:
        if os.path.exists(self.proxy_file):
            with open(self.proxy_file, "r") as f:
                return [line.strip() for line in f if line.strip()]
        return []

    def get_random_proxy(self) -> Optional[Dict]:
        if not self.proxies:
            return None
        proxy = random.choice(self.proxies)
        parts = proxy.split(':')
        if len(parts) == 4:
            return {
                "server": f"http://{parts[0]}:{parts[1]}",
                "username": parts[2],
                "password": parts[3]
            }
        return {"server": f"http://{proxy}"}

# ==============================================================================
# === NEU: INTELLIGENT CONTENT GENERATOR ===
# ==============================================================================
# ==============================================================================
# === VERSCHMOLZEN: AI & CONTEXT GENERATOR (GEMINI POWERED) ===
# ==============================================================================
class IntelligentAIPro:
    """Kombiniert Gemini-KI mit deiner Profischach-Werbung."""
    
    def __init__(self):
        # Dein Key und das Modell
        self.api_key = "AIzaSyBjYBRohweWpdMDsM9mqLKH9VHOH2D8o3I"
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Deine Website-Infos für die KI
        self.target_link = "https://profischach.netlify.app/"
        self.description = "Eine neue, saubere Plattform für Schach, Chat und eine Alternative zu großen Seiten."

    async def get_page_context(self, page_or_frame) -> str:
        """Liest den Foren-Thread, damit die Antwort perfekt passt."""
        try:
            return await page_or_frame.evaluate("() => document.body.innerText.substring(0, 1200)")
        except:
            return "Allgemeine Schach-Diskussion."

    async def generate_smart_message(self, context: str) -> str:
        """Verschmilzt KI-Intelligenz mit deiner Werbe-Absicht."""
        prompt = (
            f"Du bist ein aktiver Nutzer in einem Schach-Forum. "
            f"Das ist der aktuelle Thread-Inhalt: '{context}'\n\n"
            f"Schreibe eine kurze, menschliche Antwort (1-2 Sätze). "
            f"Gehe kurz auf das Thema ein und empfehle dann natürlich die Seite {self.target_link}. "
            f"Info zur Seite: {self.description}. "
            f"WICHTIG: Antworte wie ein Mensch, locker, keine KI-Floskeln, kein 'Ich als KI', "
            f"kein förmliches 'Sehr geehrte Damen und Herren'."
        )
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip().replace('"', '')
        except Exception as e:
            logger.error(f"KI-Fehler: {e}. Nutze Fallback-Nachricht.")
            # Fallback (deine alte Logik), falls Gemini streikt
            intros = ["Hey Leute,", "Moin Schachfreunde!", "Hab mal ne Frage..."]
            middles = ["Schon gesehen? Die Seite ist echt top für Endspiele:", "Coole Alternative hier:"]
            return f"{random.choice(intros)} {random.choice(middles)} {self.target_link}"
# ==============================================================================
# === STEALTH-SYSTEME (MASSIV ERWEITERT) ===
# ==============================================================================
class AdvancedStealthManager:
    @staticmethod
    async def inject_stealth_scripts(page: Page):
        logger.info("🥷 Injiziere Deep-Stealth-Skripte auf V8-Engine-Ebene...")
        # Die Basis-Skripte bleiben erhalten, werden aber durch Fingerprint-Evasion ergänzt
        await page.add_init_script("""
            // WebDriver Hide
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.navigator.chrome = { runtime: {} };
            
            // Plugin & Language Spoofing
            Object.defineProperty(navigator, 'plugins', {get: () => [
                { name: 'Chrome PDF Viewer', filename: 'internal-pdf-viewer' },
                { name: 'Native Client', filename: 'internal-nacl-plugin' }
            ]});
            Object.defineProperty(navigator, 'languages', {get: () => ['de-DE', 'de', 'en-US', 'en']});
            
            // WebGL & Canvas Fingerprinting Evasion
            const getParameter = WebGLRenderingContext.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return 'Intel Inc.';
                if (parameter === 37446) return 'Intel Iris OpenGL Engine';
                return getParameter(parameter);
            };

            // Permissions Spoofing
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );

            // Hardware Spoofing (CPU/RAM)
            Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
            Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
            
            // Screen Resolution Randomization
            Object.defineProperty(screen, 'width', {get: () => 1920});
            Object.defineProperty(screen, 'height', {get: () => 1080});
        """)

# ==============================================================================
# === COGNITIVE HUMAN TYPING (BESTEHEND) ===
# ==============================================================================
class CognitiveHumanTyping:
    @staticmethod
    async def type_like_human(field: Union[ElementHandle, Any], text: str):
        logger.info("🧠 Starte kognitive Tipp-Simulation...")
        try:
            await field.click()
            await asyncio.sleep(random.uniform(0.3, 0.8))
            
            for char in text:
                # Simulation von Tippfehlern (3% Chance)
                if random.random() < 0.03 and char.isalpha():
                    wrong_char = random.choice("abcdefghijklmnopqrstuvwxyz")
                    await field.type(wrong_char, delay=random.randint(20, 60))
                    await asyncio.sleep(random.uniform(0.1, 0.4))
                    await field.press("Backspace")
                    await asyncio.sleep(random.uniform(0.1, 0.3))
                
                # Natürliche Verzögerung (Gauss-Verteilung)
                delay = random.gauss(45, 20)
                delay = max(15, min(delay, 150))
                await field.type(char, delay=int(delay))
                
                # Nach Satzzeichen länger warten
                if char in [' ', '.', ',', ':', '!', '?'] and random.random() < 0.4:
                    await asyncio.sleep(random.uniform(0.3, 0.9))
        except:
            # Fallback für spezielle Input-Felder
            try:
                await field.fill(text)
            except: pass

# ==============================================================================
# === DEEP DOM ANALYZER (BESTEHEND) ===
# ==============================================================================
class DeepDOMAnalyzer:
    @staticmethod
    async def pierce_shadow_dom(page: Page, selectors: List[str]) -> Optional[Any]:
        logger.info("🔦 Aktiviere Shadow-DOM Piercing-Technologie...")
        js_code = """(selectors) => {
            function findElement(node, selectors) {
                for (let sel of selectors) {
                    if (node.matches && node.matches(sel)) return node;
                    if (node.querySelector && node.querySelector(sel)) return node.querySelector(sel);
                }
                let children = node.children || [];
                for (let child of children) {
                    let result = findElement(child, selectors);
                    if (result) return result;
                }
                if (node.shadowRoot) {
                    let result = findElement(node.shadowRoot, selectors);
                    if (result) return result;
                }
                return null;
            }
            return findElement(document.body, selectors);
        }"""
        try:
            element = await page.evaluate_handle(js_code, selectors)
            if element and await element.evaluate("e => e !== null"):
                return element
        except: pass
        return None

# ==============================================================================
# === NEU: CHATROOM & FORUM SPECIALIST (DAS "1.000.000% PROZENT" UPGRADE) ===
# ==============================================================================
class PlatformSpecialist:
    """Spezialisierte Logik für Chaträume (Chatroom 2000) und Schach-Foren."""
    
    @staticmethod
    async def handle_chatroom_2000(page: Page):
        """Spezifische Interaktion für Chatroom 2000."""
        if "chatroom2000" in page.url:
            logger.info("🚀 Spezial-Modus: Chatroom 2000 erkannt.")
            try:
                # Login / Nickname-Feld suchen
                nick_field = await page.query_selector("input#login_nickname, input[name='nickname']")
                if nick_field:
                    nick = f"SchachFan_{random.randint(100, 999)}"
                    await nick_field.fill(nick)
                    await page.keyboard.press("Enter")
                    await asyncio.sleep(5)
                
                # Nachricht im Chat senden
                chat_input = await page.query_selector("#chat_input, .chat-input, textarea")
                if chat_input:
                    msg = "Hey, spielt hier jemand Schach? Suche Leute für: https://profischach.netlify.app/"
                    await chat_input.fill(msg)
                    await page.keyboard.press("Enter")
                    return True
            except: pass
        return False

    @staticmethod
    async def handle_vbulletin_forum(page: Page):
        """Spezifische Logik für vBulletin/phpBB Schachforen."""
        try:
            reply_button = await page.query_selector("a[href*='newreply'], .button-reply")
            if reply_button:
                await reply_button.click()
                await asyncio.sleep(3)
                # Das Textfeld in Foren ist oft ein IFrame
                return True
        except: pass
        return False

# ==============================================================================
# === HAUPTKLASSE: OMNIGODBOT V3 ULTIMATE (MAXIMALE EXPANSION) ===
# ==============================================================================
class OmniGodBot:
    def __init__(self, config_path: str = 'bot_config.json'):
        self.config_path = config_path
        self.config = self._load_config()
        self.stats = {
            "attempts": 0, "successes": 0, "failures": 0, 
            "logins": 0, "captchas_detected": 0, "links_found": 0,
            "chat_messages": 0
        }
        self.visited_links: Set[str] = set()
        self.target_queue: asyncio.Queue = asyncio.Queue()
        self.db = DatabaseManager()
        self.notifier = NotificationManager()
        self.proxies = ProxyManager()
        self.ai_brain = IntelligentAIPro()
        self.session_file = 'session_v3.json'
        self.accounts_file = 'accounts.json'
        self.is_running = True

    def _load_config(self) -> Dict:
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except: pass
        return {
            "keywords": [
                "Schach Forum", "Chess Community", "Chatroom 2000", "Knuddels Alternative",
                "Schach lernen", "Schach spielen online", "Gaming Chat", "Deutsch Chat",
                "Schach Strategie Forum", "Lichess Forum", "Chess.com Feedback"
            ],
            "parts": ["Schon gesehen?", "Kleiner Tipp für euch:", "Interessanter Link:", "Schaut mal hier vorbei:"],
            "messages": ["https://profischach.netlify.app/"],
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/123.0.0.0 Safari/537.36"
            ]
        }

    def _build_message(self) -> str:
        # Da die KI jetzt direkt in try_post_in_frame aufgerufen wird,
        # dient dies nur noch als absoluter Notfall-Fallback.
        return "Schaut mal hier vorbei für Schach-Training: https://profischach.netlify.app/"
        
        prefix = random.choice(self.config.get('parts', [""]))
        main = random.choice(self.config.get('messages', ["https://profischach.netlify.app/"]))
        msg = f"{prefix} {main}".strip()
        return msg.replace("[", "").replace("]", "")

    async def accept_everything(self, page: Page):
        """Erweiterte Cookie- und Overlay-Beseitigung."""
        selectors = [
            "button:has-text('Zustimmen')", "button:has-text('Akzeptieren')", 
            "button:has-text('Agree')", "button:has-text('OK')", "button:has-text('Accept')",
            "button:has-text('Alles erlauben')", "#save", ".close-button", ".modal-close",
            "button:has-text('Verstanden')", "a.cc-btn.cc-dismiss", "button.accept",
            "button[aria-label*='Allow']", "button[id*='cookie-accept']", ".qc-cmp2-footer button"
        ]
        for sel in selectors:
            try:
                elements = await page.query_selector_all(sel)
                for el in elements:
                    if await el.is_visible():
                        await el.click()
                        await asyncio.sleep(0.5)
            except: continue

    async def human_emulation(self, page: Page):
        """Verbesserte Simulation menschlichen Verhaltens."""
        try:
            width, height = 1920, 1080
            # Zufällige Mausbewegungen
            for _ in range(random.randint(8, 20)):
                tx = random.randint(50, width - 50)
                ty = random.randint(50, height - 50)
                await page.mouse.move(tx, ty, steps=random.randint(20, 60))
                if random.random() < 0.3:
                    await page.mouse.wheel(0, random.randint(-400, 800))
                await asyncio.sleep(random.uniform(0.1, 0.5))
            
            # Zufälliges Verweilen (Lese-Simulation)
            if random.random() < 0.5:
                await asyncio.sleep(random.uniform(2, 5))
        except: pass

    async def auto_login(self, page: Page, link: str):
        """Erweiterter Login-Mechanismus."""
        if not os.path.exists(self.accounts_file): return
        try:
            with open(self.accounts_file, 'r') as f: accounts = json.load(f)
            # Finde passenden Account für Domain
            target = next((a for a in accounts if a.get("domain") in link or a.get("domain") == "*"), None)
            if not target: return

            logger.info(f"🔑 Login-Versuch auf {link}")
            user_selectors = [
                "input[name*='user']", "input[name*='login']", "input[type='text']", 
                "input[id*='user']", "#login-username", "input[autocomplete='username']"
            ]
            pass_selectors = [
                "input[name*='pass']", "input[type='password']", "#login-passwd", 
                "input[autocomplete='current-password']"
            ]
            
            for u_sel in user_selectors:
                u_field = await page.query_selector(u_sel)
                if u_field and await u_field.is_visible():
                    await CognitiveHumanTyping.type_like_human(u_field, target['username'])
                    for p_sel in pass_selectors:
                        p_field = await page.query_selector(p_sel)
                        if p_field and await p_field.is_visible():
                            await CognitiveHumanTyping.type_like_human(p_field, target['password'])
                            await page.keyboard.press("Enter")
                            self.stats["logins"] += 1
                            await page.wait_for_load_state("networkidle", timeout=10000)
                            return
        except: pass

    async def try_post_in_frame(self, frame, link: str) -> bool:
        """
        Sucht Felder in Frames, generiert KI-Beiträge basierend auf dem 
        Seiteninhalt und schickt den Post ab.
        """
        selectors = [
            "textarea", "div[contenteditable='true']", "[role='textbox']", 
            "#message", ".cke_editable", "textarea[name='comment_text']",
            "input[name='message']", ".redactor-editor", "#quick_reply_textarea",
            "iframe[title*='Rich Text']", ".message-editor"
        ]

        for sel in selectors:
            try:
                # 1. Feld suchen
                field = await frame.wait_for_selector(sel, timeout=4000, state="visible")
                if field:
                    logger.info(f"🎯 Feld gefunden: {sel} auf {link}. Generiere KI-Beitrag...")
                    await field.scroll_into_view_if_needed()

                    # 2. KI-KONTEXT UND GENERIERUNG (Verschmelzung)
                    # Wir lesen erst, was auf der Seite steht
                    page_context = await self.ai_brain.get_page_context(frame)
                    # Gemini erstellt die passende Antwort für profischach.netlify.app
                    smart_msg = await self.ai_brain.generate_smart_message(page_context)

                    # 3. TEXT EINGEBEN
                    # Falls es ein Rich-Text-Iframe ist (wie bei vielen Foren)
                    if (await field.evaluate("e => e.tagName")) == "IFRAME":
                        content_frame = await field.content_frame()
                        if content_frame:
                            await content_frame.fill("body", smart_msg)
                        else: continue
                    else:
                        await field.click()
                        # Nutzt dein menschliches Tipp-Verhalten
                        await CognitiveHumanTyping.type_like_human(field, smart_msg)
                    
                    await asyncio.sleep(2)
                    
                    # 4. SENDEN-LOGIK
                    submit_selectors = [
                        "button[type='submit']", "input[type='submit']", 
                        "button:has-text('Post')", "button:has-text('Send')",
                        "button:has-text('Antworten')", ".submit-btn", "button:has-text('Abschicken')"
                    ]
                    
                    for s_sel in submit_selectors:
                        btn = await frame.query_selector(s_sel)
                        if btn and await btn.is_visible():
                            await btn.click()
                            logger.info(f"🚀 KI-Post erfolgreich abgeschickt auf {link}")
                            self.stats['successes'] += 1
                            self.db.add_success(link, smart_msg)
                            return True
                    
                    # Shortcut Fallback (Strg+Enter), falls kein Button gefunden wurde
                    await frame.keyboard.press("Control+Enter")
                    logger.info(f"🚀 Post via Shortcut abgeschickt auf {link}")
                    self.stats['successes'] += 1
                    self.db.add_success(link, smart_msg)
                    return True

            except Exception as e:
                logger.debug(f"Versuch mit Selektor {sel} fehlgeschlagen: {e}")
                continue
        
        return False

    async def process_queue(self, context: BrowserContext):
        """Haupt-Worker für die Link-Abarbeitung."""
        while self.is_running:
            try:
                link = await self.target_queue.get()
            except asyncio.CancelledError: break

            if link in self.visited_links:
                self.target_queue.task_done()
                continue
            
            self.visited_links.add(link)
            self.stats["attempts"] += 1
            page = await context.new_page()
            
            try:
                logger.info(f"🌐 Navigation: {link}")
                await AdvancedStealthManager.inject_stealth_scripts(page)
                
                # Maximale Wartezeit für schwere Seiten
                await page.goto(link, timeout=90000, wait_until="domcontentloaded")
                await asyncio.sleep(random.uniform(2, 5))
                
                await self.accept_everything(page)
                
                # SPEZIAL-CHECK: Chatrooms
                if await PlatformSpecialist.handle_chatroom_2000(page):
                    self.stats["successes"] += 1
                    self.stats["chat_messages"] += 1
                    self.db.add_visited(link, "CHAT_SUCCESS")
                    continue

                await self.auto_login(page, link)
                await self.human_emulation(page)
                
                # Versuche in allen Frames zu posten
                posted = False
                for frame in page.frames:
                    if await self.try_post_in_frame(frame, link):
                        self.stats["successes"] += 1
                        posted = True
                        break
                
                if not posted:
                    # Letzte Hoffnung: Shadow DOM oder generische Felder
                    shadow = await DeepDOMAnalyzer.pierce_shadow_dom(page, ["textarea", "div[contenteditable='true']"])
                    if shadow:
                        msg = self._build_message()
                        await shadow.click()
                        await CognitiveHumanTyping.type_like_human(shadow, msg)
                        await shadow.press("Enter")
                        self.stats["successes"] += 1
                        posted = True

                self.db.add_visited(link, "SUCCESS" if posted else "FAILED")
                
            except Exception as e:
                logger.debug(f"⚠️ Fehler bei {link}: {e}")
                self.stats["failures"] += 1
                self.db.add_visited(link, f"ERROR: {str(e)[:50]}")
                # Screenshot bei Fehler für Analyse
                try:
                    await page.screenshot(path=f"error_{int(time.time())}.png")
                except: pass
            finally:
                await page.close()
                self.target_queue.task_done()
                # Menschliche Pause zwischen Aktionen
                await asyncio.sleep(random.uniform(15, 45))

    async def perform_search(self, context: BrowserContext, engine: str, url_pattern: str, kw: str):
        """Scannt Suchmaschinen nach neuen Zielen."""
        page = await context.new_page()
        try:
            for p_idx in range(15): # Bis zu 15 Seiten pro Keyword
                offset = p_idx * 10
                search_url = url_pattern.format(kw=kw.replace(" ", "+"), offset=offset)
                logger.info(f"🔎 {engine} Scan: {kw} (Seite {p_idx+1})")
                
                await AdvancedStealthManager.inject_stealth_scripts(page)
                await page.goto(search_url, timeout=60000)
                await asyncio.sleep(random.uniform(4, 8))
                await self.accept_everything(page)
                
                # Extrahiere alle Links
                links = await page.eval_on_selector_all("a", "nodes => nodes.map(n => n.href)")
                
                count = 0
                for link in links:
                    # Filter: Keine großen Konzerne, nur potenzielle Foren/Blogs/Chats
                    if link.startswith("http") and not any(x in link for x in ["google", "bing", "microsoft", "apple", "github", "facebook", "twitter"]):
                        await self.target_queue.put(link)
                        count += 1
                
                self.stats["links_found"] += count
                logger.info(f"📥 {count} neue Links aus {engine} extrahiert.")
                
                # Wenn keine Links gefunden wurden, ist vielleicht ein Captcha da
                if count == 0:
                    if "captcha" in (await page.content()).lower():
                        logger.warning(f"🚨 Captcha auf {engine} erkannt!")
                        self.stats["captchas_detected"] += 1
                        await asyncio.sleep(60) # Pause zum Abkühlen
                    break 
                
                # Zufällige Pause zwischen Suchseiten
                await asyncio.sleep(random.uniform(5, 12))
                
        except Exception as e:
            logger.error(f"❌ Suchmaschinen-Fehler ({engine}): {e}")
        finally:
            await page.close()

    async def start(self):
        """Haupt-Orchestrierung des Bots."""
        async with async_playwright() as p:
            logger.info("🔥 ULTRA-GOD-MODE V3 ULTIMATE AKTIVIERT. REICHWEITE: GLOBAL.")
            
            proxy_config = self.proxies.get_random_proxy()
            browser = await p.chromium.launch(headless=True, args=[
                '--no-sandbox', '--disable-setuid-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--window-size=1920,1080', '--mute-audio',
                '--disable-infobars', '--disable-dev-shm-usage'
            ], proxy=proxy_config)
            
            # Persistente Session laden
            storage = self.session_file if os.path.exists(self.session_file) else None
            
            context = await browser.new_context(
                storage_state=storage,
                user_agent=random.choice(self.config['user_agents']),
                viewport={'width': 1920, 'height': 1080},
                locale="de-DE",
                timezone_id="Europe/Berlin"
            )
            
            # Suchmaschinen-Konfiguration
            search_engines = [
                ("Bing", "https://www.bing.com/search?q={kw}+forum+comment&first={offset}"),
                ("Google", "https://www.google.com/search?q={kw}+forum+reply&start={offset}"),
                ("DuckDuckGo", "https://duckduckgo.com/?q={kw}+chat"),
                ("Yahoo", "https://search.yahoo.com/search?p={kw}+post&b={offset}"),
                ("Ask", "https://www.ask.com/web?q={kw}+forum&page={offset}")
            ]
            
            # Starte Worker-Pool (12 parallele Worker für maximale Power)
            worker_count = 12
            workers = [asyncio.create_task(self.process_queue(context)) for _ in range(worker_count)]
            
            # Starte Such-Tasks
            search_tasks = []
            for kw in self.config['keywords']:
                for name, url in search_engines:
                    search_tasks.append(self.perform_search(context, name, url, kw))
                    # Kurze Pause zwischen Such-Starts, um Rate-Limits zu umgehen
                    await asyncio.sleep(random.uniform(1, 3))

            # Führe Suchen aus
            await asyncio.gather(*search_tasks)
            
            # Warte auf Abarbeitung der Queue
            try:
                await asyncio.wait_for(self.target_queue.join(), timeout=7200) # 2 Stunden Max
            except asyncio.TimeoutError:
                logger.info("⏳ Zeitlimit für aktuelle Queue erreicht. Speichere Status...")

            # Status speichern
            await context.storage_state(path=self.session_file)
            
            # Beenden
            self.is_running = False
            for w in workers: w.cancel()
            await browser.close()
            
            # Finaler Report
            report = self._generate_report()
            self.notifier.send_report("OmniGodBot V3 ULTIMATE - Final Status", report)
            print(report)

    def _generate_report(self) -> str:
        rep = f"""
        📊 OMNI-GOD-BOT V3 ULTIMATE REPORT (EXTREME EDITION)
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
        Email: Bericht wurde versandt.
        --------------------------------------------------
        """
        return rep

# ==============================================================================
# === ENTRY POINT ===
# ==============================================================================
if __name__ == "__main__":
    bot = OmniGodBot()
    # Windows Selector Loop Fix
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        logger.info("🛑 Bot manuell durch User gestoppt.")
    except Exception as e:
        logger.critical(f"💥 KRITISCHER SYSTEMFEHLER: {e}")
        traceback.print_exc()
