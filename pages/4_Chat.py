import streamlit as st

client = st.session_state.get('openai_client', None)
if client is None:
    if st.button("API Key를 입력하세요."):
        st.switch_page("pages/1_Setting.py")
    st.stop()

st.header("My Chat")

assistant = client.beta.assistants.create(
  instructions="당신은 똑똑한 비서입니다.",
  model="gpt-4o-mini"
)

prompt = st.chat_input("Ask any question")

with st.sidebar:
    messages = st.container(height=300)
    if prompt := st.chat_input("Say something"):
        messages.chat_message("user").write(prompt)
        messages.chat_message("assistant").write(f"Echo: {prompt}")