import streamlit as st


def render():
    st.markdown("""
    <div class="main-container">
        <div class="center-content">
            <div class="brand">◈ PaperLens</div>
            <h1 class="page-title">Research Paper Digest</h1>
            <p class="page-subtitle">Upload a paper and start exploring.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drop PDF here — or click to browse",
        type=["pdf"],
        label_visibility="collapsed",
        key="landing_uploader",
    )

    st.markdown("""
    <div style="width:100%; max-width:560px; margin:0 auto;">
        <div class="input-bar">
            <span class="attach-btn">📎</span>
            <span style="color:var(--muted); font-size:0.88rem;">Upload a document to start asking questions...</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    return uploaded
