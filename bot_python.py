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
        self.target_queue: Optional[asyncio.Queue] = None 

    def _load_config(self) -> Dict:
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "keywords": ["Schach spielen"],
                "parts": ["Schau mal hier", "Interessant:", "Neuheit:"],
                "messages": ["https://profischach.netlify.app/"],
                "user_agents": [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                ]
            }

    def _build_message(self) -> str:
        if 'parts' in self.config and self.config['parts']:
            prefix = random.choice(self.config['parts'])
            main = random.choice(self.config['messages'])
            msg = f"{prefix} {main}"
            return msg.replace("[", "").replace("]", "")
        return random.choice(self.config['messages'])

    async def solve_captchas(self, page: Page):
        """Sucht nach Google ReCaptcha Kästchen und klickt sie an."""
        frames = page.frames
        for frame in frames:
            try:
                captcha_checkbox = await frame.query_selector("span#recaptcha-anchor")
                if captcha_checkbox:
                    logger.info("🛡️ Captcha erkannt! Versuche Kästchen zu klicken...")
                    await captcha_checkbox.click()
                    await asyncio.sleep(2)
            except:
                continue

    async def accept_terms_and_cookies(self, page: Page):
        """Sucht nach AGB-Bestätigungen, Cookie-Bannern und 'Zustimmen'-Buttons."""
        terms_selectors = [
            "button:has-text('Akzeptieren')", "button:has-text('Zustimmen')", 
            "button:has-text('Alle akzeptieren')", "button:has-text('Agree')",
            "button:has-text('Accept all')", "button:has-text('OK')",
            "button:has-text('Ich stimme zu')", "#accept-choices", ".css-at769",
            "button.accept", "button.consent-give", "a.cc-btn.cc-dismiss"
        ]
        
        for frame in page.frames:
            for sel in terms_selectors:
                try:
                    btn = await frame.query_selector(sel)
                    if btn and await btn.is_visible():
                        logger.info(f"🍪 Cookie/AGB-Banner erkannt ({sel}). Klicke...")
                        await btn.click()
                        await asyncio.sleep(1)
                except:
                    continue

    async def human_emulation(self, page: Page):
        """Simuliert komplexe menschliche Bewegungsmuster."""
        try:
            for _ in range(random.randint(2, 4)):
                await page.mouse.move(random.randint(100, 700), random.randint(100, 700), steps=10)
            await page.mouse.wheel(0, random.randint(200, 600))
            await asyncio.sleep(random.uniform(0.5, 1.5))
        except: pass

    async def perform_search(self, context: BrowserContext, engine_name: str, url_pattern: str, kw: str):
        """Parallel-Task für die Suchmaschinen-Kaskade."""
        page = await context.new_page()
        try:
            for page_nr in range(3): # Reduziert auf 3 Seiten für Speed
                offset = page_nr * 10
                url = url_pattern.format(kw=kw, offset=offset)
                logger.info(f"🔎 {engine_name} Scan (Seite {page_nr+1})...")
                
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await self.accept_terms_and_cookies(page)
                await asyncio.sleep(2)
                
                links = await page.eval_on_selector_all("a", "nodes => nodes.map(n => n.href)")
                for link in links:
                    if link.startswith("http") and not any(x in link for x in ["google", "bing", "microsoft", "duckduckgo"]):
                        await self.target_queue.put(link)
                        
        except Exception as e:
            logger.error(f"❌ {engine_name} Fehler: {str(e)[:50]}")
        finally:
            await page.close()

    async def try_post_in_frame(self, frame, link: str) -> bool:
        """Versucht in einem spezifischen Frame zu posten mit erweiterten Techniken."""
        selectors = [
            "textarea", "div[contenteditable='true']", "[role='textbox']",
            "input[name='message']", "#message", "#vB_Editor_QR_textarea",
            "#quickreply_textarea", ".cke_editable", ".fr-element", 
            ".redactor-editor", ".ql-editor", ".tox-edit-area", ".ProseMirror",
            "textarea[name='post_message']", "textarea[name='comment_text']"
        ]

        for sel in selectors:
            try:
                # Warten bis Element da ist
                field = await frame.wait_for_selector(sel, timeout=2000, state="visible")
                if field:
                    logger.info(f"🎯 Feld gefunden: {sel}")
                    await field.scroll_into_view_if_needed()
                    await field.click() # Fokus setzen
                    await asyncio.sleep(0.5)
                    
                    msg = self._build_message()
                    # Alternative Schreibmethode für schwierige Felder
                    await field.fill("") # Erst leeren
                    await field.type(msg, delay=20) 
                    
                    await asyncio.sleep(1)
                    
                    # Absenden Strategie 1: Enter
                    await frame.keyboard.press("Enter")
                    
                    # Absenden Strategie 2: Button Suche
                    buttons = await frame.query_selector_all("button, input[type='submit'], .button")
                    for b in buttons:
                        try:
                            t = await b.inner_text()
                            if any(x in t.lower() for x in ["post", "send", "antwor", "reply", "submit", "senden", "erstellen"]):
                                await b.click()
                                logger.info(f"🚀 ABSENDEN geklickt auf {link}")
                                return True
                        except: continue
                    
                    # Wenn Enter gedrückt wurde, werten wir es auch als Versuch
                    return True
            except:
                continue
        return False

    async def process_queue(self, context: BrowserContext):
        """Worker-Schleife: Verarbeitet Ziele asynchron."""
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
                logger.info(f"🌐 Zielanflug: {link}")
                # Schnelles Laden
                await page.goto(link, timeout=30000, wait_until="commit")
                
                # Schritt 1: Überwinde AGBs/Cookies
                await self.accept_terms_and_cookies(page)
                await asyncio.sleep(1)
                
                # Schritt 2: Menschlich wirken
                await self.human_emulation(page)

                # Schritt 3: In allen Frames nach Feldern suchen
                posted = False
                all_frames = page.frames
                for frame in all_frames:
                    if await self.try_post_in_frame(frame, link):
                        logger.info(f"✅ Nachricht eingetippt auf {link}")
                        self.stats["successes"] += 1
                        posted = True
                        break

                if not posted:
                    self.stats["failures"] += 1
                    # Letzter Versuch: JavaScript Inject
                    try:
                        await page.evaluate("""() => {
                            let tx = document.querySelector('textarea');
                            if(tx) { tx.value = 'Interessante Seite!'; tx.dispatchEvent(new Event('input')); }
                        }""")
                    except: pass

            except Exception as e:
                logger.debug(f"⚠️ Seite übersprungen: {link}")
            finally:
                await page.close()
                self.target_queue.task_done()
                await asyncio.sleep(random.uniform(2, 5))

    async def start(self):
        self.target_queue = asyncio.Queue()
        async with async_playwright() as p:
            logger.info("🔥 EXTREM-MODUS AKTIVIERT: Suche & AGB-Bypass")
            browser = await p.chromium.launch(headless=True, args=[
                '--no-sandbox', 
                '--disable-setuid-sandbox', 
                '--disable-blink-features=AutomationControlled',
                '--use-fake-ui-for-media-stream'
            ]) 
            
            context = await browser.new_context(
                user_agent=random.choice(self.config['user_agents']),
                viewport={'width': 1280, 'height': 720}
            )

            engines = [
                ("Bing", "https://www.bing.com/search?q={kw}+forum&first={offset}"),
                ("Google", "https://www.google.com/search?q={kw}+forum&start={offset}")
            ]

            # Suche starten
            search_tasks = []
            for kw in self.config['keywords']:
                for name, url in engines:
                    search_tasks.append(self.perform_search(context, name, url, kw))

            # Worker starten
            workers = [asyncio.create_task(self.process_queue(context)) for _ in range(5)]

            await asyncio.gather(*search_tasks)
            
            # Warten bis Queue leer oder Timeout
            try:
                await asyncio.wait_for(self.target_queue.join(), timeout=300)
            except asyncio.TimeoutError:
                logger.info("⏳ Zeitlimit für Queue erreicht.")

            for w in workers: w.cancel()
            await browser.close()
            self._final_summary()

    def _final_summary(self):
        print("\n" + "█"*60)
        print(f"📊 EXTREM-REPORT")
        print(f"Erfolge: {self.stats['successes']} | Versuche: {self.stats['attempts']}")
        print(f"Gefundene URLs: {len(self.visited_links)}")
        print("█"*60 + "\n")

if __name__ == "__main__":
    bot = OmniGodBot()
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(bot.start())
