const puppeteer = require('puppeteer');
const config = require('./bot_config.json');

async function runAutomatik() {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    
    // 1. Zufälligen Text und User-Agent wählen
    const message = config.messages[Math.floor(Math.random() * config.messages.length)];
    await page.setUserAgent(config.user_agents[Math.floor(Math.random() * config.user_agents.length)]);

    console.log("🤖 Suche nach neuen Webseiten...");
    // Beispiel: Suche auf Bing (da Google Bots oft blockt)
    await page.goto('https://www.bing.com/search?q=chess+forum+new+posts');

    // Hier würde der Bot jetzt die Links sammeln und nacheinander abklappern
    // Das ist der Teil, wo er auf die "Senden"-Buttons der Foren klickt.
    
    console.log(`📝 Würde jetzt posten: "${message}"`);

    await browser.close();
    console.log("✅ Automatik-Runde beendet.");
}

runAutomatik();
