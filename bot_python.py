import json
import random
import asyncio
from playwright.async_api import async_playwright

async def run_super_bot():
    # 1. Deine bot_config.json laden
    with open('bot_config.json', 'r') as f:
        config = json.load(f)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = await browser.new_context(
            user_agent=random.choice(config['user_agents']) #
        )
        page = await context.new_page()

        # Zufälliges Keyword wählen
        keyword = random.choice(config['keywords']) #
        print(f"🚀 Bot sucht nach: {keyword}")

        await page.goto(f"https://www.bing.com/search?q={keyword}+forum+diskussion")
        await page.wait_for_timeout(3000)

        # Links sammeln
        links = await page.eval_on_selector_all("li.b_algo h2 a", "nodes => nodes.map(n => n.href)")

        for link in links[:5]:
            try:
                print(f"🌐 Besuche Seite: {link}")
                await page.goto(link, timeout=30000, wait_until="networkidle")
                
                # 1. Nachricht eintippen
                selectors = ["textarea", "input[type='text']", "[contenteditable='true']"]
                found_field = False
                
                for selector in selectors:
                    field = await page.query_selector(selector)
                    if field and await field.is_visible():
                        message = random.choice(config['messages']) #
                        await field.fill(message)
                        print(f"✅ Nachricht eingetippt auf {link}")
                        found_field = True
                        break
                
                # 2. Senden-Button suchen und klicken
                if found_field:
                    await page.wait_for_timeout(1000) # Kurz warten für Realismus
                    # Sucht nach typischen Buttons wie "Senden", "Post", "Antworten"
                    buttons = await page.query_selector_all("button, input[type='submit']")
                    for btn in buttons:
                        text = await btn.inner_text()
                        if any(x in text.lower() for x in ["senden", "post", "antwort", "submit", "reply", "veröffentlichen"]):
                            await btn.click()
                            print(f"🚀 ABSENDEN geklickt auf {link}!")
                            await page.wait_for_timeout(2000)
                            break
                else:
                    print(f"❌ Kein Feld auf {link}")

            except Exception as e:
                print(f"⚠️ Fehler oder Blockade bei {link}")

        await browser.close()
        print("✅ Alle Ziele abgearbeitet.")

if __name__ == "__main__":
    asyncio.run(run_super_bot())
