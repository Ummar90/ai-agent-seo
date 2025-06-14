import openai
from dotenv import load_dotenv
import os
import json
import streamlit as st

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit App
st.title("🧠 AI-Powered SEO Generator")
st.write("Enter a blog topic and get a catchy SEO title, meta description, and a blog post using GPT-4.")

# Input fields
blog_topic = st.text_input("📚 Blog Topic", placeholder="e.g. Benefits of Morning Walk")

tone = st.selectbox(
    "✍️ Choose a Tone/Style",
    ["Professional", "Casual", "Clickbait", "Funny", "Inspirational"]
)

if st.button("Generate SEO"):
    if blog_topic.strip() == "":
        st.warning("Please enter a blog topic.")
    else:
        with st.spinner("Generating SEO Title & Meta Description..."):
            try:
                # Generate SEO title + meta
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an SEO assistant."},
                        {
                            "role": "user",
                            "content": f"Generate a catchy SEO blog title and meta description for the topic: '{blog_topic}' in a {tone.lower()} tone. Respond ONLY in valid JSON format with two keys: title and meta_description."
                        }
                    ]
                )

                output = json.loads(response['choices'][0]['message']['content'])

                st.success("✅ SEO Content Ready!")
                st.subheader("📝 Title")
                st.write(output["title"])
                st.subheader("🔍 Meta Description")
                st.write(output["meta_description"])

            except Exception as e:
                st.error("❌ Failed to generate SEO title/meta")
                st.code(str(e))

        with st.spinner("Writing full blog post..."):
            try:
                # Generate blog post
                blog_response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": f"You are a professional blog writer who writes in a {tone.lower()} tone."},
                        {"role": "user", "content": f"Write a 300-word blog post on: '{blog_topic}'"}
                    ]
                )
                blog_post = blog_response['choices'][0]['message']['content']

                st.success("✅ Blog Post Ready!")
                st.subheader("🧾 Blog Post")
                st.write(blog_post)

            except Exception as e:
                st.error("❌ Blog generation failed:")
                st.code(str(e))
