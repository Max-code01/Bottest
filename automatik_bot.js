const puppeteer = require('puppeteer');
const config = require('./bot_config.json');

async function runAutomatik() {
    // WICHTIG: args für GitHub Actions hinzufügen
    const browser = await puppeteer.launch({ 
        headless: true, 
        args: ['--no-sandbox', '--disable-setuid-sandbox'] 
    });
    const page = await browser.newPage();
    
    // Zufälligen Text und User-Agent wählen
    const message = config.messages[Math.floor(Math.random() * config.messages.length)];
    const keyword = config.keywords[Math.floor(Math.random() * config.keywords.length)];
    await page.setUserAgent(config.user_agents[Math.floor(Math.random() * config.user_agents.length)]);

    console.log(`🤖 Suche nach: ${keyword}`);
    
    // 1. Suche bei Bing starten
    await page.goto(`https://www.bing.com/search?q=${encodeURIComponent(keyword + " forum comment")}`);
    await page.waitForTimeout(2000);

    // 2. Alle Links der Suchergebnisse einsammeln
    const links = await page.evaluate(() => {
        const results = document.querySelectorAll('li.b_algo h2 a');
        return Array.from(results).map(a => a.href);
    });

    console.log(`🔍 ${links.length} potenzielle Seiten gefunden.`);

    // 3. Jede Seite besuchen und versuchen zu posten
    for (let link of links) {
        if (link.includes('bing.com') || link.includes('microsoft.com')) continue;

        try {
            console.log(`🌐 Besuche: ${link}`);
            await page.goto(link, { waitUntil: 'networkidle2', timeout: 30000 });

            // 4. AUTOMATIK-LOGIK: Suche nach einem Kommentarfeld
            // Wir suchen nach typischen Namen wie "comment", "message", "reply"
            const commentBox = await page.$('textarea, input[type="text"]');
            
            if (commentBox) {
                await page.type('textarea, input[type="text"]', message);
                console.log(`✍️ Text eingegeben auf ${link}`);
                
                // Hier könnte man den "Senden"-Button suchen (VORSICHT: Spam-Gefahr)
                // await page.keyboard.press('Enter'); 
            }
        } catch (e) {
            console.log(`⚠️ Konnte ${link} nicht bearbeiten.`);
        }
    }

    await browser.close();
    console.log("✅ Automatik-Runde beendet.");
}

runAutomatik();
