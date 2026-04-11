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
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import List, Dict, Set, Optional, Any, Union
from playwright.async_api import async_playwright, Page, BrowserContext, ElementHandle, Browser, Frame

# ==============================================================================
# === 1. MAXIMALE LOGGING & DEBUG KONFIGURATION (TITAN EDITION) ===
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - [WORKER %(threadName)s] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout), 
        logging.FileHandler('omni_god_v6_TITAN.log', encoding='utf-8')
    ]
)
logger = logging.getLogger("OMNI_GOD_V6_TITAN")

# ==============================================================================
# === 2. ERWEITERTE DATENBANK-ARCHITEKTUR (TRUST SCORING & ANALYTICS) ===
# ==============================================================================
class DatabaseManager:
    """Verwaltet das komplette Gedächtnis des Bots inklusive Trust-Scores."""
    def __init__(self, db_path: str = "bot_data_v6.db"):
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
                              (url TEXT, error_type TEXT, error_msg TEXT, timestamp DATETIME)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS domain_trust 
                              (domain TEXT PRIMARY KEY, trust_score INTEGER, captcha_hits INTEGER)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS sniper_targets 
                              (url TEXT PRIMARY KEY, platform TEXT, priority INTEGER)''')
            conn.commit()
            conn.close()
            logger.info("🗄️ V6 Titan Datenbank-Architektur online.")
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
        except Exception as e: logger.error(f"DB Error (visited): {e}")

    def add_success(self, url: str, message: str, platform_type: str = "unknown"):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO successes VALUES (?, ?, ?, ?)", 
                           (url, message, datetime.now(), platform_type))
            
            # Trust Score erhöhen
            domain = urllib.parse.urlparse(url).netloc
            cursor.execute("INSERT OR IGNORE INTO domain_trust (domain, trust_score, captcha_hits) VALUES (?, 50, 0)", (domain,))
            cursor.execute("UPDATE domain_trust SET trust_score = trust_score + 10 WHERE domain = ?", (domain,))
            
            conn.commit()
            conn.close()
        except Exception as e: logger.error(f"DB Error (success): {e}")

    def log_error(self, url: str, error_type: str, error_msg: str):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO error_logs VALUES (?, ?, ?, ?)", 
                           (url, error_type, str(error_msg), datetime.now()))
            conn.commit()
            conn.close()
        except: pass

    def report_captcha(self, url: str):
        try:
            domain = urllib.parse.urlparse(url).netloc
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO domain_trust (domain, trust_score, captcha_hits) VALUES (?, 50, 0)", (domain,))
            cursor.execute("UPDATE domain_trust SET captcha_hits = captcha_hits + 1, trust_score = trust_score - 5 WHERE domain = ?", (domain,))
            conn.commit()
            conn.close()
        except: pass

# ==============================================================================
# === 3. DISCORD / WEBHOOK NOTIFICATION SYSTEM (NEU) ===
# ==============================================================================
class WebhookNotifier:
    """Sendet Echtzeit-Warnungen und Erfolge an Discord oder Telegram."""
    def __init__(self):
        self.discord_webhook_url = "" # HIER DEINE DISCORD WEBHOOK URL EINTRAGEN

    async def send_alert(self, title: str, message: str, color: int = 16711680):
        if not self.discord_webhook_url: return
        import aiohttp
        payload = {
            "embeds": [{
                "title": title,
                "description": message,
                "color": color,
                "timestamp": datetime.utcnow().isoformat()
            }]
        }
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(self.discord_webhook_url, json=payload)
        except Exception as e:
            logger.debug(f"Webhook Failed: {e}")

# ==============================================================================
# === 4. DYNAMIC FINGERPRINT ENGINE (ERWEITERTER STEALTH V6) ===
# ==============================================================================
class AdvancedStealthManager:
    @staticmethod
    async def inject_stealth_scripts(page: Page, worker_id: int):
        """Macht jeden Worker einzigartig, um Massen-Banns zu verhindern."""
        logger.debug(f"🥷 [Worker {worker_id}] Generiere einzigartigen Browser-Fingerprint...")
        
        # Dynamische Hardware-Werte pro Worker
        ram_gb = random.choice([4, 8, 16, 32])
        cores = random.choice([4, 6, 8, 12, 16])
        vendor = random.choice(['Google Inc. (Apple)', 'Google Inc. (NVIDIA)', 'Google Inc. (AMD)'])
        renderer = random.choice(['ANGLE (Apple, Apple M1 Pro, OpenGL 4.1)', 'ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0)'])
        
        await page.add_init_script(f"""
            // Core Evasion
            Object.defineProperty(navigator, 'webdriver', {{get: () => undefined}});
            window.navigator.chrome = {{ runtime: {{}}, loadTimes: function() {{}}, csmo: {{}}, app: {{}} }};
            
            // Dynamic WebGL Evasion
            const getParameter = WebGLRenderingContext.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                if (parameter === 37445) return '{vendor}';
                if (parameter === 37446) return '{renderer}';
                return getParameter(parameter);
            }};

            // Hardware & Battery
            Object.defineProperty(navigator, 'deviceMemory', {{get: () => {ram_gb}}});
            Object.defineProperty(navigator, 'hardwareConcurrency', {{get: () => {cores}}});
            window.AudioContext = window.AudioContext || window.webkitAudioContext;
            navigator.getBattery = () => Promise.resolve({{
                level: {random.uniform(0.3, 0.99)}, charging: {str(random.choice([True, False])).lower()}, chargingTime: 0, dischargingTime: Infinity
            }});

            // Plugins & Permissions
            Object.defineProperty(navigator, 'plugins', {{get: () => [1, 2, 3, 4, 5]}});
            Object.defineProperty(navigator, 'languages', {{get: () => ['de-DE', 'de', 'en-US']}});
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ? Promise.resolve({{ state: Notification.permission }}) : originalQuery(parameters)
            );
        """)

# ==============================================================================
# === 5. SESSION WARMING SYSTEM (NEU) ===
# ==============================================================================
class SessionWarmer:
    """Simuliert menschliches Browsen VOR dem Posten, um Cloudflare zu beruhigen."""
    @staticmethod
    async def warm_up(page: Page):
        try:
            logger.debug("🔥 Starte Session Warming (Maus/Scroll-Simulation)...")
            width, height = 1920, 1080
            
            # Zufällige Scroll-Bewegungen
            for _ in range(random.randint(2, 5)):
                await page.mouse.wheel(0, random.randint(200, 700))
                await asyncio.sleep(random.uniform(0.5, 1.5))
            
            # Maus über Elemente bewegen
            links = await page.query_selector_all("a, p, h1, h2")
            if links:
                target = random.choice(links[:10])
                if await target.is_visible():
                    box = await target.bounding_box()
                    if box:
                        await page.mouse.move(box['x'] + 5, box['y'] + 5, steps=random.randint(10, 30))
                        await asyncio.sleep(random.uniform(0.2, 0.8))
            
            # Wieder hochscrollen
            await page.mouse.wheel(0, random.randint(-800, -200))
            await asyncio.sleep(random.uniform(1.0, 3.0))
        except: pass

# ==============================================================================
# === 6. CHAT-SNIPER-SYSTEM (BEIBEHALTEN & INTEGRIERT) ===
# ==============================================================================
class ChatSniper:
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
# === 7. INTELLIGENT LINK FILTER (VERBESSERT FÜR WENIGER CAPTCHAS) ===
# ==============================================================================
class LinkIntelligence:
    RELEVANT_KEYWORDS = [
        "forum", "chat", "thread", "topic", "community", "board", "viewtopic", 
        "index.php", "showtopic", "comments", "diskussion", "reply", "post", 
        "nachricht", "phpbb", "vbulletin", "Chatroom", "guestbook"
    ]
    
    JUNK_DOMAINS = [
        "google.com", "bing.com", "duckduckgo.com", "yahoo.com",
        "microsoft.com", "apple.com", "amazon.", "ebay.", 
        "twitter.com", "facebook.com", "instagram.com", "reddit.com",
        "quora.com", "britannica.com", "wikipedia.org", "arena.im",
        "googleusercontent.com"
    ]

    @classmethod
    def is_valuable(cls, url: str) -> bool:
        url_lower = url.lower()
        if any(junk in url_lower for junk in cls.JUNK_DOMAINS): return False
        if any(kw in url_lower for kw in cls.RELEVANT_KEYWORDS): return True
        import random
        return random.random() < 0.15 # Nur 15% unbekannte durchlassen

# ==============================================================================
# === 8. KOGNITIVES TIPPEN (BEIBEHALTEN) ===
# ==============================================================================
class CognitiveHumanTyping:
    @staticmethod
    async def type_like_human(page_or_frame, selector: str, text: str):
        try:
            element = await page_or_frame.wait_for_selector(selector, timeout=5000)
            if not element: return False
            await element.click()
            await asyncio.sleep(random.uniform(0.5, 1.5))
            
            for char in text:
                if random.random() < 0.02: 
                    await page_or_frame.keyboard.type(random.choice("abcdefghijklmnopqrstuvwxyz"))
                    await asyncio.sleep(random.uniform(0.1, 0.3))
                    await page_or_frame.keyboard.press("Backspace")
                await page_or_frame.keyboard.type(char)
                await asyncio.sleep(random.uniform(0.02, 0.15) if char != ' ' else random.uniform(0.05, 0.2))
                    
            await asyncio.sleep(random.uniform(1.0, 2.5))
            return True
        except: return False

# ==============================================================================
# === 9. PLATFORM SPECIALIST (TIEFE CHAT INTEGRATION BEIBEHALTEN) ===
# ==============================================================================
class PlatformSpecialist:
    @staticmethod
    async def detect_and_attack(page: Page, bot_instance, link: str):
        content = (await page.content()).lower()
        if "chatroom2000" in link or "mainchat" in link or "chat" in link.lower():
            return await PlatformSpecialist.deep_chat_attack(page, bot_instance, link)
        if "discourse" in content or "d-header" in content:
            return await PlatformSpecialist.attack_discourse(page, bot_instance.ai_brain, link)
        if any(x in content for x in ["vbulletin", "phpbb", "xenforo"]):
            return False 
        return False

    @staticmethod
    async def deep_chat_attack(page: Page, bot_instance, link: str):
        try:
            try:
                cookie_btns = await page.query_selector_all("button:has-text('Akzeptieren'), .cookie-btn")
                for btn in cookie_btns: 
                    if await btn.is_visible(): await btn.click()
            except: pass

            guest_login_selectors = ["input#login_nickname", "input[name='nickname']", "input[name='user']", ".guest-login-input"]
            nick_field = None
            for sel in guest_login_selectors:
                try:
                    nick_field = await page.wait_for_selector(sel, timeout=4000)
                    if nick_field: break
                except: continue

            if nick_field:
                await CognitiveHumanTyping.type_like_human(page, nick_field, f"SchachFreak_{random.randint(100,999)}")
                login_btn_selectors = ["button#login_btn", "input[type='submit']", "button:has-text('Chat betreten')"]
                for btn_sel in login_btn_selectors:
                    try:
                        btn = await page.query_selector(btn_sel)
                        if btn and await btn.is_visible(): await btn.click(); break
                    except: pass
                await asyncio.sleep(10)

            chat_input_selectors = ["#chat_input", ".message-input", "textarea[name='message']", "[contenteditable='true']"]
            chat_input = None
            for sel in chat_input_selectors:
                try:
                    chat_input = await page.wait_for_selector(sel, timeout=5000, state="visible")
                    if chat_input: break
                except: continue

            if chat_input:
                bot_instance.stats["logins"] += 1
                msg = "Spielt hier eigentlich jemand ernsthaft Schach? Suche Gegner für: https://profischach.netlify.app/"
                await CognitiveHumanTyping.type_like_human(page, chat_input_selectors[0] if not isinstance(chat_input, ElementHandle) else chat_input, msg)
                await page.keyboard.press("Enter")
                await asyncio.sleep(3)
                bot_instance.stats["chat_messages"] += 1
                return True
            return False
        except: return False

    @staticmethod
    async def attack_discourse(page: Page, ai_brain, link: str):
        try:
            reply_btn = await page.query_selector(".create.btn-primary")
            if reply_btn:
                await reply_btn.click()
                await asyncio.sleep(2)
                editor = await page.query_selector(".d-editor-input")
                if editor:
                    context = await page.evaluate("() => document.body.innerText.substring(0, 1000)")
                    msg = await ai_brain.generate_smart_message(context)
                    await CognitiveHumanTyping.type_like_human(page, ".d-editor-input", msg)
                    await page.click(".save-or-cancel .btn-primary")
                    return True
        except: return False

# ==============================================================================
# === 10. MULTI-LANGUAGE AI BRAIN (NEU) ===
# ==============================================================================
class IntelligentAIPro:
    def __init__(self):
        self.api_key = "AIzaSyBjYBRohweWpdMDsM9mqLKH9VHOH2D8o3I"
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.ai_active = True
        except: self.ai_active = False
        self.target_link = "https://profischach.netlify.app/"

    async def generate_smart_message(self, context: str) -> str:
        if not self.ai_active: return f"Great topic! If anyone plays chess, check out: {self.target_link}"
            
        prompt = (
            f"Analyze the following forum thread text to determine its language. "
            f"Text: '{context}'\n"
            f"Write a very short, natural response (1-2 sentences) matching the exact language of the text. "
            f"Casually mention you are looking for chess opponents on {self.target_link}. "
            f"Do not sound like an AI. Be informal."
        )
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            return response.text.strip().replace('"', '')
        except: return f"Anyone up for chess? I play here: {self.target_link}"

# ==============================================================================
# === 11. HAUPTKLASSE: OMNIGODBOT V6 TITAN ===
# ==============================================================================
class OmniGodBot:
    def __init__(self):
        self.db = DatabaseManager()
        self.ai_brain = IntelligentAIPro()
        self.webhook = WebhookNotifier()
        self.stats = {
            "attempts": 0, "successes": 0, "failures": 0, 
            "links_found": 0, "chat_messages": 0, "logins": 0,
            "captchas_detected": 0, "waf_blocks": 0
        }
        self.visited_links = set()
        self.is_running = True
        self.target_queue = asyncio.Queue()
        
        self.email_sender = "max.schule13@gmail.com"
        self.email_password = "Max1234567890123" 
        self.email_receiver = "max.schule13@gmail.com"
        
        # Fallback Suchmaschinen
        self.search_engines = [
            "https://www.google.com/search?q={kw}+forum",
            "https://html.duckduckgo.com/html/?q={kw}+forum",
            "https://search.yahoo.com/search?p={kw}+forum"
        ]

    async def start(self):
        async with async_playwright() as p:
            logger.info("🔥 OMNI-GOD-BOT V6 TITAN AKTIVIERT!")
            await self.webhook.send_alert("🚀 Bot Start", "OMNI-GOD V6 Titan hochgefahren. Beginne Infiltration.", 3066993)
            
            browser = await p.chromium.launch(
                headless=True, 
                args=['--no-sandbox', '--disable-blink-features=AutomationControlled', '--disable-infobars', '--window-size=1920,1080']
            )
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080}, locale="de-DE",
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36"
            )
            
            # 1. Chat-Sniper füllen
            for target in ChatSniper.get_extreme_targets(): await self.target_queue.put(target)

            # 2. Worker starten (Mit Fehler-Recovery)
            worker_count = 10 
            workers = [asyncio.create_task(self.worker_wrapper(context, i)) for i in range(worker_count)]
            
            # 3. Dynamic Search Scraper
            keywords = ["Schach Forum", "Chatroom Alternative", "Schach spielen online Chat", "Brettspiele Forum"]
            search_tasks = [self.smart_search(context, kw) for kw in keywords]
            await asyncio.gather(*search_tasks)
            
            try: await asyncio.wait_for(self.target_queue.join(), timeout=7200)
            except asyncio.TimeoutError: logger.info("⏱️ Zeitlimit erreicht.")

            self.is_running = False
            for w in workers: w.cancel()
            await browser.close()
            
            self.generate_live_dashboard()
            self.send_email_report()
            await self.webhook.send_alert("🏁 Bot Offline", f"Lauf beendet. Erfolge: {self.stats['successes']}", 15158332)

    async def smart_search(self, context, kw):
        """Wechselt Suchmaschinen, wenn Captchas auftreten."""
        page = await context.new_page()
        for engine_url in self.search_engines:
            try:
                search_url = engine_url.format(kw=kw.replace(' ', '+'))
                await page.goto(search_url, timeout=30000)
                await asyncio.sleep(random.uniform(4, 7))
                
                content = await page.content()
                if "captcha" in content.lower() or "unusual traffic" in content.lower():
                    logger.warning(f"🚨 Captcha bei {engine_url}! Wechsele Suchmaschine...")
                    self.stats["captchas_detected"] += 1
                    continue # Versuche nächste Suchmaschine
                
                all_links = await page.evaluate("() => Array.from(document.querySelectorAll('a')).map(a => a.href)")
                
                valuable_count = 0
                for link in all_links:
                    if LinkIntelligence.is_valuable(link) and link not in self.visited_links:
                        await self.target_queue.put(link)
                        valuable_count += 1
                
                self.stats["links_found"] += valuable_count
                logger.info(f"📥 {valuable_count} Links für '{kw}' via {engine_url[:20]}... gefunden.")
                break # Erfolgreich, keine weitere Suchmaschine für dieses Keyword nötig
            except Exception as e: logger.error(f"Search Error: {e}")
        try: await page.close()
        except: pass

    async def worker_wrapper(self, context, worker_id):
        """Auto-Recovery Wrapper für Worker."""
        while self.is_running:
            try:
                await self.process_queue(context, worker_id)
            except asyncio.CancelledError: break
            except Exception as e:
                logger.error(f"Worker {worker_id} Crash: {e}. Neustart...")
                await asyncio.sleep(5)

    async def process_queue(self, context, worker_id):
        while self.is_running:
            try: link = await self.target_queue.get()
            except: break

            if link in self.visited_links:
                self.target_queue.task_done()
                continue
            
            self.visited_links.add(link)
            self.stats["attempts"] += 1
            page = await context.new_page()
            start_time = time.time()
            
            try:
                await AdvancedStealthManager.inject_stealth_scripts(page, worker_id)
                page.on("response", lambda response: self._check_response(response))
                
                await page.goto(link, timeout=45000, wait_until="domcontentloaded")
                await SessionWarmer.warm_up(page)
                
                success = await PlatformSpecialist.detect_and_attack(page, self, link)
                
                if not success:
                    for frame in page.frames:
                        if await self.try_post_in_frame(frame, link):
                            success = True; break
                
                if not success: success = await self.try_post_in_frame(page, link)
                
                if success:
                    self.stats["successes"] += 1
                    self.db.add_success(link, "Erfolgreicher Post/Chat", "auto-detect")
                    logger.info(f"✅ [Worker {worker_id}] ERFOLG bei {link}")
                    asyncio.create_task(self.webhook.send_alert("🎯 Neuer Erfolg!", f"Post auf: {link}", 3066993))
                else:
                    self.stats["failures"] += 1
                    
                self.db.add_visited(link, "SUCCESS" if success else "FAILED", time.time() - start_time)
                
            except Exception as e:
                self.stats["failures"] += 1
                error_str = str(e).lower()
                if "timeout" in error_str: err_type = "Timeout"
                elif "target closed" in error_str: err_type = "Browser Closed"
                else: err_type = "Unknown Exception"
                self.db.log_error(link, err_type, str(e)[:100])
                logger.debug(f"[Worker {worker_id}] Fehlschlag {link}: {err_type}")
            finally:
                try: await page.close()
                except: pass
                self.target_queue.task_done()
                await asyncio.sleep(random.uniform(10, 25))

    async def try_post_in_frame(self, frame_or_page, link):
        selectors = ["textarea[name='message']", "textarea[name='body']", ".cke_editable", "div[contenteditable='true']", "[role='textbox']", "#message", "#quick_reply_textarea"]
        for sel in selectors:
            try:
                field = await frame_or_page.wait_for_selector(sel, timeout=3000, state="visible")
                if field:
                    try: context = await frame_or_page.evaluate("() => document.body.innerText.substring(0, 800)")
                    except: context = ""
                    msg = await self.ai_brain.generate_smart_message(context)
                    if await CognitiveHumanTyping.type_like_human(frame_or_page, sel, msg):
                        try: await frame_or_page.keyboard.press("Control+Enter")
                        except: pass
                        try:
                            submit_btns = await frame_or_page.query_selector_all("input[type='submit'], button[type='submit'], .submit-button")
                            if submit_btns: await submit_btns[0].click()
                        except: pass
                        await asyncio.sleep(3)
                        return True
            except: continue
        return False

    def _check_response(self, response):
        status = response.status
        url = response.url.lower()
        if status in [403, 429] or "cloudflare" in response.headers.get("server", "").lower():
            self.stats["waf_blocks"] += 1
        if "captcha" in url or "challenge" in url:
            self.stats["captchas_detected"] += 1
            self.db.report_captcha(url)

    def generate_live_dashboard(self):
        """Erweitertes Dashboard mit integrierten Charts (Feature 9)."""
        try:
            html = f"""
            <html>
            <head>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <style>
                    body {{ background:#121212; color:white; font-family:sans-serif; text-align:center; }}
                    .grid {{ display:flex; justify-content:center; gap:20px; flex-wrap:wrap; margin-bottom: 30px; }}
                    .card {{ background:#1e1e1e; padding:20px; border-radius:10px; width:200px; }}
                    .card h3 {{ font-size:16px; color:#aaa; margin:0 0 10px 0; }}
                    .card p {{ font-size:36px; margin:0; font-weight:bold; }}
                    .success {{ color:#00ff00; }} .warning {{ color:#ffaa00; }} .danger {{ color:#ff0000; }}
                    .chart-container {{ width: 80%; max-width: 800px; margin: auto; background: #1e1e1e; padding: 20px; border-radius: 10px; }}
                </style>
            </head>
            <body>
                <h1>🚀 OMNI-GOD V6 TITAN LIVE</h1>
                <div class="grid">
                    <div class="card"><h3>Erfolge</h3><p class="success">{self.stats['successes']}</p></div>
                    <div class="card"><h3>In Chats</h3><p class="success">{self.stats['chat_messages']}</p></div>
                    <div class="card"><h3>Versuche</h3><p>{self.stats['attempts']}</p></div>
                    <div class="card"><h3>Links gefunden</h3><p class="warning">{self.stats['links_found']}</p></div>
                    <div class="card"><h3>Captchas / Blocks</h3><p class="danger">{self.stats['captchas_detected']} / {self.stats['waf_blocks']}</p></div>
                </div>
                
                <div class="chart-container">
                    <canvas id="statsChart"></canvas>
                </div>
                
                <script>
                    const ctx = document.getElementById('statsChart').getContext('2d');
                    new Chart(ctx, {{
                        type: 'bar',
                        data: {{
                            labels: ['Erfolge', 'Chats', 'Versuche', 'Captchas', 'WAF Blocks'],
                            datasets: [{{
                                label: 'Bot Performance Metriken',
                                data: [{self.stats['successes']}, {self.stats['chat_messages']}, {self.stats['attempts']}, {self.stats['captchas_detected']}, {self.stats['waf_blocks']}],
                                backgroundColor: ['#00ff00', '#00ffff', '#ffffff', '#ff0000', '#ff8800']
                            }}]
                        }},
                        options: {{ scales: {{ y: {{ beginAtZero: true, grid: {{ color: '#333' }} }} }}, plugins: {{ legend: {{ labels: {{ color: 'white' }} }} }} }}
                    }});
                </script>
                <p style="color:#666; margin-top:40px;">Letztes Update: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</p>
            </body>
            </html>
            """
            with open("index.html", "w", encoding="utf-8") as f: f.write(html)
            self.push_live_update()
        except: pass

    def push_live_update(self):
        try:
            subprocess.run(["git", "config", "--global", "user.email", "bot@omnigod.com"], check=False)
            subprocess.run(["git", "config", "--global", "user.name", "OmniGodBot"], check=False)
            subprocess.run(["git", "add", "index.html", "bot_data_v6.db"], check=False)
            subprocess.run(["git", "commit", "-m", f"V6 Titan Update {datetime.now().strftime('%H:%M')}"], check=False)
            subprocess.run(["git", "push"], check=False)
        except: pass

    def send_email_report(self):
        if not self.email_password or self.email_password == "Max1234567890123": return
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_sender; msg['To'] = self.email_receiver
            msg['Subject'] = f"📊 OMNI-GOD V6 REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            body = f"TITAN REPORT\nLinks: {self.stats['links_found']}\nErfolge: {self.stats['successes']}\nCaptchas: {self.stats['captchas_detected']}\nBlocks: {self.stats['waf_blocks']}"
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587); server.starttls()
            server.login(self.email_sender, self.email_password)
            server.send_message(msg); server.quit()
        except: pass

if __name__ == "__main__":
    bot = OmniGodBot()
    if sys.platform == "win32": asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try: asyncio.run(bot.start())
    except KeyboardInterrupt: logger.info("🛑 Manuell gestoppt.")
    except Exception as e: logger.critical(f"💥 CRASH: {e}")
    finally: bot.generate_live_dashboard()
