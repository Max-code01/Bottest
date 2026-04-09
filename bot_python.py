import json
import random
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def analyze_page(html, keywords):
    """Das 'Gehirn': Prüft, ob die Seite relevant ist."""
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text().lower()
    # Zählt, wie oft deine Keywords auf der Seite vorkommen
    score = sum(text.count(key.lower()) for key in keywords)
    return score

async def run_super_bot():
    with open('bot_config.json', 'r') as f:
        config = json.load(f) #

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = await browser.new_context(user_agent=random.choice(config['user_agents'])) #
        page = await context.new_page()

        keyword = random.choice(config['keywords']) #
        print(f"🚀 Super-Bot sucht nach: {keyword}")

        await page.goto(f"https://www.bing.com/search?q={keyword}+forum+diskussion")
        await page.wait_for_timeout(2000)

        links = await page.eval_on_selector_all("li.b_algo h2 a", "nodes => nodes.map(n => n.href)")

        for link in links[:3]:
            try:
                print(f"🧐 Analysiere Seite: {link}")
                await page.goto(link, timeout=30000)
                content = await page.content()
                
                # 'Lern'-Phase: Ist das eine gute Seite?
                relevance = await analyze_page(content, config['keywords']) #
                
                if relevance > 2:
                    print(f"🔥 Hohe Relevanz (Score: {relevance})! Suche Kommentarfeld...")
                    
                    # Sucht nach Feldern für Kommentare, Nachrichten oder Antworten
                    selectors = ["textarea", "input[type='text']", "[contenteditable='true']"]
                    for selector in selectors:
                        if await page.query_selector(selector):
                            message = random.choice(config['messages']) #
                            await page.fill(selector, message)
                            print(f"✅ Nachricht platziert auf {link}")
                            # Hier könnte man jetzt auf 'Senden' klicken
                            break
                else:
                    print(f"😴 Seite nicht relevant genug (Score: {relevance}). Überspringe...")

            except Exception as e:
                print(f"⚠️ Seite blockiert oder Fehler.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_super_bot())
