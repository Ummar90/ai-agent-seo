import openai
from dotenv import load_dotenv
import os
import json

# Load .env and API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 📝 Step 1: Ask user for blog topic
blog_topic = input("📚 Enter your blog topic: ")

# 🤖 Step 2: Send prompt to GPT
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an SEO assistant."},
        {
            "role": "user",
            "content": f"Generate a catchy SEO blog title and meta description for the topic: '{blog_topic}'. Respond ONLY in valid JSON format with two keys: title and meta_description."
        }
    ]
)

# 📦 Step 3: Parse and display output
try:
    output = json.loads(response['choices'][0]['message']['content'])
    print("\n✅ SEO Results:")
    print("Title:", output["title"])
    print("Meta Description:", output["meta_description"])
except json.JSONDecodeError:
    print("⚠️ GPT did not return valid JSON. Raw output:")
    print(response['choices'][0]['message']['content'])
