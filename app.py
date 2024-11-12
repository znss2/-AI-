import streamlit as st
import openai
from openai import OpenAI

st.title("gpt-4o-mini 체험")

user_api_key = st.text_input("api키를 입력하세요", type="password")

client = OpenAI(api_key=user_api_key)
