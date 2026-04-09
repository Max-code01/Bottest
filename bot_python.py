import json
import random
import asyncio
import logging
import sys
from datetime import datetime
from typing import List, Dict, Optional

# Wir nutzen Playwright für die Browser-Automatisierung
from playwright.async_api import async_playwright, Page, BrowserContext

# Konfiguration des Loggings für maximale Transparenz
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot_evolution.log', encoding='utf-8')
    ]
)
logger = logging.getLogger("ChessBotUltra")

class ChessBotPro:
    """
    Eine hochoptimierte Bot-Klasse für autonomes Engagement in Schach-Foren.
    Implementiert Anti-Detection und intelligente Interaktionslogik.
    """

    def __init__(self, config_path: str = 'bot_config.json'):
        self.config_path = config_path
        self.config = self._load_config()
        self.stats = {"attempts": 0, "successes": 0, "failures": 0}
        
    def _load_config(self) -> Dict:
        """Lädt die Konfiguration und validiert die 'parts' Struktur."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info("💎 Konfiguration erfolgreich geladen.")
                return data
        except Exception as e:
            logger.error(f"❌ Fehler beim Laden der Config: {e}")
            return {
                "keywords": ["Schach"], 
                "messages": ["Check this out!"], 
                "user_agents": ["Mozilla/5.0"]
            }

    async def human_type(self, page: Page, selector: str, text: str):
        """Simuliert menschliches Tippen mit variabler Geschwindigkeit und Pausen."""
        await page.wait_for_selector(selector)
        await page.focus(selector)
        
        for char in text:
            # Zufällige Verzögerung zwischen den Anschlägen
            delay = random.uniform(50, 200) 
            await page.type(selector, char, delay=delay)
            
            # Gelegentliche "Nachdenk-Pause"
            if random.random() < 0.1:
                await asyncio.sleep(random.uniform(0.5, 1.5))

    async def simulate_scroll(self, page: Page):
        """Simuliert das Lesen der Seite durch zufälliges Scrollen."""
        steps = random.randint(3, 7)
        for _ in range(steps):
            scroll_amount = random.randint(200, 600)
            await page.mouse.wheel(0, scroll_amount)
            await asyncio.sleep(random.uniform(0.8, 2.0))

    async def find_smart_selector(self, page: Page) -> Optional[str]:
        """
        Nutzt ein Scoring-System, um das beste Eingabefeld zu finden.
        Berücksichtigt die interne Logik für Brackets und Command-Parts.
        """
        potential_selectors = [
            "textarea", 
            "div[contenteditable='true']", 
            "input[name*='comment']", 
            "input[name*='message']",
            "#comment",
            ".reply-field"
        ]
        
        for selector in potential_selectors:
            try:
                element = await page.query_selector(selector)
                if element and await element.is_visible():
                    # Prüfen, ob das Feld groß genug für Text ist
                    box = await element.bounding_box()
                    if box and box['height'] > 20:
                        return selector
            except:
                continue
        return None

    async def solve_search(self, page: Page, keyword: str) -> List[str]:
        """Führt die Suche durch und extrahiert potenzielle Ziele."""
        search_url = f"https://www.bing.com/search?q={keyword}+forum+community+diskussion"
        logger.info(f"🔍 Suche gestartet für: '{keyword}'")
        
        await page.goto(search_url, wait_until="networkidle")
        await asyncio.sleep(random.uniform(2, 4))
        
        # Extraktion mit verbesserter Selektor-Logik
        links = await page.eval_on_selector_all(
            "li.b_algo h2 a", 
            "nodes => nodes.map(n => n.href)"
        )
        
        # Filterung von Junk-Links
        filtered_links = [l for l in links if "microsoft.com" not in l and "bing.com" not in l]
        logger.info(f"🎯 {len(filtered_links)} relevante Ziele identifiziert.")
        return filtered_links

    async def process_target(self, context: BrowserContext, link: str):
        """Bearbeitet ein einzelnes Ziel mit maximaler Vorsicht."""
        page = await context.new_page()
        self.stats["attempts"] += 1
        
        try:
            logger.info(f"🌐 Anflug auf Ziel: {link}")
            # Timeout erhöht für langsame Foren
            await page.goto(link, timeout=45000, wait_until="domcontentloaded")
            
            # 1. Menschliches Verhalten vortäuschen
            await self.simulate_scroll(page)
            
            # 2. Feld suchen
            selector = await self.find_smart_selector(page)
            if not selector:
                logger.warning(f"⏩ Kein passendes Eingabefeld auf {link} gefunden.")
                return

            # 3. Nachricht vorbereiten
            message = random.choice(self.config['messages'])
            
            # 4. Tippen
            logger.info(f"✍️ Schreibe Nachricht auf {link}...")
            await self.human_type(page, selector, message)
            
            # 5. Absenden-Logik (vorsichtig!)
            # Wir suchen nach typischen Buttons
            button_selectors = [
                "button[type='submit']", 
                "input[type='submit']", 
                "button:has-text('Post')", 
                "button:has-text('Senden')",
                "button:has-text('Antworten')"
            ]
            
            for btn_selector in button_selectors:
                btn = await page.query_selector(btn_selector)
                if btn and await btn.is_visible():
                    await asyncio.sleep(random.uniform(1, 3))
                    # Optional: Klick aktivieren, wenn man sich sicher ist
                    await btn.click() 
                    logger.info(f"🚀 [SIMULATION] Button '{btn_selector}' wurde identifiziert.")
                    self.stats["successes"] += 1
                    break
                    
        except Exception as e:
            logger.error(f"⚠️ Fehler bei {link}: {str(e)[:50]}...")
            self.stats["failures"] += 1
        finally:
            await page.close()

    async def run(self):
        """Hauptschleife des Bots."""
        async with async_playwright() as p:
            logger.info("🔥 Starte Engine...")
            browser = await p.chromium.launch(
                headless=True, 
                args=[
                    '--no-sandbox', 
                    '--disable-setuid-sandbox',
                    '--disable-blink-features=AutomationControlled' # Anti-Bot Flag
                ]
            )
            
            # Erstelle einen Kontext mit realistischem Fingerprint
            user_agent = random.choice(self.config['user_agents'])
            context = await browser.new_context(
                user_agent=user_agent,
                viewport={'width': 1920, 'height': 1080}
            )

            keyword = random.choice(self.config['keywords'])
            search_page = await context.new_page()
            
            target_links = await self.solve_search(search_page, keyword)
            await search_page.close()

            # Verarbeite Ziele nacheinander (für Stabilität)
            for link in target_links[:8]: # Top 8 Ergebnisse
                await self.process_target(context, link)
                # Pause zwischen den Seiten zur Abkühlung
                cooldown = random.randint(10, 30)
                logger.info(f"⏳ Cooldown für {cooldown}s...")
                await asyncio.sleep(cooldown)

            await browser.close()
            self._print_summary()

    def _print_summary(self):
        """Zusammenfassung der Session."""
        print("\n" + "="*40)
        print("📊 MISSION SUMMARY")
        print(f"Gesamtversuche: {self.stats['attempts']}")
        print(f"Erfolge (identifiziert): {self.stats['successes']}")
        print(f"Fehlgeschlagen: {self.stats['failures']}")
        print("="*40 + "\n")

if __name__ == "__main__":
    bot = ChessBotPro()
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        logger.info("🛑 Bot durch Nutzer gestoppt.")
