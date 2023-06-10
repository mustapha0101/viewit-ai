import streamlit as st
st.set_page_config(page_title="Viewit Property Analyst", page_icon="📊",
                   layout="centered", initial_sidebar_state="auto")
import os
import openai
import random
from streamlit_chat import message
from datetime import datetime
from model import agent, df_prefix, icons
col1, col2, col3 = st.columns(3)

with col2:
    st.image("https://i.postimg.cc/Nfz5nZ8G/Logo.png", width=200)

# # Clear Session State Variables
# for key in st.session_state.keys():
#     del st.session_state[key]


# ViewIt OpenAI API key
openai.organization = st.secrets['org']
openai.api_key = st.secrets['api_key']


if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ''


def clear():
    st.session_state.user_input = st.session_state.widget
    st.session_state.widget = ''


# App Title
st.title('ViewIt Chatbot 0.3')

datanames = ['real_estate1.csv', 'new_reidin_data.csv', 'pfraw.csv']

data_option = st.radio('Choose the data', datanames,
                       key='radio_option', horizontal=True)

if data_option == 'pfraw.csv':
    df, PREFIX = df_prefix('pfraw.csv')
elif data_option == 'new_reidin_data.csv':
    df, PREFIX = df_prefix('new_reidin_data.csv')
else:
    df, PREFIX = df_prefix('real_estate1.csv')


with st.expander("Show data"):
    st.write(f"Total rows: {len(df)}")
    st.dataframe(df)


# App Sidebar
with st.sidebar:
    st.markdown(f"""
                # About
                This is version 0.3 of the Chatbot Assistant that will help you
                  look for your desired properties.
                
                # How to use
                Simply enter your query in the text field and the assistant 
                will help you out.
                """)


st.text_input("Ask a question: ", key='widget',
              placeholder='Ask a question...', on_change=clear)


# storing chat history
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

user_input = st.session_state.user_input

datenow = datetime.now().strftime("%Y_%m_%d")

# Generate a response if input exists
if user_input:
    user_log = f"\nUser [{datetime.now().strftime('%H:%M:%S')}]: " + user_input
    print(user_log)

    with st.spinner('Thinking...'):
        output = str(agent.run(user_input))
        response_log = f"Bot [{datetime.now().strftime('%H:%M:%S')}]: " + output
        print(response_log)
        # store chat
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True,
                avatar_style='thumbs', key=str(i)+'_user')
        message(st.session_state['generated'][i], key=str(i))


st.write("---")
st.caption(
    """Made by Hamdan Mohammad. [GitHub](https://github.com/hamdan-27) | 
    [Instagram](https://instagram/hxm.dxn_)""")
# st.caption(
#     "Like what we're building? [Join the waitlist](https://tally.so/r/w4QW4r)")