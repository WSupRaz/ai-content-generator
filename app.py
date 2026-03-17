import streamlit as st
import requests
import os
from dotenv import load_dotenv

# ------------------------
# LOAD ENV VARIABLES
# ------------------------
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", None)

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}" if API_KEY else "",
    "Content-Type": "application/json"
}

# ------------------------
# PAGE CONFIG
# ------------------------
st.set_page_config(page_title="AI Content Generator", layout="wide")

st.title("🚀 AI Content Generator for Creators")

# ------------------------
# DEBUG STATUS (IMPORTANT)
# ------------------------
st.write("✅ App Started")
st.write("🔑 API Key:", "FOUND" if API_KEY else "❌ MISSING")

# ------------------------
# SIDEBAR SETTINGS
# ------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    platform = st.selectbox(
        "Platform",
        ["YouTube Shorts", "YouTube Long", "LinkedIn"]
    )

    tone = st.selectbox(
        "Tone",
        ["Motivational", "Funny", "Educational", "Controversial"]
    )

    audience = st.text_input("Target Audience", "Students")

# ------------------------
# MAIN INPUT
# ------------------------
topic = st.text_input("💡 Enter your topic")

# ------------------------
# GENERATE BUTTON
# ------------------------
if st.button("🔥 Generate Content"):

    try:
        # Check topic
        if not topic:
            st.warning("Please enter a topic")
            st.stop()

        # Check API key
        if not API_KEY:
            st.error("❌ API Key Missing! Add it in Streamlit secrets.")
            st.stop()

        # Prompt
        prompt = f"""
You are a viral content creator expert.

Create content for:
Platform: {platform}
Tone: {tone}
Audience: {audience}

Topic: {topic}

Give output in this format:

1. 3 Viral Hooks
2. Full Script (engaging, emotional, high retention)
3. 5 Catchy Titles
4. Thumbnail Ideas
5. Hashtags
"""

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        # Loader
        with st.spinner("🚀 Generating viral content..."):
            response = requests.post(url, headers=headers, json=data)

        # Debug response
        st.write("📡 Status Code:", response.status_code)

        try:
            result = response.json()
        except:
            st.error("❌ Failed to parse response")
            st.stop()

        # If success
        if "choices" in result:
            output = result["choices"][0]["message"]["content"]

            st.subheader("🔥 Generated Content")
            st.write(output)

            # Download button
            st.download_button(
                "⬇️ Download Content",
                data=output,
                file_name="content.txt",
                use_container_width=True
            )

        else:
            st.error("❌ API Error")
            st.write(result)

    except Exception as e:
        st.error(f"❌ App Crashed: {e}")