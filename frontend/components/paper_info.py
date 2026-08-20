import streamlit as st


def render(info, digest):
    st.markdown(f"""
    <div class="main-container">
        <div class="center-content">
            <div class="paper-header">
                <h1 class="paper-title">{info['filename']}</h1>
                <p class="paper-meta">{info['characters']} characters extracted</p>
            </div>
            <p class="ready-prompt">What would you like to know?</p>
            <div class="suggested-questions">
                <div class="suggested-btn" onclick="void(0)">What is the main contribution?</div>
                <div class="suggested-btn" onclick="void(0)">What dataset did they use?</div>
                <div class="suggested-btn" onclick="void(0)">What are the main results?</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns([1, 8, 1])
    with cols[0]:
        st.markdown("")
    with cols[1]:
        question = st.text_input(
            "Ask about your paper",
            placeholder="Ask about your paper...",
            label_visibility="collapsed",
            key="ready_input",
        )
    with cols[2]:
        send = st.button("➤", key="ready_send")

    return question, send
