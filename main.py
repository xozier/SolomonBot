from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
import re
from dotenv import load_dotenv
from ai import chat, summarize_conversation
from collections import defaultdict

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

    try:
        # Get bot's own user ID to filter out its messages
        bot_info = client.auth_test()
        bot_user_id = bot_info["user_id"] if bot_info["ok"] else None
        
        # Fetch conversation history from the channel
        channel_id = event["channel"]
        result = client.conversations_history(channel=channel_id)
        
        if not result["ok"]:
            response = f"Sorry, I couldn't access the conversation history. Error: {result.get('error', 'Unknown error')}"
        else:
            messages = result["messages"]
            print(f"\nDEBUG: Retrieved {len(messages)} total messages from channel")
            
            # Filter out bot messages, system messages, and the bot's own messages
            user_messages = []
            user_ids = set()
            
            for msg in messages:
                # Skip bot messages and messages without text
                if "bot_id" in msg or "subtype" in msg:
                    continue
                if "text" not in msg or "user" not in msg:
                    continue
                
                user_id = msg["user"]
                
                # Skip the bot's own messages
                if bot_user_id and user_id == bot_user_id:
                    continue
                
                text = msg["text"]
                
                # Clean up @mentions from the text (remove <@USERID> patterns)
                text = re.sub(r'<@[A-Z0-9]+>', '', text).strip()
                
                # Skip empty messages after cleaning
                if not text:
                    continue
                
                user_messages.append((user_id, text))
                user_ids.add(user_id)
            
            print(f"DEBUG: After filtering, found {len(user_messages)} user messages from {len(user_ids)} unique users")
            if user_messages:
                print("DEBUG: Sample messages:")
                for i, (uid, msg) in enumerate(user_messages[:3]):  # Show first 3
                    print(f"  [{i+1}] User {uid}: {msg[:100]}...")
            
            if not user_messages:
                response = "No user messages found in this conversation. Make sure there are messages in the channel before mentioning me."
            else:
                # Get user names
                user_names = {}
                for user_id in user_ids:
                    try:
                        user_info = client.users_info(user=user_id)
                        if user_info["ok"]:
                            user_names[user_id] = user_info["user"].get("real_name") or user_info["user"].get("name", user_id)
                    except:
                        user_names[user_id] = user_id
                
                # Group messages by user
                messages_by_user = defaultdict(list)
                for user_id, text in user_messages:
                    messages_by_user[user_id].append(text)
                
                # Generate summary
                if messages_by_user:
                    response = summarize_conversation(messages_by_user, user_names)
                else:
                    response = "No valid messages found to summarize."
        
    except Exception as e:
        response = f"Sorry, I encountered an error while summarizing the conversation: {str(e)}"
    
    client.chat_postMessage(
        channel=event["channel"],
        thread_ts=event["ts"],
        text=response,
    )
    client.reactions_remove(
        channel=event["channel"],
        timestamp=event["ts"],
        name="eyes",
    )

handler = SocketModeHandler(app, app_token)
handler.start()
    