import streamlit as st
import openai

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

if prompt := st.chat_input("Ask any question"):
    messages = st.container(height=600)
    messages.chat_message("user").write(prompt)

    thread = client.beta.threads.create(
    messages=[
        {
            "role":"user",
            "content": messages
        }
    ]
    )

    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    poll_interval_ms=2000
    )

    if run.status == 'completed':
        thread_messages = client.beta.threads.messages.list(thread.id)
        for msg in thread_messages.data[::-1]:
            messages.chat_message("assistant").write(f"Echo: {msg.content[0].text.value}")