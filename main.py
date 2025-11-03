from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv
from ai import chat

# Load environment variables from .env file
load_dotenv()

app_token = os.getenv("APP_TOKEN")
bot_token = os.getenv("BOT_TOKEN")
app = App(token=bot_token)

@app.event("app_mention")
def handle_app_mention_events(event, client, say):
    client.reactions_add(
        channel=event["channel"],
        timestamp=event["ts"],
        name="eyes",
    )

    response = chat(event["text"])
    client.chat_postMessage(
        channel=event["channel"],
        thread_ts=event["ts"],
        timestamp=event["ts"],
        text=response,
    )
    client.reactions_remove(
        channel=event["channel"],
        timestamp=event["ts"],
        name="eyes",
    )

handler = SocketModeHandler(app, app_token)
handler.start()
    