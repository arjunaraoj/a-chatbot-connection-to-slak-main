import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# ─── 1) Load .env ────────────────────────────────────────────────────────────────
env_path = Path("D:/GenerativeAI/Structured_Unstructured/.env")
if not env_path.is_file():
    print(f"❌ .env not found at {env_path}")
    sys.exit(1)

load_dotenv(dotenv_path=env_path, override=True)

SLACK_BOT_TOKEN      = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
SLACK_APP_TOKEN      = os.getenv("SLACK_APP_TOKEN")  # xapp-… only for Socket Mode

# ─── 2) Validate critical tokens ─────────────────────────────────────────────────
missing = [name for name,val in [
    ("SLACK_BOT_TOKEN", SLACK_BOT_TOKEN),
    ("SLACK_SIGNING_SECRET", SLACK_SIGNING_SECRET),
] if not val]
if missing:
    print(f"❌ Missing env vars: {', '.join(missing)}")
    sys.exit(1)

# Only use Socket Mode if this token *looks* valid (must start with "xapp-")
use_socket_mode = SLACK_APP_TOKEN and SLACK_APP_TOKEN.startswith("xapp-")

# ─── 3) Import your QA function ───────────────────────────────────────────────────
from chat_app import ask_question   # ensure chat_app.py is in the same folder

# ─── 4) Initialize Bolt App ───────────────────────────────────────────────────────
app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

# ─── 5) Respond to mentions ──────────────────────────────────────────────────────
@app.event("app_mention")
def handle_app_mention(event, say):
    text = event.get("text", "").split(maxsplit=1)
    query = text[1].strip() if len(text) > 1 else ""
    if not query:
        say("⚠️ Please ask me something, e.g. `@bot What’s our top product?`")
    else:
        say(ask_question(query))

# ─── 6) Optional /ask command ─────────────────────────────────────────────────────
@app.command("/ask")
def handle_slash(ack, respond, command):
    ack()
    user_query = command.get("text", "").strip()
    if not user_query:
        respond("⚠️ You need to provide a query, e.g. `/ask Show me sales by region.`")
    else:
        respond(ask_question(user_query))

# ─── 7) Start the app ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    if use_socket_mode:
        print("🔌 Starting in Socket Mode…")
        SocketModeHandler(app, SLACK_APP_TOKEN).start()
    else:
        print(f"🌐 Starting in HTTP mode on port {port} (remove SLACK_APP_TOKEN or fix it to enable Socket Mode)")
        app.start(port=port)
