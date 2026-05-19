import streamlit as st

from retriever import retrieve_top_k
from openai_llm import ask_openai
from gemini_llm import ask_gemini
from knowledge_loader import load_knowledge
from firebase_db import get_or_create_google_user
from firebase_activity import log_login, log_action


# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Lotus Hospital Multi LLM Chat",
    page_icon="🏥",
    layout="wide"
)


# -------------------------------
# SESSION STATE
# -------------------------------
if "signed_in" not in st.session_state:
    st.session_state.signed_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "openai"


# -------------------------------
# LOGIN SIDEBAR
# -------------------------------
with st.sidebar:
    st.title("🏥 Hospital Chat")

    if not st.session_state.signed_in:

        email = st.text_input("Email")
        name = st.text_input("Name")

        if st.button("Login"):
            if email and name:

                user = get_or_create_google_user(email, name)

                st.session_state.user = user
                st.session_state.signed_in = True

                log_login(user["user_id"], user["email"], user["display_name"])
                log_action(user["user_id"], "login")

                st.rerun()

            else:
                st.error("Enter email and name")

    else:
        st.success(f"Hi {st.session_state.user['display_name']}")

        if st.button("Logout"):
            log_action(st.session_state.user["user_id"], "logout")
            st.session_state.clear()
            st.rerun()


# -------------------------------
# MAIN APP
# -------------------------------
st.title("🏥 Hospital AI Assistant")

if not st.session_state.signed_in:
    st.info("Please login to continue")
    st.stop()

user = st.session_state.user


# -------------------------------
# SHOW CHAT HISTORY
# -------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# -------------------------------
# INPUT BOX
# -------------------------------
query = st.chat_input("Ask your question...")

if query:

    # save user message
    st.session_state.messages.append(
        {"role": "user", "content": query}
    )

    log_action(user["user_id"], "asked_question")

    # -------------------------------
    # RETRIEVE CONTEXT
    # -------------------------------
    context = retrieve_top_k(query)

    # -------------------------------
    # CALL BOTH LLMs
    # -------------------------------
    openai_ans = ask_openai(query, context)

    gemini_ans = ask_gemini(query, context)

    # -------------------------------
    # GEMINI FALLBACK → KNOWLEDGE FILE
    # -------------------------------
    if not gemini_ans:
        knowledge_text = load_knowledge()
        gemini_ans = knowledge_text


    # -------------------------------
    # SIDE BY SIDE UI
    # -------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🤖 OpenAI Answer")
        st.write(openai_ans)

    with col2:
        st.subheader("🧠 Gemini Answer")
        st.write(gemini_ans)

    st.markdown("---")


    # -------------------------------
    # SELECTION BUTTONS
    # -------------------------------
    col3, col4 = st.columns(2)

    with col3:
        if st.button("✅ Select OpenAI"):
            st.session_state.selected_model = "openai"
            log_action(user["user_id"], "selected_openai")

    with col4:
        if st.button("✅ Select Gemini"):
            st.session_state.selected_model = "gemini"
            log_action(user["user_id"], "selected_gemini")


    # -------------------------------
    # SAVE FINAL MESSAGE BASED ON SELECTION
    # -------------------------------
    final_answer = (
        openai_ans if st.session_state.selected_model == "openai"
        else gemini_ans
    )

    st.session_state.messages.append(
        {"role": "assistant", "content": final_answer}
    )

    log_action(user["user_id"], "got_answer")