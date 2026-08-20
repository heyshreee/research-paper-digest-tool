import html
import streamlit as st


def _escape(value):
    """Safely render user/API text inside HTML."""
    return html.escape(str(value))


def _render_sources(sources):
    """Render source references below an assistant answer."""

    if not sources:
        return ""

    items = []

    for source in sources:
        if isinstance(source, dict):
            page = source.get("page", "?")
            section = source.get("section", "Unknown section")

            items.append(
                f"""
                <div class="source-item">
                    Page {html.escape(str(page))}
                    &middot;
                    {html.escape(str(section))}
                </div>
                """
            )

        elif isinstance(source, str):
            items.append(
                f"""
                <div class="source-item">
                    {html.escape(source)}
                </div>
                """
            )

    if not items:
        return ""

    return f"""
        <div class="sources-card">
            <div class="sources-header">Sources</div>
            {''.join(items)}
        </div>
    """


def render_message(message):
    """
    Render a single chat message.

    Expected message format:

    {
        "role": "user" | "assistant",
        "content": "...",
        "sources": [...]
    }
    """

    role = message.get("role", "assistant")
    content = message.get("content", "")

    safe_content = _escape(content)

    if role == "user":
        st.markdown(
            f"""
            <div class="msg msg-user">
                <div class="msg-label">You</div>

                <div class="msg-bubble">
                    {safe_content}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        sources = _render_sources(
            message.get("sources", [])
        )

        st.markdown(
            f"""
            <div class="msg msg-assistant">
                <div class="msg-label">
                    ◈ PaperLens
                </div>

                <div class="msg-bubble">
                    {safe_content}
                    {sources}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_messages():
    """
    Render all messages stored in Streamlit session state.
    """

    messages = st.session_state.get("messages", [])

    if not messages:
        return

    st.markdown(
        '<div class="chat-messages" id="chat-messages">',
        unsafe_allow_html=True,
    )

    for message in messages:
        render_message(message)

    st.markdown(
        """
        </div>

        <script>
        (function () {
            const container =
                document.getElementById("chat-messages");

            if (container) {
                container.scrollTop = container.scrollHeight;
            }
        })();
        </script>
        """,
        unsafe_allow_html=True,
    )


def render_thinking():
    """
    Display the assistant processing state.

    This intentionally shows high-level processing stages
    rather than exposing hidden model chain-of-thought.
    """

    st.markdown(
        """
        <div class="msg msg-assistant">
            <div class="msg-label">
                ◈ PaperLens
            </div>

            <div class="msg-bubble">
                <span class="thinking-text">
                    Retrieving relevant sections
                    &nbsp;→&nbsp;
                    Analyzing context
                    &nbsp;→&nbsp;
                    Generating answer
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render(info):
    """
    Render the complete chat area.

    `info` should contain:
        title
        authors
        pages
    """

    title = _escape(info.get("title", "Research Paper"))
    authors = _escape(info.get("authors", "Unknown authors"))
    pages = _escape(info.get("pages", "—"))

    st.markdown(
        f"""
        <div class="chat-layout">

            <div class="chat-header">

                <div class="brand">
                    ◈ PaperLens
                </div>

                <h1 class="paper-title"
                    style="font-size:1.1rem;">
                    {title}
                </h1>

                <p class="paper-meta">
                    {authors} &middot; {pages} pages
                </p>

            </div>
        """,
        unsafe_allow_html=True,
    )

    render_messages()

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )