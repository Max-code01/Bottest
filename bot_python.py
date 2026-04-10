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
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict, Set, Optional, Any
from playwright.async_api import async_playwright, Page, BrowserContext, ElementHandle, Browser

# === MAXIMALE LOGGING KONFIGURATION ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('ultra_god_mode_v3.log', encoding='utf-8')]
)
logger = logging.getLogger("ULTRA_GOD_MODE_V3")

# ==========================================
# NEU: DATENBANK-MANAGER FÜR PERSISTENZ
# ==========================================

class DatabaseManager:
    """Verwaltet besuchte URLs und Erfolge in einer SQLite-Datenbank."""
    def __init__(self, db_path: str = "bot_data.db"):
        self.db_path = db_path
        self._setup()

    def _setup(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS visited_urls 
                          (url TEXT PRIMARY KEY, status TEXT, timestamp DATETIME)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS successes 
                          (url TEXT, message TEXT, timestamp DATETIME)''')
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
        except: pass

    def add_success(self, url: str, message: str):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO successes VALUES (?, ?, ?)", 
                           (url, message, datetime.now()))
            conn.commit()
            conn.close()
        except: pass

# ==========================================
# NEU: EMAIL-NOTIFIKATIONSSYSTEM
# ==========================================

class NotificationManager:
    """Sendet Berichte an den hinterlegten Google-Account."""
    def __init__(self, email: str = "max.schule13@gmail.com"):
        self.receiver_email = email
        self.sender_email = email
        self.password = "DEIN_APP_PASSWORT" # Muss durch ein App-Passwort ersetzt werden

    def send_report(self, subject: str, body: str):
        if self.password == "DEIN_APP_PASSWORT":
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

# ==========================================
# NEU: ADVANCED PROXY ROTATOR
# ==========================================

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
        # Format: ip:port:user:pass oder ip:port
        parts = proxy.split(':')
        if len(parts) == 4:
            return {
                "server": f"http://{parts[0]}:{parts[1]}",
                "username": parts[2],
                "password": parts[3]
            }
        return {"server": f"http://{proxy}"}

# ==========================================
# BESTEHENDE STEALTH-SYSTEME (ERWEITERT)
# ==========================================

class AdvancedStealthManager:
    @staticmethod
    async def inject_stealth_scripts(page: Page):
        logger.info("🥷 Injiziere Deep-Stealth-Skripte auf V8-Engine-Ebene...")
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.navigator.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['de-DE', 'de', 'en-US', 'en']});
            
            const getParameter = WebGLRenderingContext.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return 'Intel Inc.';
                if (parameter === 37446) return 'Intel Iris OpenGL Engine';
                return getParameter(parameter);
            };

            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );

            // Hardware Concurrency Spoofing
            Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
            // Device Memory Spoofing
            Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
        """)

class CognitiveHumanTyping:
    @staticmethod
    async def type_like_human(field: ElementHandle, text: str):
        logger.info("🧠 Starte kognitive Tipp-Simulation...")
        try:
            await field.click()
            await asyncio.sleep(random.uniform(0.3, 0.8))
            
            for char in text:
                if random.random() < 0.03 and char.isalpha():
                    wrong_char = random.choice("abcdefghijklmnopqrstuvwxyz")
                    await field.type(wrong_char, delay=random.randint(20, 60))
                    await asyncio.sleep(random.uniform(0.1, 0.4))
                    await field.press("Backspace")
                    await asyncio.sleep(random.uniform(0.1, 0.3))
                
                delay = random.gauss(45, 20)
                delay = max(15, min(delay, 150))
                await field.type(char, delay=int(delay))
                
                if char in [' ', '.', ',', ':', '!', '?'] and random.random() < 0.4:
                    await asyncio.sleep(random.uniform(0.3, 0.9))
        except:
            await field.fill(text)

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

# ==========================================
# HAUPTKLASSE: OMNIGODBOT V3 (MAXIMALE EXPANSION)
# ==========================================

class OmniGodBot:
    def __init__(self, config_path: str = 'bot_config.json'):
        self.config_path = config_path
        self.config = self._load_config()
        self.stats = {
            "attempts": 0, "successes": 0, "failures": 0, 
            "logins": 0, "captchas_detected": 0, "links_found": 0
        }
        self.visited_links: Set[str] = set()
        self.target_queue: Optional[asyncio.Queue] = None 
        self.db = DatabaseManager()
        self.notifier = NotificationManager()
        self.proxies = ProxyManager()
        self.session_file = 'session_v3.json'
        self.accounts_file = 'accounts.json'

    def _load_config(self) -> Dict:
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except: pass
        return {
            "keywords": ["Schach", "Chess", "Gaming Forum", "Reddit Chess", "Schach lernen"],
            "parts": ["Interessanter Ansatz!", "Hast du das schon gesehen?", "Passend dazu:", "Check das mal aus:"],
            "messages": ["https://profischach.netlify.app/"],
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/123.0.0.0 Safari/537.36"
            ]
        }

    def _build_message(self) -> str:
        prefix = random.choice(self.config.get('parts', [""]))
        main = random.choice(self.config.get('messages', ["https://profischach.netlify.app/"]))
        msg = f"{prefix} {main}".strip()
        return msg.replace("[", "").replace("]", "")

    async def accept_everything(self, page: Page):
        selectors = [
            "button:has-text('Zustimmen')", "button:has-text('Akzeptieren')", 
            "button:has-text('Agree')", "button:has-text('OK')", "button:has-text('Accept')",
            "button:has-text('Alles erlauben')", "#save", ".close-button", ".modal-close",
            "button:has-text('Verstanden')", "a.cc-btn.cc-dismiss", "button.accept",
            "button[aria-label*='Allow']", "button[id*='cookie-accept']"
        ]
        for sel in selectors:
            try:
                elements = await page.query_selector_all(sel)
                for el in elements:
                    if await el.is_visible():
                        await el.click()
                        await asyncio.sleep(0.3)
            except: continue

    async def human_emulation(self, page: Page):
        try:
            width, height = 1920, 1080
            for _ in range(random.randint(5, 12)):
                tx = random.randint(100, width - 100)
                ty = random.randint(100, height - 100)
                await page.mouse.move(tx, ty, steps=random.randint(15, 40))
                if random.random() < 0.2:
                    await page.mouse.wheel(0, random.randint(200, 800))
                await asyncio.sleep(random.uniform(0.1, 0.4))
        except: pass

    async def auto_login(self, page: Page, link: str):
        if not os.path.exists(self.accounts_file): return
        try:
            with open(self.accounts_file, 'r') as f: accounts = json.load(f)
            target = next((a for a in accounts if a.get("domain") in link or a.get("domain") == "*"), None)
            if not target: return

            logger.info(f"🔑 Login-Versuch auf {link}")
            user_selectors = ["input[name*='user']", "input[type='text']", "input[id*='user']", "#login-username"]
            pass_selectors = ["input[name*='pass']", "input[type='password']", "#login-passwd"]
            
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
                            await asyncio.sleep(5)
                            return
        except: pass

    async def try_post_in_frame(self, frame, link: str) -> bool:
        selectors = [
            "textarea", "div[contenteditable='true']", "[role='textbox']", 
            "#message", ".cke_editable", "textarea[name='comment_text']",
            "input[name='message']", ".redactor-editor", "#quick_reply_textarea"
        ]
        for sel in selectors:
            try:
                field = await frame.wait_for_selector(sel, timeout=3000, state="visible")
                if field:
                    logger.info(f"🎯 Feld gefunden: {sel} auf {link}")
                    await field.scroll_into_view_if_needed()
                    msg = self._build_message()
                    await field.click()
                    await CognitiveHumanTyping.type_like_human(field, msg)
                    await asyncio.sleep(2)
                    
                    submit_selectors = [
                        "button[type='submit']", "input[type='submit']", 
                        "button:has-text('Post')", "button:has-text('Send')",
                        "button:has-text('Antworten')", ".submit-btn"
                    ]
                    for s_sel in submit_selectors:
                        btn = await frame.query_selector(s_sel)
                        if btn and await btn.is_visible():
                            await btn.click()
                            logger.info(f"🚀 Post abgeschickt auf {link}")
                            self.db.add_success(link, msg)
                            return True
                    await frame.keyboard.press("Control+Enter")
                    return True
            except: continue
        return False

    async def process_queue(self, context: BrowserContext):
        while True:
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
                
                # KEINE FILTER: Wir versuchen jede Seite zu laden
                response = await page.goto(link, timeout=60000, wait_until="domcontentloaded")
                
                await self.accept_everything(page)
                await self.auto_login(page, link)
                await self.human_emulation(page)
                
                posted = False
                for frame in page.frames:
                    if await self.try_post_in_frame(frame, link):
                        self.stats["successes"] += 1
                        posted = True
                        break
                
                if not posted:
                    shadow = await DeepDOMAnalyzer.pierce_shadow_dom(page, ["textarea", "div[contenteditable='true']"])
                    if shadow:
                        await shadow.fill(self._build_message())
                        await shadow.press("Enter")
                        self.stats["successes"] += 1
                        posted = True

                self.db.add_visited(link, "SUCCESS" if posted else "FAILED")
                
            except Exception as e:
                logger.debug(f"⚠️ Fehler bei {link}: {e}")
                self.stats["failures"] += 1
                self.db.add_visited(link, f"ERROR: {str(e)[:50]}")
            finally:
                await page.close()
                self.target_queue.task_done()
                await asyncio.sleep(random.uniform(10, 25))

    async def perform_search(self, context: BrowserContext, engine: str, url_pattern: str, kw: str):
        page = await context.new_page()
        try:
            # Maximale Seitenzahl für Suche
            for p_idx in range(15): 
                offset = p_idx * 10
                search_url = url_pattern.format(kw=kw, offset=offset)
                logger.info(f"🔎 {engine} Scan: {kw} (Seite {p_idx+1})")
                
                await AdvancedStealthManager.inject_stealth_scripts(page)
                await page.goto(search_url, timeout=40000)
                await asyncio.sleep(random.uniform(3, 6))
                await self.accept_everything(page)
                
                links = await page.eval_on_selector_all("a", "nodes => nodes.map(n => n.href)")
                # === DEBUGLOG ANFANG ===
                if not links:
                    logger.warning(f"⚠️ {engine} hat auf Seite {p_idx+1} keine Links gefunden!")
                    # Erstellt einen Screenshot im Hauptordner des Bots
                    screenshot_name = f"error_{engine}_page{p_idx+1}_{int(time.time())}.png"
                    await page.screenshot(path=screenshot_name)
                    logger.info(f"📸 Screenshot gespeichert als: {screenshot_name}")
                # === DEBUGLOG ENDE ===
                
                count = 0
                for link in links:
                    # FILTER ENTFERNT: Fast alles wird genommen
                    if link.startswith("http") and not any(x in link for x in ["google", "bing", "microsoft", "apple", "github"]):
                        await self.target_queue.put(link)
                        count += 1
                
                self.stats["links_found"] += count
                logger.info(f"📥 {count} Links aus {engine} extrahiert.")
                if count == 0: break # Keine weiteren Ergebnisse
        except Exception as e:
            logger.error(f"❌ Suchmaschinen-Fehler ({engine}): {e}")
        finally:
            await page.close()

    async def start(self):
        self.target_queue = asyncio.Queue()
        async with async_playwright() as p:
            logger.info("🔥 ULTRA-GOD-MODE V3 AKTIVIERT. REICHWEITE: MAXIMAL.")
            
            proxy_config = self.proxies.get_random_proxy()
            browser = await p.chromium.launch(headless=True, args=[
                '--no-sandbox', '--disable-setuid-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--window-size=1920,1080', '--mute-audio'
            ], proxy=proxy_config)
            
            context = await browser.new_context(
                user_agent=random.choice(self.config['user_agents']),
                viewport={'width': 1920, 'height': 1080},
                locale="de-DE",
                timezone_id="Europe/Berlin"
            )
            
            search_engines = [
                ("Bing", "https://www.bing.com/search?q={kw}+forum+comment&first={offset}"),
                ("Google", "https://www.google.com/search?q={kw}+forum+reply&start={offset}"),
                ("DuckDuckGo", "https://duckduckgo.com/?q={kw}"),
                ("Yahoo", "https://search.yahoo.com/search?p={kw}+forum+post&b={offset}")
            ]
            
            search_tasks = []
            for kw in self.config['keywords']:
                for name, url in search_engines:
                    search_tasks.append(self.perform_search(context, name, url, kw))

            # 10 parallele Worker für maximale Geschwindigkeit
            workers = [asyncio.create_task(self.process_queue(context)) for _ in range(10)]
            
            await asyncio.gather(*search_tasks)
            
            try:
                # Längeres Timeout für die Queue
                await asyncio.wait_for(self.target_queue.join(), timeout=3600)
            except asyncio.TimeoutError:
                logger.info("⏳ Zeitlimit für aktuelle Queue erreicht.")

            await context.storage_state(path=self.session_file)
            
            for w in workers: w.cancel()
            await browser.close()
            
            report = self._generate_report()
            self.notifier.send_report("OmniGodBot V3 Status-Update", report)
            print(report)

    def _generate_report(self) -> str:
        rep = f"""
        📊 OMNI-GOD-BOT V3 ULTIMATE REPORT
        ----------------------------------
        Zeitpunkt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Gefundene Links: {self.stats['links_found']}
        Versuche: {self.stats['attempts']}
        Erfolge: {self.stats['successes']}
        Fehlgeschlagen: {self.stats['failures']}
        Logins: {self.stats['logins']}
        Captchas: {self.stats['captchas_detected']}
        ----------------------------------
        Email-Status: Bericht gesendet an max.schule13@gmail.com
        Datenbank: bot_data.db aktualisiert.
        """
        return rep

if __name__ == "__main__":
    bot = OmniGodBot()
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        logger.info("🛑 Manuell gestoppt.")
