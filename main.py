import openai
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_chat import message
from model import generate_response, load_old_data, load_data, get_answer

# # Clear Session State Variables
# for key in st.session_state.keys():
#     del st.session_state[key]



# df = load_old_data()
df = load_data()

st.set_page_config(page_title="Viewit Property Analyst", page_icon="🤓", 
                   layout="centered", initial_sidebar_state="expanded")

# ViewIt OpenAI API key
openai.organization = st.secrets['org']
openai.api_key = st.secrets['api_key']

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ''


with st.expander("See the data being used"):
    st.write("Here's a sample of our transaction data")
    st.write(f"Total rows: {len(df)}")
    st.dataframe(df.head(25))


def clear():
    st.session_state.user_input = st.session_state.widget
    st.session_state.widget = ''


st.image("https://i.postimg.cc/Nfz5nZ8G/Logo.png", width=200)

# App Title
st.title('ViewIt Chatbot 0.3')

# App Sidebar
with st.sidebar:
    st.markdown(f"""
                # About
                This is version 0.3 of the Chatbot Assistant that will help you look for your desired properties.
                
                # How to use
                Simply enter your query in the text field and the assistant will help you out.
                """)

st.text_input("Ask a question: ", key='widget',
              placeholder='Ask a question...', on_change=clear)

# storing chat history
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

user_input = st.session_state.user_input

# Generate a response if input exists
if user_input:
    output = str(get_answer(user_input, df, temperature=.2))

    # store chat
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, avatar_style='thumbs', key=str(i)+'_user')
        message(st.session_state['generated'][i], key=str(i))
