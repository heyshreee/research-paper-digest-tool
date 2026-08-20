import streamlit as st


def _render_messages():
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'''
            <div class="msg msg-user">
                <div class="msg-label">You</div>
                <div class="msg-bubble">{msg["content"]}</div>
            </div>''', unsafe_allow_html=True)
        else:
            sources_html = ""
            if "sources" in msg and msg["sources"]:
                items = "".join(
                    f'<div class="source-item">Page {s["page"]} &middot; {s["section"]}</div>'
                    for s in msg["sources"]
                )
                sources_html = f'''
                <div class="sources-card">
                    <div class="sources-header">Sources</div>
                    {items}
                </div>'''
            st.markdown(f'''
            <div class="msg msg-assistant">
                <div class="msg-label">◈ PaperLens</div>
                <div class="msg-bubble">{msg["content"]}{sources_html}</div>
            </div>''', unsafe_allow_html=True)


def render_chat(info):
    st.markdown(f'''
    <div class="chat-layout">
        <div class="chat-header">
            <h1 class="paper-title" style="font-size:1.1rem;">{info['title']}</h1>
            <p class="paper-meta">{info['authors']} &middot; {info['pages']} pages</p>
        </div>
        <div class="chat-messages" id="chat-messages">
    ''', unsafe_allow_html=True)

    _render_messages()

    st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="chat-input-wrapper">', unsafe_allow_html=True)
    cols = st.columns([1, 8, 1])
    with cols[0]:
        st.markdown("")
    with cols[1]:
        question = st.text_input(
            "Ask about your paper",
            placeholder="Ask about your paper...",
            label_visibility="collapsed",
            key="chat_input",
        )
    with cols[2]:
        send = st.button("➤", key="chat_send")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <script>
    (function(){
        var el = document.getElementById('chat-messages');
        if(el) el.scrollTop = el.scrollHeight;
    })();
    </script>
    """, unsafe_allow_html=True)

    return question, send


def render_thinking(info):
    st.markdown(f'''
    <div class="chat-layout">
        <div class="chat-header">
            <h1 class="paper-title" style="font-size:1.1rem;">{info['title']}</h1>
            <p class="paper-meta">{info['authors']} &middot; {info['pages']} pages</p>
        </div>
        <div class="chat-messages" id="chat-messages">
    ''', unsafe_allow_html=True)

    _render_messages()

    st.markdown('''
    <div class="msg msg-assistant">
        <div class="msg-label">◈ PaperLens</div>
        <div class="msg-bubble">
            <span class="thinking-text">Retrieving relevant sections &rarr; Analyzing context &rarr; Generating answer</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)
