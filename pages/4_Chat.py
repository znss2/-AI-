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
  model="gpt-4o-mini",
  tools=[{"type": "code_interpreter"}]
)

thread = client.beta.threads.create()

if prompt := st.chat_input("Ask any question"):
    messages = st.container(height=600)
    messages.chat_message("user").write(prompt)

    new_message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role="user",
    content=prompt
    )

    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    poll_interval_ms=2000
    )

    if run.status == 'completed':
        thread_messages = client.beta.threads.messages.list(thread.id, limit = 1)
        for msg in thread_messages.data[::-1]:
            messages.chat_message(msg.role).write(f"Echo: {msg.content[0].text.value}")

    if st.button("Clear"):
        response = client.beta.threads.delete(thread.id)
        thread = client.beta.threads.create()

    if st.button("Exit Chat"):
        response = client.beta.threads.delete(thread.id)
        response = client.beta.assistants.delete(assistant.id)