import streamlit as st

client = st.session_state.get('openai_client', None)
if client is None:
    if st.button("API Key를 입력하세요."):
        st.switch_page("pages/1_Setting.py")
    st.stop()

def generate_img(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response.data[0].url

st.header("My Chat")

assistant = client.beta.assistants.create(
  instructions="당신은 똑똑한 비서입니다.",
  model="gpt-4o-mini",
  tools=[{"type": "code_interpreter"}]
)

tools = [
    {
        "type":"function",
        "function": {
            "name":"generate_img",
            "description":"Dall-E를 이용해 이미지를 생성하고 이미지 파일 이름을 반환.",
            "parameters": {
                "type":"object",
                "properties": {
                    "prompt": {"type":"string", "description":"image generation prompt"}
                }
            }
        }
    }
]

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