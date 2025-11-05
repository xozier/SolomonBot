from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat(query: str):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": query}],
        model="gpt-4o"
    )
    return chat_completion.choices[0].message.content

def summarize_conversation(messages_by_user: dict, user_names: dict) -> str:
    """
    Summarizes what each person said in the conversation.
    
    Args:
        messages_by_user: Dictionary mapping user IDs to lists of their messages
        user_names: Dictionary mapping user IDs to display names
    
    Returns:
        A formatted summary string
    """
    if not messages_by_user:
        return "No messages found in this conversation."
    
    # Build the conversation text directly
    conversation_text = []
    for user_id, messages in messages_by_user.items():
        user_name = user_names.get(user_id, f"User {user_id}")
        for msg in messages:
            if msg and msg.strip():  # Only add non-empty messages
                conversation_text.append(f"{user_name}: {msg}")
    
    if not conversation_text:
        return "No valid messages found in the conversation to summarize."
    
    # Create a very explicit prompt that makes it clear we're providing the text
    conversation_content = "\n".join(conversation_text)
    
    prompt = f"""I have a conversation transcript below. Please read it and summarize what each person said.

CONVERSATION TRANSCRIPT:
{conversation_content}

Please provide a summary of what each person contributed to this conversation. Format it with each person's name followed by a brief summary of their main points or contributions."""
    
    # Debug: Print what we're sending to the API
    print("=" * 80)
    print("DEBUG: Data being sent to OpenAI API")
    print("=" * 80)
    print("\nSystem message:")
    print("You are a conversation summarizer. You receive conversation transcripts as text and summarize what each participant said. You do not access external systems - you only analyze the text provided to you.")
    print("\n" + "-" * 80)
    print("User prompt:")
    print(prompt)
    print("\n" + "-" * 80)
    print(f"Total conversation lines: {len(conversation_text)}")
    print(f"Total characters in prompt: {len(prompt)}")
    print("=" * 80 + "\n")
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system", 
                "content": "You are a conversation summarizer. You receive conversation transcripts as text and summarize what each participant said. You do not access external systems - you only analyze the text provided to you."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        model="gpt-4o"
    )
    return chat_completion.choices[0].message.content