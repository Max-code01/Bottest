import json
import random
import asyncio
import logging
import sys
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Page, BrowserContext

# === LOGGING FÜR MAXIMALE TRANSPARENZ ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ULTRA_BOT_OMEGA")

class ExtremeBotOmega:
    def __init__(self, config_path: str = 'bot_config.json'):
        self.config_path = config_path
        self.config = self._load_config()
        self.stats = {"attempts": 0, "successes": 0, "failures": 0}
        self.visited_links = set()

    def _load_config(self) -> Dict:
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "keywords": ["Schach"], 
                "messages": ["Check this out!"], 
                "user_agents": ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0"]
            }

    async def human_type(self, page: Page, selector: str, text: str):
        """Simuliert menschliche Eingaben mit variabler Geschwindigkeit."""
        await page.wait_for_selector(selector, timeout=10000)
        await page.focus(selector)
        for char in text:
            await page.type(selector, char, delay=random.uniform(20, 80))
        if random.random() > 0.5:
            await asyncio.sleep(random.uniform(0.5, 1.5))

    async def _extract_links(self, page: Page, selectors: List[str]) -> List[str]:
        """Extrahiert alle Links basierend auf einer Liste von Selektor-Parts."""
        all_found = []
        for selector in selectors:
            try:
                found = await page.eval_on_selector_all(
                    selector, 
                    "nodes => nodes.map(n => n.href)"
                )
                all_found.extend(found)
            except:
                continue
        return [l for l in all_found if l and l.startswith("http")]

    async def solve_search(self, page: Page, keyword: str) -> List[str]:
        """Dreistufige Such-Kaskade: Bing -> Google -> DuckDuckGo."""
        engines = [
            {
                "name": "Bing",
                "url": "https://www.bing.com/search?q={kw}+forum+diskussion&first={offset}",
                "selectors": ["li.b_algo h2 a", "h2 a"],
                "cookie_btn": "button#bnp_btn_accept"
            },
            {
                "name": "Google",
                "url": "https://www.google.com/search?q={kw}+forum+diskussion&start={offset}",
                "selectors": ["div.g a", "h3", "a h3"],
                "cookie_btn": "button:has-text('Alle akzeptieren')"
            },
            {
                "name": "DuckDuckGo",
                "url": "https://duckduckgo.com/html/?q={kw}+forum+diskussion",
                "selectors": ["a.result__a", "h2 a", "a"],
                "cookie_btn": None
            }
        ]

        final_links = []
        for engine in engines:
            logger.info(f"🚀 Versuche Engine: {engine['name']}...")
            for page_idx in range(3):  # Jeweils 3 Seiten tief
                offset = page_idx * 10
                target_url = engine['url'].format(kw=keyword, offset=offset)
                
                try:
                    await page.goto(target_url, wait_until="networkidle", timeout=60000)
                    if engine['cookie_btn']:
                        try:
                            await page.click(engine['cookie_btn'], timeout=3000)
                        except: pass
                    
                    await page.wait_for_timeout(2000)
                    links = await self._extract_links(page, engine['selectors'])
                    
                    if links:
                        # FILTER ENTFERNT: Jede URL wird genommen
                        final_links.extend(links)
                        logger.info(f"✅ {len(links)} Links von {engine['name']} (Seite {page_idx+1}) extrahiert.")
                except Exception as e:
                    logger.warning(f"⚠️ Fehler bei {engine['name']}: {str(e)[:50]}")
                    break
            
            if final_links:
                break # Wenn eine Engine geliefert hat, springen wir zur Verarbeitung
        
        return list(set(final_links))

    async def process_target(self, context: BrowserContext, link: str):
        """Bearbeitet ein Ziel mit optimierter Feldsuche."""
        if link in self.visited_links: return
        self.visited_links.add(link)
        
        page = await context.new_page()
        self.stats["attempts"] += 1
        
        try:
            logger.info(f"🌐 Navigiere zu: {link}")
            await page.goto(link, timeout=45000, wait_until="domcontentloaded")
            
            # Dynamische Feldsuche (Parts-Logik)
            field_parts = [
                "textarea", "div[contenteditable='true']", 
                "input[name*='message']", "input[name*='comment']",
                "#comment", ".reply-field", ".editor", "input[type='text']"
            ]
            
            target_selector = None
            for part in field_parts:
                try:
                    element = await page.query_selector(part)
                    if element and await element.is_visible():
                        target_selector = part
                        break
                except: continue

            if target_selector:
                message = random.choice(self.config['messages'])
                await self.human_type(page, target_selector, message)
                
                # Senden-Logik
                submit_selectors = ["button[type='submit']", "input[type='submit']", "button:has-text('Post')"]
                for sub in submit_selectors:
                    btn = await page.query_selector(sub)
                    if btn and await btn.is_visible():
                        await btn.click()
                        logger.info(f"🚀 ERFOLGREICH GEPOSCHT: {link}")
                        self.stats["successes"] += 1
                        return
            else:
                self.stats["failures"] += 1
                
        except Exception as e:
            logger.debug(f"⏩ Seite übersprungen: {link}")
        finally:
            await page.close()

    async def run(self):
        async with async_playwright() as p:
            logger.info("🔥 STARTING OMEGA ENGINE...")
            # Headless=False ermöglicht das manuelle Eingreifen bei Captchas
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
            
            context = await browser.new_context(
                user_agent=random.choice(self.config['user_agents']),
                viewport={'width': 1920, 'height': 1080}
            )

            for kw in self.config['keywords']:
                search_page = await context.new_page()
                targets = await self.solve_search(search_page, kw)
                await search_page.close()

                # Alle gefundenen Ziele abarbeiten
                for target in targets:
                    await self.process_target(context, target)
                    await asyncio.sleep(random.uniform(5, 15))

            await browser.close()
            self._print_summary()

    def _print_summary(self):
        print("\n" + "="*50)
        print("📊 OMEGA SESSION COMPLETED")
        print(f"Gesamtziele gefunden: {len(self.visited_links)}")
        print(f"Erfolgreiche Interaktionen: {self.stats['successes']}")
        print(f"Fehlversuche: {self.stats['failures']}")
        print("="*50 + "\n")

if __name__ == "__main__":
    bot = ExtremeBotOmega()
    asyncio.run(bot.run())
