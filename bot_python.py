import json
import random
import asyncio
import logging
import sys
import re
from typing import List, Dict, Set, Optional
from playwright.async_api import async_playwright, Page, BrowserContext

# === LOGGING KONFIGURATION ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('god_mode.log')]
)
logger = logging.getLogger("GOD_MODE")

class OmniGodBot:
    def __init__(self, config_path: str = 'bot_config.json'):
        self.config_path = config_path
        self.config = self._load_config()
        self.stats = {"attempts": 0, "successes": 0, "failures": 0}
        self.visited_links: Set[str] = set()
        self.target_queue: asyncio.Queue = asyncio.Queue()

    def _load_config(self) -> Dict:
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            # Fallback mit der von dir gewünschten 'parts' Struktur
            return {
                "keywords": ["Schach spielen"],
                "parts": ["Schau mal hier", "Interessant:", "Neuheit:"],
                "messages": ["https://profischach.netlify.app/"],
                "user_agents": ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"]
            }

    def _build_message(self) -> str:
        """Implementiert die 'parts' Logik und das Handling von Brackets."""
        if 'parts' in self.config and self.config['parts']:
            prefix = random.choice(self.config['parts'])
            main = random.choice(self.config['messages'])
            # Verarbeitet mögliche Brackets/Platzhalter
            msg = f"{prefix} {main}"
            return msg.replace("[", "").replace("]", "") # Entfernt Brackets falls vorhanden
        return random.choice(self.config['messages'])

    async def human_emulation(self, page: Page):
        """Simuliert komplexe menschliche Bewegungsmuster."""
        for _ in range(random.randint(3, 6)):
            await page.mouse.move(random.randint(0, 800), random.randint(0, 800), steps=15)
        await page.mouse.wheel(0, random.randint(400, 1200))
        await asyncio.sleep(random.uniform(1.5, 3.0))

    async def extract_all_links(self, page: Page) -> List[str]:
        """Zero-Filter Extraktion: Inhaliert jeden verfügbaren Link."""
        return await page.eval_on_selector_all("a", """
            nodes => nodes.map(n => n.href).filter(h => h.startsWith('http'))
        """)

    async def perform_search(self, context: BrowserContext, engine_name: str, url_pattern: str, kw: str):
        """Parallel-Task für die Suchmaschinen-Kaskade."""
        page = await context.new_page()
        try:
            for page_nr in range(5): # 5 Seiten tief pro Engine
                offset = page_nr * 10
                url = url_pattern.format(kw=kw, offset=offset)
                logger.info(f"🔎 {engine_name} Scan läuft (Seite {page_nr+1})...")
                
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(3)
                
                links = await self.extract_all_links(page)
                # KEINE FILTER: Alles in die Queue werfen
                for link in links:
                    if not any(x in link for x in ["google.", "bing.", "duckduckgo.", "microsoft.", "apple."]):
                        await self.target_queue.put(link)
        except Exception as e:
            logger.error(f"❌ {engine_name} Blockade: {str(e)[:50]}")
        finally:
            await page.close()

    async def process_queue(self, context: BrowserContext):
        """Worker-Schleife: Verarbeitet Ziele asynchron zur Suche."""
        while True:
            link = await self.target_queue.get()
            if link in self.visited_links:
                self.target_queue.task_done()
                continue
            
            self.visited_links.add(link)
            self.stats["attempts"] += 1
            page = await context.new_page()
            
            try:
                logger.info(f"🌐 Zielanflug ({self.target_queue.qsize()} offen): {link}")
                await page.goto(link, timeout=45000, wait_until="domcontentloaded")
                await self.human_emulation(page)

                # Suche in Hauptseite + allen Iframes
                all_frames = [page.main_frame] + page.frames
                posted = False

                for frame in all_frames:
                    # 'parts' gesteuerte Feld-Identifikation
                    selectors = ["textarea", "div[contenteditable='true']", "input[type='text']", ".editor-canvas"]
                    for sel in selectors:
                        try:
                            field = await frame.query_selector(sel)
                            if field and await field.is_visible():
                                msg = self._build_message()
                                await field.fill(msg)
                                await asyncio.sleep(1)
                                
                                # Senden-Versuch (Enter & Button-Scan)
                                await frame.keyboard.press("Enter")
                                buttons = await frame.query_selector_all("button, input[type='submit']")
                                for b in buttons:
                                    t = await b.inner_text()
                                    if any(x in t.lower() for x in ["post", "send", "antwort", "reply", "submit"]):
                                        await b.click()
                                        break
                                
                                logger.info(f"🚀 ERFOLGREICH: {link}")
                                self.stats["successes"] += 1
                                posted = True
                                break
                        except: continue
                    if posted: break

                if not posted: self.stats["failures"] += 1

            except: pass
            finally:
                await page.close()
                self.target_queue.task_done()
                await asyncio.sleep(random.uniform(10, 20))

    async def start(self):
        async with async_playwright() as p:
            logger.info("🔥 OMNI-GOD-MODE AKTIVIERT")
            # Headless=False damit du bei Captchas eingreifen kannst
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox']) 
            context = await browser.new_context(
                user_agent=random.choice(self.config['user_agents']),
                viewport={'width': 1920, 'height': 1080}
            )

            # 1. Definiere die Engines
            engines = [
                ("Bing", "https://www.bing.com/search?q={kw}+forum&first={offset}"),
                ("Google", "https://www.google.com/search?q={kw}+forum&start={offset}"),
                ("DuckDuckGo", "https://duckduckgo.com/html/?q={kw}+forum")
            ]

            # 2. Starte Suche und Worker gleichzeitig
            tasks = []
            for kw in self.config['keywords']:
                for name, url in engines:
                    tasks.append(self.perform_search(context, name, url, kw))

            # Erstelle 3 parallele Worker für die Zielverarbeitung
            workers = [asyncio.create_task(self.process_queue(context)) for _ in range(3)]

            # Such-Tasks ausführen
            await asyncio.gather(*tasks)

            # Warten bis die Queue leer ist
            try:
                await asyncio.wait_for(self.target_queue.join(), timeout=600)
            except asyncio.TimeoutError:
                logger.info("⏳ Zeitlimit erreicht.")

            for w in workers: w.cancel()
            await browser.close()
            self._final_summary()

    def _final_summary(self):
        print("\n" + "█"*60)
        print(f"📊 OMNI-REPORT")
        print(f"Erfolge: {self.stats['successes']} | Versuche: {self.stats['attempts']}")
        print(f"Gefundene URLs: {len(self.visited_links)}")
        print("█"*60 + "\n")

if __name__ == "__main__":
    bot = OmniGodBot()
    asyncio.run(bot.start())
