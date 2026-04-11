import asyncio
import json
import logging
import time
from playwright.async_api import async_playwright

# --- 1. SAUBERES LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [BOT] - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("ChatBot")

# --- 2. BOT KLASSE ---
class InteractiveChatBot:
    def __init__(self):
        self.config = self.load_config()
        self.is_running = True
        self.processed_messages = set() # Merkt sich gelesene PMs, um nicht doppelt zu antworten

    def load_config(self):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error("Konnte config.json nicht finden! Bitte erstellen.")
            exit()

    async def start(self):
        async with async_playwright() as p:
            logger.info("Browser wird gestartet...")
            # headless=False bedeutet, du siehst den Browser. Setze es auf True, wenn er unsichtbar laufen soll.
            browser = await p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled'])
            context = await browser.new_context(viewport={'width': 1280, 'height': 800})
            page = await context.new_page()

            await self.login(page)
            await self.listen_for_pms(page)

            await browser.close()

    async def login(self, page):
        logger.info(f"Verbinde zu Chatroom2000 als '{self.config['bot_name']}'...")
        await page.goto("https://www.chatroom2000.de/", timeout=60000)
        
        # 1. Cookie Banner wegklicken (aus deinem HTML ausgelesen)
        try:
            logger.info("Prüfe auf Cookie-Banner...")
            btn = await page.wait_for_selector("button:has-text('Alle akzeptieren')", timeout=5000)
            if btn: await btn.click()
        except:
            pass

        # 2. Nickname eingeben
        logger.info("Gebe Logindaten ein...")
        await page.fill("input#username", self.config['bot_name'])
        
        # Geschlecht wählen
        gender = self.config.get('gender', 'n')
        await page.click(f"label[for='sex_{gender}']")

        # 3. Warten, ob das Passwort-Feld auftaucht (passiert, wenn der Name registriert ist)
        await asyncio.sleep(2)
        try:
            pw_field = await page.query_selector("input#pw")
            if pw_field and await pw_field.is_visible():
                await page.fill("input#pw", self.config['bot_password'])
                logger.info("Passwort eingegeben.")
        except:
            logger.info("Kein Passwort-Feld gefunden (Gast-Modus).")

        # 4. AGB Checkbox und Login klicken
        await page.check("input#rules")
        await page.click("button.loginbutton")
        
        logger.info("Warte auf das Laden des Chatraums...")
        await asyncio.sleep(10) # Dem Chat Zeit geben, komplett zu laden
        logger.info("Erfolgreich eingeloggt! Bot ist jetzt im Zuhör-Modus.")

    async def listen_for_pms(self, page):
        """Die Hauptschleife, die permanent nach privaten Nachrichten sucht."""
        logger.info("Warte auf private Befehle...")
        
        while self.is_running:
            try:
                # Chatroom2000 markiert private Nachrichten meist mit speziellen Klassen.
                # WICHTIG: Sollten PMs nicht erkannt werden, müssen wir diese Klassen anpassen.
                pm_elements = await page.query_selector_all(".chat-message.private, .msg-text.private, span.whisper")
                
                for pm in pm_elements:
                    # Eindeutige ID der Nachricht finden (verhindert Spam)
                    msg_id = await pm.evaluate("(el) => el.id || el.innerText")
                    
                    if msg_id not in self.processed_messages:
                        self.processed_messages.add(msg_id)
                        text = await pm.inner_text()
                        
                        # Extrahiere Absender und Befehl
                        # Beispiel-Format im Chat: "[Flüstern von UserX]: !hilfe"
                        if self.config['command_prefix'] in text:
                            await self.process_command(page, text)
                            
            except Exception as e:
                logger.debug(f"Fehler beim Scannen der Nachrichten: {e}")
                
            await asyncio.sleep(2) # Alle 2 Sekunden prüfen (schont CPU)

    async def process_command(self, page, raw_text):
        """Erkennt Befehle und antwortet darauf."""
        prefix = self.config['command_prefix']
        
        # Simpler Parser: Wir tun so, als stünde der Absender vor einem Doppelpunkt
        # In der Realität musst du schauen, wie Chatroom2000 Flüstern formatiert.
        try:
            # Versuch den Absender zu finden
            sender = raw_text.split(":")[0].replace("[Flüstern von ", "").replace("]", "").strip()
            command_part = raw_text.split(prefix)[1].strip().lower()
            command = command_part.split(" ")[0] # Das erste Wort nach dem !
        except:
            return

        logger.info(f"Befehl erhalten von {sender}: {prefix}{command}")

        # --- HIER KOMMEN DEINE BEFEHLE REIN ---
        if command == "ping":
            await self.send_pm(page, sender, "Pong! Der Bot ist online und bereit.")
            
        elif command == "zeit":
            jetzt = time.strftime("%H:%M:%S")
            await self.send_pm(page, sender, f"Die aktuelle Serverzeit ist {jetzt} Uhr.")
            
        elif command == "info":
            await self.send_pm(page, sender, "Ich bin ein interaktiver Service-Bot. Verfügbare Befehle: !ping, !zeit, !info")
            
        elif command == "schach":
            await self.send_pm(page, sender, "Du willst Schach spielen? Hier entlang: https://profischach.netlify.app/")

    async def send_pm(self, page, target_user, message):
        """Sendet eine Flüsternachricht zurück an den User."""
        try:
            # Bei Chatroom2000 ist der Befehl zum Flüstern oft "/w [Name] [Text]" oder "/msg [Name] [Text]"
            chat_input = await page.wait_for_selector("input#chat_input, textarea#chat_input", timeout=3000)
            
            if chat_input:
                pm_command = f"/w {target_user} {message}"
                await chat_input.fill(pm_command)
                await page.keyboard.press("Enter")
                logger.info(f"Antwort gesendet an {target_user}")
        except Exception as e:
            logger.error(f"Konnte PM an {target_user} nicht senden: {e}")

if __name__ == "__main__":
    bot = InteractiveChatBot()
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        logger.info("Bot wurde manuell beendet.")
