import json
import random
import asyncio
from playwright.async_api import async_playwright

async def run_super_bot():
    # 1. Deine bot_config.json laden
    with open('bot_config.json', 'r') as f:
        config = json.load(f)

    async with async_playwright() as p:
        # Browser starten
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = await browser.new_context(
            user_agent=random.choice(config['user_agents'])
        )
        page = await context.new_page()

        # Zufälliges Keyword für die Suche wählen
        keyword = random.choice(config['keywords'])
        print(f"🚀 Bot sucht nach: {keyword}")

        # Suche auf Bing starten
        await page.goto(f"https://www.bing.com/search?q={keyword}+forum+diskussion")
        await page.wait_for_timeout(2000)

        # Links von der Suchseite einsammeln
        links = await page.eval_on_selector_all("li.b_algo h2 a", "nodes => nodes.map(n => n.href)")

        for link in links[:5]: # Besucht die ersten 5 gefundenen Seiten
            try:
                print(f"🌐 Besuche Seite: {link}")
                await page.goto(link, timeout=30000)
                
                # Wir überspringen jetzt die Analyse und suchen sofort das Feld
                print(f"🔍 Suche Kommentarfeld auf {link}...")
                
                # Sucht nach Feldern für Kommentare oder Nachrichten
                selectors = ["textarea", "input[type='text']", "[contenteditable='true']"]
                
                found_field = False
                for selector in selectors:
                    if await page.query_selector(selector):
                        message = random.choice(config['messages'])
                        await page.fill(selector, message)
                        print(f"✅ Nachricht eingetippt auf {link}")
                        found_field = True
                        # Hier könnte man den Senden-Befehl ergänzen
                        break
                
                if not found_field:
                    print(f"❌ Kein passendes Feld auf {link} gefunden.")

            except Exception as e:
                print(f"⚠️ Seite blockiert oder Fehler bei {link}")

        await browser.close()
        print("✅ Runde beendet.")

if __name__ == "__main__":
    asyncio.run(run_super_bot())
