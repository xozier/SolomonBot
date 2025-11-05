# Solomon Bot

A Slack bot that summarizes conversations when mentioned. When added to a channel and mentioned, the bot reads all messages in the channel and provides a summary of what each person said.

## Features

- **Automatic Conversation Summarization**: When mentioned with `@Solomon`, the bot reads all messages in the channel and summarizes what each participant contributed
- **Smart Filtering**: Automatically filters out bot messages and system messages
- **User-Friendly**: Uses OpenAI's GPT-4o to generate clear, concise summaries
- **Threaded Replies**: Responds in a thread to keep the channel clean

## Prerequisites

- Python 3.7 or higher


## Local Setup

### 1. Clone or Download the Repository

https://github.com/xozier/SolomonBot.git

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Environment File

Create a `.env` file in the project root:

```bash
touch .env
```

Add your tokens to the `.env` file:

```env
APP_TOKEN=xapp-your-app-token-here
BOT_TOKEN=xoxb-your-bot-token-here
OPENAI_API_KEY=sk-your-openai-api-key-here
```
### 5. Run the app
```bash
python3 main.py
```

## Usage

1. **Add the bot to a channel**: Use `/invite @Solomon` in any channel
2. **Have a conversation**: Make sure there are some messages in the channel
3. **Mention the bot**: Type `@Solomon` or `@Solomon summarize the conversation`
4. **Get the summary**: The bot will read all messages and reply with a summary of what each person said



## Dependencies

- `slack-bolt`: Slack SDK for Python
- `python-dotenv`: Load environment variables from .env file
- `openai`: OpenAI API client


