import json
import random
import asyncio
import logging
import sys
import os
import re
from typing import List, Dict, Set, Optional
from playwright.async_api import async_playwright, Page, BrowserContext, ElementHandle

# === MAXIMALE LOGGING KONFIGURATION ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('ultra_god_mode.log')]
)
logger = logging.getLogger("ULTRA_GOD_MODE")

class OmniGodBot:
    def __init__(self, config_path: str = 'bot_config.json'):
        self.config_path = config_path
        self.config = self._load_config()
        self.stats = {"attempts": 0, "successes": 0, "failures": 0, "logins": 0}
        self.visited_links: Set[str] = set()
        self.target_queue: Optional[asyncio.Queue] = None 
        # Externe Dateien für maximale Power
        self.accounts_file = 'accounts.json'
        self.session_file = 'session.json'
        self.proxy_file = 'proxies.txt' # Optional für später

    def _load_config(self) -> Dict:
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info("✅ Config geladen.")
                return data
        except Exception as e:
            logger.error(f"⚠️ Config Fehler: {e}. Nutze Default.")
            return {
                "keywords": ["Schach spielen"],
                "parts": ["Schau mal hier", "Interessant:", "Neuheit:"],
                "messages": ["https://profischach.netlify.app/"],
                "user_agents": [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                ]
            }

    def _load_accounts(self) -> List[Dict]:
        """EXTREM: Lädt Login-Daten aus der externen accounts.json."""
        if os.path.exists(self.accounts_file):
            try:
                with open(self.accounts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except: return []
        return []

    def _build_message(self) -> str:
        """Erstellt eine Nachricht ohne die Formatierungs-Klammern."""
        if 'parts' in self.config and self.config['parts']:
            prefix = random.choice(self.config['parts'])
            main = random.choice(self.config['messages'])
            msg = f"{prefix} {main}"
            return msg.replace("[", "").replace("]", "")
        return random.choice(self.config['messages'])

    async def auto_login(self, page: Page, link: str):
        """EXTREM: Volle Login-Automatisierung für bekannte Domains."""
        accounts = self._load_accounts()
        for acc in accounts:
            if acc.get("domain") in link:
                logger.info(f"🔑 Erkenne Account-Pflicht für {acc.get('domain')}. Starte Login...")
                try:
                    # Riesige Liste an Selektoren für alle Foren-Typen (vBulletin, XenForo, MyBB)
                    user_selectors = ["input[name*='user']", "input[name*='login']", "input[name*='name']", "input[type='text']", "input[id*='user']", "#login-username"]
                    pass_selectors = ["input[name*='pass']", "input[type='password']", "input[id*='pass']", "#login-passwd"]
                    
                    for u_sel in user_selectors:
                        try:
                            u_field = await page.query_selector(u_sel)
                            if u_field and await u_field.is_visible():
                                await u_field.fill(acc['username'])
                                break
                        except: continue
                    
                    for p_sel in pass_selectors:
                        try:
                            p_field = await page.query_selector(p_sel)
                            if p_field and await p_field.is_visible():
                                await p_field.fill(acc['password'])
                                break
                        except: continue
                    
                    await page.keyboard.press("Enter")
                    await page.wait_for_load_state("networkidle", timeout=5000)
                    logger.info(f"✅ Login für {acc.get('domain')} abgeschlossen.")
                    self.stats["logins"] += 1
                except Exception as e:
                    logger.error(f"❌ Login-Fehler auf {link}: {e}")

    async def solve_captchas(self, page: Page):
        """Sucht nach Google ReCaptcha und Cloudflare."""
        for frame in page.frames:
            try:
                # ReCaptcha
                captcha = await frame.query_selector("span#recaptcha-anchor")
                if captcha:
                    logger.info("🛡️ ReCaptcha entdeckt! Versuche Klick...")
                    await captcha.click()
                    await asyncio.sleep(3)
                # Cloudflare
                cf = await frame.query_selector("input[type='checkbox']")
                if cf and "cloudflare" in frame.url:
                    logger.info("🛡️ Cloudflare erkannt! Klicke Checkbox...")
                    await cf.click()
            except: continue

    async def accept_everything(self, page: Page):
        """Beseitigt Cookie-Banner, AGBs und Popups mit Gewalt."""
        selectors = [
            "button:has-text('Zustimmen')", "button:has-text('Akzeptieren')", 
            "button:has-text('Agree')", "button:has-text('OK')", "button:has-text('Accept')",
            "button:has-text('Alles erlauben')", "#save", ".close-button", ".modal-close"
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
        """Simuliert Mausbewegungen und Scrollen gegen Bot-Sperren."""
        try:
            width, height = 1280, 720
            for _ in range(random.randint(3, 6)):
                await page.mouse.move(random.randint(0, width), random.randint(0, height), steps=15)
            await page.mouse.wheel(0, random.randint(300, 800))
            await asyncio.sleep(random.uniform(1.0, 2.5))
        except: pass

    async def try_post_in_frame(self, frame, link: str) -> bool:
        """KERN-LOGIK: Sucht und füllt Textfelder in jedem Frame."""
        # Fast 20 verschiedene Selektoren für maximale Trefferrate
        selectors = [
            "textarea", "div[contenteditable='true']", "[role='textbox']", 
            "#message", ".cke_editable", ".fr-element", ".ProseMirror", 
            "input[name='message']", "textarea[name='comment_text']",
            "#vB_Editor_QR_textarea", "#quick_reply_textarea", ".redactor-editor"
        ]
        
        for sel in selectors:
            try:
                field = await frame.wait_for_selector(sel, timeout=2500, state="visible")
                if field:
                    logger.info(f"🎯 Treffer! Feld gefunden: {sel} auf {link}")
                    await field.scroll_into_view_if_needed()
                    await field.click()
                    await asyncio.sleep(0.8)
                    
                    msg = self._build_message()
                    # EXTREM: Wir löschen erst, falls alter Text drin steht
                    await field.fill("")
                    # Tippen wie ein Mensch
                    await field.type(msg, delay=random.randint(15, 35))
                    await asyncio.sleep(1.5)
                    
                    # Absende-Strategie: Enter + Button-Scan
                    await frame.keyboard.press("Enter")
                    
                    buttons = await frame.query_selector_all("button, input[type='submit'], .btn-primary")
                    for b in buttons:
                        try:
                            txt = await b.inner_text()
                            if any(x in txt.lower() for x in ["post", "send", "antwor", "reply", "absenden", "erstellen", "submit"]):
                                await b.click()
                                logger.info(f"🚀 ERFOLGREICH ABSENDEN geklickt!")
                                return True
                        except: continue
                    return True # Wenn Enter gereicht hat
            except: continue
        return False

    async def process_queue(self, context: BrowserContext):
        """Endlos-Worker für die Queue-Verarbeitung."""
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
            
            # Anti-Bot-Header
            await page.set_extra_http_headers({"Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7"})

            try:
                logger.info(f"🌐 Anflug auf: {link}")
                # Timeout auf 45s erhöht für langsame Foren
                response = await page.goto(link, timeout=45000, wait_until="domcontentloaded")
                
                if response.status >= 400:
                    logger.warning(f"⚠️ Seite gab Fehler {response.status} zurück.")
                    self.stats["failures"] += 1
                else:
                    # Volles Programm: Cookies -> Logins -> Captchas -> Human -> Posting
                    await self.accept_everything(page)
                    await self.auto_login(page, link)
                    await self.solve_captchas(page)
                    await self.human_emulation(page)
                    
                    posted = False
                    for frame in page.frames:
                        if await self.try_post_in_frame(frame, link):
                            self.stats["successes"] += 1
                            posted = True
                            break
                    
                    if not posted:
                        # PLAN B: JavaScript Gewalt-Injektion
                        try:
                            await page.evaluate(f"""() => {{
                                let t = document.querySelector('textarea');
                                if(t) {{ t.value = "{self._build_message()}"; t.dispatchEvent(new Event('input')); }}
                            }}""")
                        except: pass
                        self.stats["failures"] += 1

            except Exception as e:
                logger.debug(f"⚠️ Link-Fehler: {str(e)[:50]}")
                self.stats["failures"] += 1
            finally:
                await page.close()
                self.target_queue.task_done()
                # Zufällige Pause gegen Erkennung
                await asyncio.sleep(random.uniform(5, 12))

    async def perform_search(self, context: BrowserContext, engine: str, url_pattern: str, kw: str):
        """Erntet Links von Suchmaschinen."""
        page = await context.new_page()
        try:
            for p_idx in range(5): # 5 Seiten pro Keyword für mehr Ziele
                offset = p_idx * 10
                search_url = url_pattern.format(kw=kw, offset=offset)
                logger.info(f"🔎 {engine} Suche: {kw} (Seite {p_idx+1})")
                
                await page.goto(search_url, timeout=30000)
                await asyncio.sleep(3)
                await self.accept_everything(page)
                
                links = await page.eval_on_selector_all("a", "nodes => nodes.map(n => n.href)")
                count = 0
                for link in links:
                    if link.startswith("http") and not any(x in link for x in ["google", "bing", "microsoft", "duckduckgo", "facebook"]):
                        await self.target_queue.put(link)
                        count += 1
                logger.info(f"📥 {count} neue Links in die Warteschlange gepackt.")
        except Exception as e:
            logger.error(f"❌ Such-Fehler bei {engine}: {e}")
        finally:
            await page.close()

    async def start(self):
        self.target_queue = asyncio.Queue()
        async with async_playwright() as p:
            logger.info("🔥 GIGA-MODUS GESTARTET. NICHTS WIRD GELÖSCHT.")
            
            # Browser-Konfiguration für maximale Tarnung
            browser = await p.chromium.launch(headless=True, args=[
                '--no-sandbox', '--disable-setuid-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars', '--window-position=0,0'
            ])
            
            # EXTREM: Bestehende Session laden
            storage = self.session_file if os.path.exists(self.session_file) else None
            context = await browser.new_context(
                storage_state=storage,
                user_agent=random.choice(self.config['user_agents']),
                viewport={'width': 1920, 'height': 1080}
            )

            # Such-Definitionen
            search_engines = [
                ("Bing", "https://www.bing.com/search?q={kw}+forum&first={offset}"),
                ("Google", "https://www.google.com/search?q={kw}+forum&start={offset}")
            ]

            # Tasks erstellen
            search_tasks = []
            for kw in self.config['keywords']:
                for name, url in search_engines:
                    search_tasks.append(self.perform_search(context, name, url, kw))

            # 5 Worker starten für parallele Bearbeitung
            workers = [asyncio.create_task(self.process_queue(context)) for _ in range(5)]

            # Suche durchführen
            await asyncio.gather(*search_tasks)
            
            # Warten bis Queue abgearbeitet
            try:
                await asyncio.wait_for(self.target_queue.join(), timeout=600)
            except asyncio.TimeoutError:
                logger.info("⏳ Zeitlimit für heute erreicht.")

            # EXTREM: Session für das nächste Mal speichern (Cookies!)
            await context.storage_state(path=self.session_file)
            logger.info(f"💾 Session in {self.session_file} gesichert.")

            for w in workers: w.cancel()
            await browser.close()
            self._final_summary()

    def _final_summary(self):
        print("\n" + "█"*60)
        print(f"📊 DER ULTIMATIVE BERICHT")
        print(f"✅ Erfolgreiche Posts: {self.stats['successes']}")
        print(f"🔑 Logins durchgeführt: {self.stats['logins']}")
        print(f"Attempted: {self.stats['attempts']} | Gefundene URLs: {len(self.visited_links)}")
        print("█"*60 + "\n")

if __name__ == "__main__":
    bot = OmniGodBot()
    # Windows-Fix für Asyncio
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(bot.start())
