import json
import random
import asyncio
from playwright.async_api import async_playwright

async def run_bot():
    # 1. Deine bestehende bot_config.json laden
    with open('bot_config.json', 'r') as f:
        config = json.load(f)

    async with async_playwright() as p:
        # Browser starten (perfekt für GitHub Actions konfiguriert)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=random.choice(config['user_agents']) #
        )
        page = await context.new_page()

        # Zufälliges Keyword und Nachricht wählen
        keyword = random.choice(config['keywords']) #
        message = random.choice(config['messages']) #

        print(f"🐍 Python-Bot startet Suche nach: {keyword}")

        # 2. Suche auf Bing (wie im JS-Bot)
        await page.goto(f"https://www.bing.com/search?q={keyword}+forum")
        await page.wait_for_timeout(2000)

        # 3. Links einsammeln
        links = await page.eval_on_selector_all("li.b_algo h2 a", "nodes => nodes.map(n => n.href)")
        print(f"🔍 {len(links)} Links gefunden.")

        for link in links[:5]: # Erstmal nur die ersten 5 testen
            try:
                print(f"🌐 Checke Seite: {link}")
                await page.goto(link, timeout=30000)
                
                # Hier können wir später die Login-Logik einbauen
                print(f"✅ Seite geladen. Würde posten: {message}")
            except Exception as e:
                print(f"⚠️ Fehler bei {link}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_bot())
