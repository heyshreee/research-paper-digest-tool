import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from config import APP_TITLE, APP_ICON
from state.session import init_session, reset
from utils.helpers import load_css, STRIP_HASH_JS, LIGHT_THEME_SCRIPT, DARK_THEME_SCRIPT
from components import uploader, loader, paper_info, chat_input
from api import client

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Session
# ---------------------------------------------------------------------------
init_session()

# ---------------------------------------------------------------------------
# CSS + theme + hash strip
# ---------------------------------------------------------------------------
st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)
st.markdown(STRIP_HASH_JS, unsafe_allow_html=True)
if st.session_state.theme == "light":
    st.markdown(LIGHT_THEME_SCRIPT, unsafe_allow_html=True)
else:
    st.markdown(DARK_THEME_SCRIPT, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-brand">
        <span style="color:var(--accent)">{APP_ICON}</span>
        {APP_TITLE}
    </div>
    """, unsafe_allow_html=True)

    if st.button("＋ New Chat", use_container_width=True):
        client.clear_paper()
        reset()
        st.rerun()

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">Current Paper</div>', unsafe_allow_html=True)
    if st.session_state.paper_info:
        info = st.session_state.paper_info
        st.markdown(f"""
        <div class="sidebar-paper">
            📄 {info['filename']}
            <br><span style="color:var(--muted); font-size:0.75rem;">{info['characters']} characters</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.caption("No paper loaded.")

    st.markdown('<div class="sidebar-section-label">Settings</div>', unsafe_allow_html=True)
    theme_choice = st.radio(
        "Appearance",
        ["Dark", "Light"],
        index=0 if st.session_state.theme == "dark" else 1,
        label_visibility="collapsed",
    )
    new_theme = "dark" if theme_choice == "Dark" else "light"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-label">About</div>', unsafe_allow_html=True)
    st.caption(f"{APP_TITLE} v1.0")
    st.caption("SRM Hackathon 2026")

# ---------------------------------------------------------------------------
# View router
# ---------------------------------------------------------------------------
view = st.session_state.view

# ===== LANDING — upload triggers analysis immediately =====
if view == "landing":
    uploaded_file = uploader.render()
    if uploaded_file is not None:
        st.session_state.selected_file = uploaded_file
        st.session_state.analyzing_stage = 0
        st.session_state.analyzing_done = False
        st.session_state.upload_started = False
        st.session_state.upload_response = None
        st.session_state.view = "analyzing"
        st.rerun()

# ===== ANALYZING — upload to backend + show stages =====
elif view == "analyzing":
    selected_file = st.session_state.selected_file
    if selected_file is None:
        reset()
        st.rerun()

    if not st.session_state.upload_started:
        with st.spinner("Uploading PDF..."):
            response = client.upload_pdf(selected_file)
        if not response:
            st.error("Unable to upload the PDF. Check that the backend is running.")
            if st.button("Back to Upload", use_container_width=True):
                reset()
                st.rerun()
            st.stop()
        st.session_state.upload_response = response
        st.session_state.upload_started = True

    loader.render()

    if st.session_state.analyzing_done:
        paper = client.get_paper()
        if not paper:
            st.error("PDF uploaded, but paper info could not be retrieved.")
            if st.button("Back to Upload", use_container_width=True):
                reset()
                st.rerun()
            st.stop()

        st.session_state.paper_info = paper

        digest_resp = client.get_digest()
        if digest_resp and digest_resp.get("digest"):
            st.session_state.digest = digest_resp["digest"]
        else:
            st.session_state.digest = "Could not generate digest."

        st.session_state.messages = []
        st.session_state.selected_file = None
        st.session_state.upload_started = False
        st.session_state.upload_response = None
        st.session_state.view = "ready"
        st.rerun()

# ===== READY — show paper info + digest as first assistant message =====
elif view == "ready":
    info = st.session_state.paper_info
    if not info:
        reset()
        st.rerun()

    digest = st.session_state.digest or ""
    question, send = paper_info.render(info, digest)

    if digest and not st.session_state.messages:
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"**Paper digest:**\n\n{digest}",
        })

    if question and send:
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.view = "thinking"
        st.rerun()

# ===== CHAT — conversation view =====
elif view == "chat":
    info = st.session_state.paper_info
    if not info:
        reset()
        st.rerun()

    question, send = chat_input.render_chat(info)
    if question and send:
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.view = "thinking"
        st.rerun()

# ===== THINKING — call /ask, then back to chat =====
elif view == "thinking":
    info = st.session_state.paper_info
    if not info:
        reset()
        st.rerun()

    chat_input.render_thinking(info)

    if not st.session_state.messages:
        st.session_state.view = "chat"
        st.rerun()

    last_message = st.session_state.messages[-1]
    question = last_message.get("content", "")
    if not question:
        st.session_state.view = "chat"
        st.rerun()

    response = client.ask_question(question)

    if not response:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "I couldn't get a response from the paper analysis backend.",
            "sources": [],
        })
    else:
        st.session_state.messages.append({
            "role": "assistant",
            "content": response.get("answer", "No answer was returned."),
            "sources": response.get("sources", []),
        })

    st.session_state.view = "chat"
    st.rerun()

# ===== UNKNOWN — reset =====
else:
    reset()
    st.rerun()
