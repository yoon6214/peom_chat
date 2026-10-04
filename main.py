from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import html
from pathlib import Path

st.set_page_config(
    page_title="인공지능 시인",
    page_icon="✍️",
    layout="wide",
)

chat_model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash"
)

css_path = Path(__file__).parent / "style.css"
if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="title-area">
        <h1>인공지능 시인 <span>✍️</span></h1>
        <p>원하는 주제를 입력하면 AI가 시를 만들어드려요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-title">
        <span>📖</span> 시의 주제를 입력해주세요.
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([5, 1], gap="small")
with col1:
    content = st.text_input(
        "시의 주제",
        placeholder="예: 첫사랑, 가을, 인공지능",
        label_visibility="collapsed",
    )
with col2:
    button = st.button(
        "시 작성 ✍️",
        use_container_width=True,
    )

if button:
    if content and content.strip():

        with st.spinner("시를 작성하고 있습니다... ✨"):
            result = chat_model.invoke(
                content.strip() + "에 대한 시를 써줘"
            )

        poem_text = result.content

        # Gemini 응답 형태 처리
        if isinstance(poem_text, list):
            parts = []
            for item in poem_text:
                if isinstance(item, dict):
                    text = item.get("text")
                    if text:
                        parts.append(str(text))
                else:
                    parts.append(str(item))
            poem_text = "\n".join(parts)
        else:
            poem_text = str(poem_text)

        lines = [
            line.strip()
            for line in poem_text.strip().splitlines()
            if line.strip()
        ]

        if lines:
            poem_title = lines[0].replace("**", "").strip()
            poem_body = lines[1:]
        else:
            poem_title = f"{content.strip()}에 대한 시"
            poem_body = []

        safe_title = html.escape(poem_title)

        body_html = "".join(
            f"<p>{html.escape(line)}</p>"
            for line in poem_body
        )

        st.html(
            f"""
            <div class="result-card">

                <div class="result-header">
                    <div class="result-title">
                        ✨ {safe_title}
                    </div>

                    <div class="result-label">
                        AI가 만든 시
                    </div>
                </div>

                <div class="poem-content">
                    {body_html}
                </div>

                <div class="result-footer">
                    주제 · {html.escape(content.strip())}
                </div>

            </div>
            """
        )

    else:
        st.warning("시의 주제를 입력해주세요.")
