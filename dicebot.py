# dicebot.py – Ein einfacher Discord-Würfelbot
# ------------------------------------------------
# Dieser Bot reagiert auf den Befehl `!roll` (Alias: `!würfeln`) und erwartet
# als Argument die Notation "<Anzahl>W<Seiten>", z.B. 2W6 oder 1W20.
# Er gibt die einzelnen Würfelwerte und ihre Summe zurück.
# ------------------------------------------------
# Installation:
# 1. Python 3.10+ installieren
# 2. Abhängigkeiten:  
#    pip install discord.py python-dotenv
# 3. .env-Datei anlegen und darin DISCORD_TOKEN=<Dein Bot-Token> setzen
# 4. Bot bei Discord registrieren, Token kopieren, Bot mit passenden Rechten
#    (Send Messages, Read Messages, Message Content Intent) auf den Server einladen.
# 5. Bot starten:  
#    python dicebot.py

import os
import random
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Lade Umgebungsvariablen
auth_env = load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # Bot-Token aus der .env-Datei

# Aktiviere Message Content Intent, damit der Bot Befehlsargumente lesen darf
intents = discord.Intents.default()
intents.message_content = True

# Befehlspräfix festlegen (hier "!")
bot = commands.Bot(command_prefix="!", intents=intents)

# Regulärer Ausdruck für die Würfel-Notation, z.B. 2W6 oder 1w20
DICE_PATTERN = re.compile(r"^(\d+)[wW](\d+)$")


@bot.event
async def on_ready():
    """Wird aufgerufen, sobald der Bot sich erfolgreich eingeloggt hat."""
    print(f"Eingeloggt als {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.command(name="roll", aliases=["würfeln"])
async def roll(ctx: commands.Context, dice: str):
    """Rollt Würfel in <Anzahl>W<Seiten>-Notation, z.B. !roll 3W6"""

    # Eingabevalidierung
    match = DICE_PATTERN.fullmatch(dice)
    if not match:
        await ctx.send("Ungültiges Format. Benutze z.B. `!roll 2W6`.")
        return

    num_dice, sides = map(int, match.groups())

    if num_dice <= 0 or sides <= 0:
        await ctx.send("Anzahl der Würfel und Seiten muss positiv sein.")
        return
    if num_dice > 100:
        await ctx.send("Bitte nicht mehr als 100 Würfel gleichzeitig werfen.")
        return

    # Würfeln
    rolls = [random.randint(1, sides) for _ in range(num_dice)]
    total = sum(rolls)

    # Antwort zusammenbauen
    rolls_str = ", ".join(map(str, rolls))
    await ctx.send(f"🎲 Ergebnis für {num_dice}W{sides}: {rolls_str} (Summe: **{total}**)")


if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError(
            "DISCORD_TOKEN nicht gefunden. Lege eine .env an oder ersetze die Zeile mit deinem Token."
        )
    bot.run(TOKEN)
