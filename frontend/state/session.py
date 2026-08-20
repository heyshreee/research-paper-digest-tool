import streamlit as st


def init_session():
    defaults = {
        "view": "landing",
        "messages": [],
        "paper_info": None,
        "digest": None,
        "selected_file": None,
        "theme": "dark",
        "analyzing_stage": 0,
        "analyzing_done": False,
        "upload_started": False,
        "upload_response": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def reset():
    st.session_state.view = "landing"
    st.session_state.messages = []
    st.session_state.paper_info = None
    st.session_state.digest = None
    st.session_state.selected_file = None
    st.session_state.analyzing_stage = 0
    st.session_state.analyzing_done = False
    st.session_state.upload_started = False
    st.session_state.upload_response = None
