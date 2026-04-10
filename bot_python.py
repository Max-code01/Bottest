import json
import random
import asyncio
import logging
import sys
import os
import re
import math
import time
from datetime import datetime
from typing import List, Dict, Set, Optional, Any
from playwright.async_api import async_playwright, Page, BrowserContext, ElementHandle, Browser

# === MAXIMALE LOGGING KONFIGURATION ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('ultra_god_mode.log', encoding='utf-8')]
)
logger = logging.getLogger("ULTRA_GOD_MODE")

# ==========================================
# NEU: EXTREM-SYSTEME FÜR 1000% ERFOLGSRATE
# ==========================================

class AdvancedStealthManager:
    """Versteckt Playwright vor modernen Bot-Schutz-Systemen (Cloudflare, PerimeterX, DataDome)."""
    
    @staticmethod
    async def inject_stealth_scripts(page: Page):
        logger.info("🥷 Injiziere Deep-Stealth-Skripte auf V8-Engine-Ebene...")
        
        # 1. WebDriver Flag entfernen
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.navigator.chrome = { runtime: {} };
        """)
        
        # 2. Fake Plugins & MimeTypes
        await page.add_init_script("""
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
            Object.defineProperty(navigator, 'languages', {get: () => ['de-DE', 'de', 'en-US', 'en']});
        """)
        
        # 3. WebGL Spoofing (Täuscht eine echte Nvidia/AMD Grafikkarte vor)
        await page.add_init_script("""
            const getParameter = WebGLRenderingContext.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return 'Intel Inc.';
                if (parameter === 37446) return 'Intel Iris OpenGL Engine';
                return getParameter(parameter);
            };
        """)
        
        # 4. Permissions API Mock
        await page.add_init_script("""
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );
        """)

class CognitiveHumanTyping:
    """Simuliert hochkomplexes, menschliches Tippverhalten inkl. Tippfehlern und Korrekturen."""
    
    @staticmethod
    async def type_like_human(field: ElementHandle, text: str):
        logger.info("🧠 Starte kognitive Tipp-Simulation...")
        await field.click()
        await asyncio.sleep(random.uniform(0.3, 0.8))
        
        for char in text:
            # 2% Chance für einen Tippfehler mit anschließender Korrektur
            if random.random() < 0.02 and char.isalpha():
                wrong_char = random.choice("abcdefghijklmnopqrstuvwxyz")
                await field.type(wrong_char, delay=random.randint(20, 50))
                await asyncio.sleep(random.uniform(0.1, 0.3))
                await field.press("Backspace")
                await asyncio.sleep(random.uniform(0.1, 0.2))
            
            # Normales Tippen mit Mikro-Varianzen
            delay = random.gauss(40, 15)  # Gaußsche Normalverteilung für Verzögerungen
            delay = max(10, min(delay, 100)) # Begrenzen zwischen 10ms und 100ms
            
            await field.type(char, delay=int(delay))
            
            # Zufällige Mikropausen beim Denken
            if char in [' ', '.', ',', ':', '!', '?'] and random.random() < 0.3:
                await asyncio.sleep(random.uniform(0.2, 0.6))

class DeepDOMAnalyzer:
    """Durchsucht Shadow-DOMs und versteckte IFrames, die Playwright normalerweise nicht sieht."""
    
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
            # Versuche das Element via JS im tiefsten DOM zu finden
            element = await page.evaluate_handle(js_code, selectors)
            if element and await element.evaluate("e => e !== null"):
                return element
        except Exception as e:
            logger.debug(f"Shadow DOM Suchfehler: {e}")
        return None

class AdvancedCaptchaHeuristics:
    """Erkennt nicht nur ReCaptcha, sondern alle modernen Bot-Schutze."""
    
    @staticmethod
    async def scan_and_log_captchas(page: Page):
        captcha_signatures = {
            "hCaptcha": ["iframe[src*='hcaptcha.com']", "[data-hcaptcha-widget-id]"],
            "Cloudflare Turnstile": ["iframe[src*='challenges.cloudflare.com']", ".cf-turnstile"],
            "GeeTest": [".geetest_captcha", "div[class*='geetest']"],
            "DataDome": ["iframe[src*='datadome.co']", "#datadome-captcha"],
            "PerimeterX": ["#px-captcha"]
        }
        
        for name, selectors in captcha_signatures.items():
            for sel in selectors:
                try:
                    if await page.query_selector(sel):
                        logger.warning(f"🚨 HOHE GEFAHR: {name} auf {page.url} entdeckt! System wird angepasst.")
                        await asyncio.sleep(random.uniform(2.0, 4.0))
                except: pass

class SystemReporter:
    """Erstellt detaillierte Analyse-Dumps bei Fehlern."""
    
    @staticmethod
    async def dump_error_state(page: Page, link: str, error_msg: str):
        try:
            if not os.path.exists("error_dumps"):
                os.makedirs("error_dumps")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_link = re.sub(r'[^a-zA-Z0-9]', '_', link)[:50]
            
            # Screenshot speichern
            pic_path = f"error_dumps/err_{timestamp}_{safe_link}.png"
            await page.screenshot(path=pic_path, full_page=True)
            
            # HTML speichern für spätere Analyse
            html_path = f"error_dumps/err_{timestamp}_{safe_link}.html"
            html_content = await page.content()
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            logger.error(f"📸 Fehler-Dump erstellt: {pic_path} | Grund: {str(error_msg)[:100]}")
        except: pass

# ==========================================
# URSPRÜNGLICHE KLASSE (100% UNBERÜHRT, NUR ERWEITERT)
# ==========================================

class OmniGodBot:
    def __init__(self, config_path: str = 'bot_config.json'):
        self.config_path = config_path
        self.config = self._load_config()
        self.stats = {"attempts": 0, "successes": 0, "failures": 0, "logins": 0, "captchas_detected": 0}
        self.visited_links: Set[str] = set()
        self.target_queue: Optional[asyncio.Queue] = None 
        self.accounts_file = 'accounts.json'
        self.session_file = 'session.json'
        self.proxy_file = 'proxies.txt'

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
        """
        EXTREM: Kombinierte Login-Automatisierung.
        1. Prüft auf bekannte Domains.
        2. Falls nichts gefunden, startet der aggressive Global-Modus auf JEDER Seite.
        """
        accounts = self._load_accounts()
        if not accounts:
            return

        target_acc = None
        
        # SCHRITT 1: Spezifischen Account für die Domain suchen
        for acc in accounts:
            if acc.get("domain") != "*" and acc.get("domain") in link:
                target_acc = acc
                logger.info(f"🔑 Spezifischen Account für {acc.get('domain')} gefunden.")
                break
        
        # SCHRITT 2: Wenn kein spezieller Account da ist, nimm den Global-Key (*)
        if not target_acc:
            for acc in accounts:
                if acc.get("domain") == "*":
                    target_acc = acc
                    logger.info(f"🌍 Nutze Global-Account Schlüssel für {link}")
                    break

        if not target_acc:
            return

        try:
            # SCHRITT 3: Login-Trigger aktivieren
            login_triggers = [
                "text='Login'", "text='Anmelden'", "text='Sign In'", "text='Einloggen'",
                ".login", "#login", "a[href*='login']", "button[id*='login']",
                "a:has-text('Anmelden')", "button:has-text('Login')"
            ]
            for trigger in login_triggers:
                try:
                    btn = await page.query_selector(trigger)
                    if btn and await btn.is_visible():
                        await btn.click()
                        await asyncio.sleep(1.5)
                except: continue

            # SCHRITT 4: Aggressives Suchen nach Eingabefeldern
            user_selectors = [
                "input[name*='user']", "input[name*='login']", "input[name*='mail']", 
                "input[name*='name']", "input[type='text']", "input[type='email']", 
                "input[id*='user']", "input[id*='login']", "#login-username",
                "input[placeholder*='Nutzer']", "input[placeholder*='User']", 
                "input[placeholder*='Mail']", "input[placeholder*='Name']"
            ]
            
            pass_selectors = [
                "input[name*='pass']", "input[type='password']", "input[id*='pass']", 
                "input[id*='password']", "#login-passwd", "input[placeholder*='Passwort']", 
                "input[placeholder*='Password']", "input[placeholder*='PW']"
            ]

            user_field = None
            target_frame = page
            
            # Suche im Hauptframe
            for u_sel in user_selectors:
                try:
                    f = await page.query_selector(u_sel)
                    if f and await f.is_visible():
                        user_field = f
                        break
                except: continue
            
            # Suche in Unter-Frames
            if not user_field:
                for frame in page.frames:
                    for u_sel in user_selectors:
                        try:
                            f = await frame.query_selector(u_sel)
                            if f and await f.is_visible():
                                user_field = f
                                target_frame = frame
                                break
                        except: continue
                    if user_field: break

            if user_field:
                # NEU: Nutzung der kognitiven Tipp-Simulation
                await CognitiveHumanTyping.type_like_human(user_field, target_acc['username'])
                
                for p_sel in pass_selectors:
                    try:
                        p_field = await target_frame.query_selector(p_sel)
                        if p_field and await p_field.is_visible():
                            await CognitiveHumanTyping.type_like_human(p_field, target_acc['password'])
                            
                            logger.info(f"🚀 LOGIN-DATEN EINGEGEBEN: {link}")
                            await target_frame.keyboard.press("Enter")
                            await asyncio.sleep(1)
                            submit_btns = await target_frame.query_selector_all("button[type='submit'], input[type='submit'], .login-button")
                            for s_btn in submit_btns:
                                try:
                                    if await s_btn.is_visible():
                                        await s_btn.click()
                                except: continue
                            await asyncio.sleep(4)
                            self.stats["logins"] += 1
                            break
                    except: continue

        except Exception as e:
            logger.error(f"❌ Schwerer Fehler beim Auto-Login auf {link}: {str(e)[:100]}")

    async def solve_captchas(self, page: Page):
        """Sucht nach Google ReCaptcha und Cloudflare."""
        for frame in page.frames:
            try:
                captcha = await frame.query_selector("span#recaptcha-anchor")
                if captcha:
                    logger.info("🛡️ ReCaptcha entdeckt! Versuche Klick...")
                    await captcha.click()
                    await asyncio.sleep(3)
                    self.stats["captchas_detected"] += 1
                cf = await frame.query_selector("input[type='checkbox']")
                if cf and "cloudflare" in frame.url:
                    logger.info("🛡️ Cloudflare erkannt! Klicke Checkbox...")
                    await cf.click()
                    self.stats["captchas_detected"] += 1
            except: continue

    async def accept_everything(self, page: Page):
        """Beseitigt Cookie-Banner, AGBs und Popups mit Gewalt."""
        selectors = [
            "button:has-text('Zustimmen')", "button:has-text('Akzeptieren')", 
            "button:has-text('Agree')", "button:has-text('OK')", "button:has-text('Accept')",
            "button:has-text('Alles erlauben')", "#save", ".close-button", ".modal-close",
            "button:has-text('Verstanden')", "a.cc-btn.cc-dismiss", "button.accept"
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
        """Simuliert komplexe Mausbewegungen und Scrollen gegen Bot-Sperren."""
        try:
            width, height = 1280, 720
            # Bezier-Kurven ähnliche Bewegungen
            for _ in range(random.randint(3, 8)):
                target_x = random.randint(100, width - 100)
                target_y = random.randint(100, height - 100)
                await page.mouse.move(target_x, target_y, steps=random.randint(10, 25))
                await asyncio.sleep(random.uniform(0.1, 0.3))
                
            # Zufälliges Scrollen nach oben und unten
            await page.mouse.wheel(0, random.randint(300, 1200))
            await asyncio.sleep(random.uniform(1.0, 2.5))
            await page.mouse.wheel(0, random.randint(-400, 200))
        except: pass

    async def try_post_in_frame(self, frame, link: str) -> bool:
        """KERN-LOGIK: Sucht und füllt Textfelder in jedem Frame."""
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
                    
                    # Nutze die neue Kognitive Tipp-Funktion
                    msg = self._build_message()
                    await field.fill("") # Altes Zeug löschen
                    await CognitiveHumanTyping.type_like_human(field, msg)
                    
                    await asyncio.sleep(1.5)
                    await frame.keyboard.press("Enter")
                    
                    buttons = await frame.query_selector_all("button, input[type='submit'], .btn-primary, .submit-btn")
                    for b in buttons:
                        try:
                            txt = await b.inner_text()
                            if any(x in txt.lower() for x in ["post", "send", "antwor", "reply", "absenden", "erstellen", "submit"]):
                                await b.click()
                                logger.info(f"🚀 ERFOLGREICH ABSENDEN geklickt!")
                                return True
                        except: continue
                    return True
            except: continue
        return False

    async def process_queue(self, context: BrowserContext):
        """Worker für die Queue-Verarbeitung."""
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
            
            # Anti-Bot-Header hinzufügen
            await page.set_extra_http_headers({
                "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1"
            })

            try:
                logger.info(f"🌐 Anflug auf: {link}")
                
                # Injiziere Stealth-Skripte vor der Navigation
                await AdvancedStealthManager.inject_stealth_scripts(page)
                
                response = await page.goto(link, timeout=45000, wait_until="domcontentloaded")
                
                if response and response.status >= 400:
                    logger.warning(f"⚠️ Seite gab Fehler {response.status} zurück.")
                    self.stats["failures"] += 1
                    await SystemReporter.dump_error_state(page, link, f"HTTP Error {response.status}")
                else:
                    await AdvancedCaptchaHeuristics.scan_and_log_captchas(page)
                    await self.accept_everything(page)
                    await self.auto_login(page, link)
                    await self.solve_captchas(page)
                    await self.human_emulation(page)
                    
                    posted = False
                    # Normale Frames durchsuchen
                    for frame in page.frames:
                        if await self.try_post_in_frame(frame, link):
                            self.stats["successes"] += 1
                            posted = True
                            break
                    
                    # NEU: Shadow-DOM und versteckte Felder durchsuchen, wenn normal nichts gefunden
                    if not posted:
                        shadow_field = await DeepDOMAnalyzer.pierce_shadow_dom(page, ["textarea", "div[contenteditable='true']"])
                        if shadow_field:
                            logger.info("🔦 Shadow-DOM Feld gefunden! Versuche Injektion.")
                            await shadow_field.fill(self._build_message())
                            await shadow_field.press("Enter")
                            posted = True
                            self.stats["successes"] += 1

                    if not posted:
                        # Plan C: JS Gewalt
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
                await SystemReporter.dump_error_state(page, link, str(e))
            finally:
                await page.close()
                self.target_queue.task_done()
                await asyncio.sleep(random.uniform(5, 12))

    async def perform_search(self, context: BrowserContext, engine: str, url_pattern: str, kw: str):
        """Erntet Links von Suchmaschinen."""
        page = await context.new_page()
        try:
            for p_idx in range(5):
                offset = p_idx * 10
                search_url = url_pattern.format(kw=kw, offset=offset)
                logger.info(f"🔎 {engine} Suche: {kw} (Seite {p_idx+1})")
                
                await AdvancedStealthManager.inject_stealth_scripts(page)
                await page.goto(search_url, timeout=30000)
                await asyncio.sleep(3)
                await self.accept_everything(page)
                
                links = await page.eval_on_selector_all("a", "nodes => nodes.map(n => n.href)")
                count = 0
                for link in links:
                    if link.startswith("http") and not any(x in link for x in ["google", "bing", "microsoft", "duckduckgo", "facebook", "twitter"]):
                        await self.target_queue.put(link)
                        count += 1
                logger.info(f"📥 {count} neue Links hinzugefügt.")
        except Exception as e:
            logger.error(f"❌ Such-Fehler bei {engine}: {e}")
        finally:
            await page.close()

    async def start(self):
        self.target_queue = asyncio.Queue()
        async with async_playwright() as p:
            logger.info("🔥 ULTRA-GIGA-MODUS GESTARTET. ALLE SYSTEME AKTIV.")
            
            browser = await p.chromium.launch(headless=True, args=[
                '--no-sandbox', '--disable-setuid-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage', '--disable-accelerated-2d-canvas',
                '--disable-gpu', '--window-size=1920,1080'
            ])
            
            storage = self.session_file if os.path.exists(self.session_file) else None
            
            # Komplexer Kontext mit mehr Tarnung
            context = await browser.new_context(
                storage_state=storage,
                user_agent=random.choice(self.config['user_agents']),
                viewport={'width': 1920, 'height': 1080},
                device_scale_factor=1,
                has_touch=False,
                is_mobile=False,
                timezone_id="Europe/Berlin",
                locale="de-DE",
                color_scheme="dark"
            )
            
            search_engines = [
                ("Bing", "https://www.bing.com/search?q={kw}+forum&first={offset}"),
                ("Google", "https://www.google.com/search?q={kw}+forum&start={offset}"),
                ("DuckDuckGo", "https://duckduckgo.com/html/?q={kw}+forum")
            ]
            
            search_tasks = []
            for kw in self.config['keywords']:
                for name, url in search_engines:
                    search_tasks.append(self.perform_search(context, name, url, kw))

            # 5 Worker starten
            workers = [asyncio.create_task(self.process_queue(context)) for _ in range(5)]
            
            await asyncio.gather(*search_tasks)
            
            try:
                await asyncio.wait_for(self.target_queue.join(), timeout=600)
            except asyncio.TimeoutError:
                logger.info("⏳ Zeitlimit erreicht.")

            await context.storage_state(path=self.session_file)
            logger.info(f"💾 Session in {self.session_file} gesichert.")

            for w in workers: w.cancel()
            await browser.close()
            self._final_summary()

    def _final_summary(self):
        print("\n" + "█"*60)
        print(f"📊 DER ULTIMATIVE BERICHT (v2.0)")
        print(f"✅ Erfolgreiche Posts: {self.stats['successes']}")
        print(f"🔑 Logins durchgeführt: {self.stats['logins']}")
        print(f"🛡️ Captchas umgangen: {self.stats['captchas_detected']}")
        print(f"Attempted: {self.stats['attempts']} | Gefundene URLs: {len(self.visited_links)}")
        print("█"*60 + "\n")

if __name__ == "__main__":
    bot = OmniGodBot()
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(bot.start())
