# from dotenv import load_dotenv
# load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st

chat_model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash"
)
result_area = st.empty()

st.title('인공지능 시인 :sunglasses:')

st.markdown("### 시의 주제를 제시해주세요.")
col1, col2 = st.columns([5, 1])
with col1:
    content = st.text_input(
        "시의 주제",
        placeholder="예: 첫사랑, 가을, 인공지능",
        label_visibility="collapsed"
    )
with col2:
    button = st.button(
        "시 작성 ✍️",
        use_container_width=True
    )

if button:
    result_area.empty()
    if content and content.strip():
        with st.spinner('시를 작성하고 있습니다...'):
            result = chat_model.invoke(content + "에 대한 시를 써줘")
            st.write(f"""
            >> {content}에 대한 시
            
            {result.content[0]["text"]}
            """)
    else:
        st.warning("시의 주제를 입력해주세요.")