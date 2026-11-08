import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY"),
    http_options=types.HttpOptions(api_version="v1beta"),
)
MODELS = [
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-3.1-flash-lite",
]


def ask_ai(prompt):
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
    )
    return response.text


def safe_ask(prompt):
    try:
        return ask_ai(prompt)
    except Exception as error:
        return f"Something went wrong: {error}"


st.title("Study Buddy")
st.write("Paste your notes, then get a summary or ask a question about them.")


notes = st.text_area("Paste your notes here", height=250)


if st.button("Summarize"):
    if not notes.strip():
        st.warning("Please paste some notes first.")
    else:
        with st.spinner("Reading your notes..."):
            prompt = (
                "Summarize the notes below in 5 short bullet points. "
                "Use very simple English.\n\n"
                f"Notes:\n{notes}"
            )
            st.subheader("Summary")
            st.write(safe_ask(prompt))


st.divider()


question = st.text_input("Ask a question about your notes")


if st.button("Get answer"):
    if not notes.strip() or not question.strip():
        st.warning("Please paste your notes and type a question.")
    else:
        with st.spinner("Thinking..."):
            prompt = (
                "Answer the question using only the notes below. "
                "If the answer is not in the notes, say you cannot find it.\n\n"
                f"Notes:\n{notes}\n\nQuestion: {question}"
            )
            st.subheader("Answer")
            st.write(safe_ask(prompt))
