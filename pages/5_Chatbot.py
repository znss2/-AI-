import streamlit as st

client = st.session_state.get('openai_client', None)
if client is None:
    if st.button("API Key를 입력하세요."):
        st.switch_page("pages/1_Setting.py")
    st.stop()

import requests
url = "https://www.law.go.kr/학칙공단/국립부경대학교 도서관 규정/(1316,20231227)"

r = requests.get(url)

with open("pknu_library_rule.csv",'w') as fo:
  fo.write(r.text)

my_file = client.files.create(
    file = open("pknu_library_rule.csv",'rb'),
    purpose='assistants'
)

assistant = client.beta.assistants.create(
  name="데이터 분석 전문가",
  instructions="당신은 데이터 분석 전문가입니다.",
  model="gpt-4o-mini",
  tools=[{"type": "code_interpreter"}]
)

thread = client.beta.threads.create()

st.header("My Chatbot")

if prompt := st.chat_input("Ask any question"):
    messages = st.container(height=600)
    messages.chat_message("user").write(prompt)

    new_message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role="user",
    content=prompt
    )
    run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)

    run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread.id,
        run_id=run.id
    )

    thread_messages = client.beta.threads.messages.list(thread.id)

    if run.status == 'completed':
        thread_messages = client.beta.threads.messages.list(thread.id, limit = 1)
        for msg in thread_messages.data[::-1]:
            messages.chat_message(msg.role).write(f"Echo: {msg.content[0].text.value}")