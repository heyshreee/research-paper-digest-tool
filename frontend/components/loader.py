import streamlit as st
import time


ANALYZING_STAGES = [
    ("Uploading PDF", 2.0),
    ("Extracting text", 1.5),
    ("Building research context", 2.0),
    ("Generating digest", 2.0),
]


def render():
    total = len(ANALYZING_STAGES)

    if not st.session_state.analyzing_done:
        if st.session_state.analyzing_stage < total:
            label, duration = ANALYZING_STAGES[st.session_state.analyzing_stage]
            time.sleep(duration)
            st.session_state.analyzing_stage += 1
            if st.session_state.analyzing_stage >= total:
                st.session_state.analyzing_done = True
            st.rerun()

    stages_html = ""
    for i, (label, _) in enumerate(ANALYZING_STAGES):
        if i < st.session_state.analyzing_stage:
            stages_html += f'<div class="stage stage-done"><span class="stage-icon">✓</span>{label}</div>'
        elif i == st.session_state.analyzing_stage and not st.session_state.analyzing_done:
            stages_html += f'<div class="stage stage-active"><span class="stage-icon">●</span>{label}</div>'
        else:
            stages_html += f'<div class="stage stage-pending"><span class="stage-icon">○</span>{label}</div>'

    progress = st.session_state.analyzing_stage / total if total > 0 else 0

    st.markdown(f"""
    <div class="main-container">
        <div class="center-content">
            <div class="analyzing-container">
                <div class="analyzing-title">Analyzing your paper...</div>
                {stages_html}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.progress(progress)
