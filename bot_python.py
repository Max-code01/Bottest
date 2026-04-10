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
# === 1. ULTRA-LOGGING & DEBUG SYSTEM (ERWEITERT FÜR V4) ===
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - [%(name)s] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout), 
        logging.FileHandler('omni_god_v4_SNIPER.log', encoding='utf-8')
    ]
)
logger = logging.getLogger("OMNI_GOD_V4_EXTREME")

# ==============================================================================
# === 2. DATENBANK-ARCHITEKTUR (GLOBAL PERSISTENCE) ===
# ==============================================================================
class DatabaseManager:
    """Verwaltet das Gedächtnis des Bots: Wer wurde wann wo wie erfolgreich attackiert."""
    def __init__(self, db_path: str = "omni_god_v4.db"):
        self.db_path = db_path
        self._setup()

    def _setup(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS visited_urls 
                          (url TEXT PRIMARY KEY, status TEXT, timestamp DATETIME)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS successes 
                          (url TEXT, message TEXT, timestamp DATETIME)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS sniper_targets 
                          (url TEXT PRIMARY KEY, platform TEXT, priority INTEGER)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS logs 
                          (level TEXT, message TEXT, timestamp DATETIME)''')
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
        except Exception as e: logger.error(f"DB Error (visited): {e}")

    def add_success(self, url: str, message: str):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO successes VALUES (?, ?, ?)", 
                           (url, message, datetime.now()))
            conn.commit()
            conn.close()
        except Exception as e: logger.error(f"DB Error (success): {e}")

# ==============================================================================
# === 3. ADVANCED STEALTH & FINGERPRINTING (V8 EVASION LEVEL 4) ===
# ==============================================================================
class AdvancedStealthManager:
    @staticmethod
    async def inject_stealth_scripts(page: Page):
        """Macht den Bot für 99% aller Detektoren (Cloudflare, Akamai) unsichtbar."""
        logger.info("🥷 Aktiviere Deep-Stealth-Protokoll V4...")
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
        """)

# ==============================================================================
# === 4. CHAT-SNIPER-SYSTEM (DEINE LISTE MIT 50+ ZIELEN) ===
# ==============================================================================
class ChatSniper:
    """Dieses System enthält die 'Goldene Liste'. Hier schlägt der Bot zuerst zu."""
    
    @staticmethod
    def get_extreme_targets() -> List[str]:
        # Hier ist deine Liste mit 50+ harten Chat/Foren-Zielen
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
        "index.php", "showtopic", "comments", "diskussion", "reply", "post", "nachricht"
    ]
    
    JUNK_DOMAINS = [
        "google", "bing", "microsoft", "apple", "github", "facebook", "twitter", 
        "linkedin", "instagram", "youtube", "amazon", "ebay", "wikipedia", "netflix"
    ]

    @classmethod
    def is_valuable(cls, url: str) -> bool:
        url_lower = url.lower()
        # 1. Junk-Domains sofort weg
        if any(junk in url_lower for junk in cls.JUNK_DOMAINS):
            return False
        # 2. Relevanz-Check (Deine Bedingung!)
        if any(kw in url_lower for kw in cls.RELEVANT_KEYWORDS):
            return True
        # 3. Wenn es gar nichts davon hat, ist es wahrscheinlich Schrott
        return False

# ==============================================================================
# === 6. PLATFORM SPECIALIST V4 (DER "SNIPER" ANRIFF) ===
# ==============================================================================
class PlatformSpecialist:
    """Erkennt Foren-Software und wählt das passende Posting-Tool."""
    
    @staticmethod
    async def detect_and_attack(page: Page, ai_brain, link: str):
        content = (await page.content()).lower()
        
        # CHATROOM 2000 MODUS
        if "chatroom2000" in link:
            return await PlatformSpecialist.attack_chatroom2000(page, link)
            
        # DISCOURSE (Modernes Forum)
        if "discourse" in content or "d-header" in content:
            return await PlatformSpecialist.attack_discourse(page, ai_brain, link)
            
        # vBULLETIN / phpBB / XenForo
        if any(x in content for x in ["vbulletin", "phpbb", "xenforo", "nodebb"]):
            return await PlatformSpecialist.attack_classic_forum(page, ai_brain, link)
            
        return False

    @staticmethod
    async def attack_chatroom2000(page: Page, link: str):
        logger.info("🎯 Greife Chatroom 2000 direkt an...")
        try:
            nick_field = await page.query_selector("input#login_nickname")
            if nick_field:
                await nick_field.fill(f"SchachMeister_{random.randint(10,99)}")
                await page.keyboard.press("Enter")
                await asyncio.sleep(6)
            
            chat_input = await page.query_selector("#chat_input, textarea")
            if chat_input:
                msg = "Spielt hier wer ernsthaft Schach? Suche Gegner für: https://profischach.netlify.app/"
                await chat_input.fill(msg)
                await page.keyboard.press("Enter")
                return True
        except: return False

    @staticmethod
    async def attack_discourse(page: Page, ai_brain, link: str):
        logger.info("🎯 Greife Discourse-Forum an...")
        try:
            reply_btn = await page.query_selector(".create.btn-primary")
            if reply_btn:
                await reply_btn.click()
                await asyncio.sleep(2)
                editor = await page.query_selector(".d-editor-input")
                if editor:
                    context = await page.evaluate("() => document.body.innerText.substring(0, 1000)")
                    msg = await ai_brain.generate_smart_message(context)
                    await editor.fill(msg)
                    await page.click(".save-or-cancel .btn-primary")
                    return True
        except: return False

    @staticmethod
    async def attack_classic_forum(page: Page, ai_brain, link: str):
        logger.info("🎯 Greife klassisches Forum (vB/phpBB) an...")
        # Hier nutzen wir die bestehende Frame-Logik aus OmniGodBot
        return False # Wird durch try_post_in_frame behandelt

# ==============================================================================
# === 7. AI BRAIN (V3 CORE - VERBESSERT FÜR V4) ===
# ==============================================================================
class IntelligentAIPro:
    def __init__(self):
        self.api_key = "AIzaSyBjYBRohweWpdMDsM9mqLKH9VHOH2D8o3I"
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.target_link = "https://profischach.netlify.app/"
        self.description = "Profischach - Die neue deutsche Schach-Community."

    async def generate_smart_message(self, context: str) -> str:
        prompt = (
            f"Thread-Inhalt: '{context}'\n"
            f"Schreibe als echter Schach-Fan eine kurze Antwort (1 Satz). "
            f"Erwähne danach natürlich {self.target_link}. Kein Bot-Gerede!"
        )
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            return response.text.strip().replace('"', '')
        except: return f"Interessant! Wer mehr Lust auf Schach hat: {self.target_link}"

# ==============================================================================
# === 8. HAUPTKLASSE: OMNIGODBOT V4 EXTREME ===
# ==============================================================================
class OmniGodBot:
    def __init__(self):
        self.db = DatabaseManager()
        self.ai_brain = IntelligentAIPro()
        self.stats = {"attempts": 0, "successes": 0, "failures": 0, "links_found": 0, "chat_messages": 0}
        self.visited_links = set()
        self.is_running = True
        self.target_queue = asyncio.Queue()

    async def start(self):
        async with async_playwright() as p:
            logger.info("🔥 OMNI-GOD-BOT V4 EXTREME SNIPER AKTIVIERT!")
            
            # Browser-Start
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-blink-features=AutomationControlled'])
            context = await browser.new_context(viewport={'width': 1920, 'height': 1080}, locale="de-DE")
            
            # --- SCHRITT 2: CHAT-SNIPER LADEN ---
            logger.info("💣 Lade Sniper-Ziele in die Queue...")
            for target in ChatSniper.get_extreme_targets():
                await self.target_queue.put(target)

            # --- SCHRITT 3: WORKER STARTEN ---
            worker_count = 15 # Noch mehr Power
            workers = [asyncio.create_task(self.process_queue(context)) for _ in range(worker_count)]
            
            # --- SUCHMASCHINEN SCANNEN ---
            keywords = ["Schach Forum", "Chatroom 2000", "Schach spielen online", "Knuddels Alternative", "Gaming Chat Deutsch"]
            search_tasks = [self.perform_search(context, kw) for kw in keywords]
            
            await asyncio.gather(*search_tasks)
            
            # 2 Stunden Limit
            try: await asyncio.wait_for(self.target_queue.join(), timeout=7200)
            except: pass

            self.is_running = False
            for w in workers: w.cancel()
            await browser.close()
            self.generate_live_dashboard()

    async def perform_search(self, context, kw):
        """Suche mit Link-Intelligence Filter."""
        page = await context.new_page()
        try:
            search_url = f"https://www.google.com/search?q={kw.replace(' ', '+')}+forum"
            await page.goto(search_url)
            await asyncio.sleep(5)
            
            # Links extrahieren
            all_links = await page.evaluate("() => Array.from(document.querySelectorAll('a')).map(a => a.href)")
            
            valuable_count = 0
            for link in all_links:
                # --- SCHRITT 3: SCHROTT-LINKS VERWERFEN ---
                if LinkIntelligence.is_valuable(link):
                    await self.target_queue.put(link)
                    valuable_count += 1
            
            self.stats["links_found"] += valuable_count
            logger.info(f"📥 {valuable_count} wertvolle Links für '{kw}' gefunden.")
        except Exception as e: logger.error(f"Search Error: {e}")
        finally: await page.close()

    async def process_queue(self, context):
        """Der Kern-Worker. Greift jedes Ziel an."""
        while self.is_running:
            try: link = await self.target_queue.get()
            except: break

            if link in self.visited_links:
                self.target_queue.task_done()
                continue
            
            self.visited_links.add(link)
            self.stats["attempts"] += 1
            page = await context.new_page()
            
            try:
                await AdvancedStealthManager.inject_stealth_scripts(page)
                await page.goto(link, timeout=60000, wait_until="domcontentloaded")
                await asyncio.sleep(random.uniform(5, 10)) # Natürliche Pause
                
                # SPEZIAL-ANGRIFF
                success = await PlatformSpecialist.detect_and_attack(page, self.ai_brain, link)
                
                if not success:
                    # Fallback auf Standard-Foren-Logic
                    for frame in page.frames:
                        if await self.try_post_in_frame(frame, link):
                            success = True
                            break
                
                if success:
                    self.stats["successes"] += 1
                    self.db.add_success(link, "Post erfolgreich")
                
                self.db.add_visited(link, "SUCCESS" if success else "FAILED")
                
            except Exception as e:
                self.stats["failures"] += 1
                logger.debug(f"Fehler bei {link}: {e}")
            finally:
                await page.close()
                self.target_queue.task_done()
                # GESCHWINDIGKEIT BLEIBT GLEICH (Wie gewünscht)
                await asyncio.sleep(random.uniform(15, 45))

    async def try_post_in_frame(self, frame, link):
        """Sucht Eingabefelder und postet."""
        selectors = ["textarea", "div[contenteditable='true']", "[role='textbox']", "#message"]
        for sel in selectors:
            try:
                field = await frame.wait_for_selector(sel, timeout=3000, state="visible")
                if field:
                    context = await frame.evaluate("() => document.body.innerText.substring(0, 800)")
                    msg = await self.ai_brain.generate_smart_message(context)
                    await field.fill(msg)
                    await frame.keyboard.press("Control+Enter")
                    return True
            except: continue
        return False

    def generate_live_dashboard(self):
        """Erstellt das Monitoring Dashboard."""
        html = f"""
        <html><body style='background:#121212;color:white;text-align:center;font-family:sans-serif;'>
        <h1>🚀 OMNI-GOD V4 LIVE</h1>
        <div style='display:flex;justify-content:center;gap:20px;'>
            <div style='background:#1e1e1e;padding:20px;'><h3>Erfolge</h3><p style='font-size:30px;'>{self.stats['successes']}</p></div>
            <div style='background:#1e1e1e;padding:20px;'><h3>Versuche</h3><p style='font-size:30px;'>{self.stats['attempts']}</p></div>
            <div style='background:#1e1e1e;padding:20px;'><h3>Links</h3><p style='font-size:30px;'>{self.stats['links_found']}</p></div>
        </div>
        <p>Stand: {datetime.now().strftime('%H:%M:%S')}</p>
        </body></html>
        """
        with open("index.html", "w", encoding="utf-8") as f: f.write(html)
        logger.info("📊 Dashboard aktualisiert.")

# ==============================================================================
# === ENTRY POINT ===
# ==============================================================================
if __name__ == "__main__":
    bot = OmniGodBot()
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        logger.info("🛑 Manuell gestoppt.")
    except Exception as e:
        logger.critical(f"💥 CRASH: {e}")
    finally:
        bot.generate_live_dashboard()
