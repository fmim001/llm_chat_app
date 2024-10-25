import streamlit as st
import numpy as np
import random
import base64
import sqlite3 as db
import pandas as pd
import conn_db 
import dr_var 
import styles as sy
import time



if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None

if 'title_name' not in st.session_state:
    st.session_state.title_name = 'default session'


if 'list_session' not in st.session_state:    
    st.session_state.list_session = None

st.session_state.list_session = conn_db.get_history()['session_name'].unique().tolist()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": 'What can I help with?'})

# st.title("Reference ChatBot",anchor=None)
st.logo('logo.png',size="large", link=None, icon_image=None)



def change_session(selected_option):
    st.session_state.selected_option = selected_option
    st.session_state.title_name = st.session_state.selected_option 

def new_session():
    st.session_state.selected_option = None
    st.session_state.my_selectbox = st.session_state.selected_option
    st.session_state.title_name = st.session_state.selected_option 
    

def delete_session(selected_option):
    conn_db.delete_db(selected_option)
    st.session_state.selected_option = None
    st.session_state.my_selectbox = st.session_state.selected_option
    st.session_state.title_name = st.session_state.selected_option 
    
def on_select():
    st.session_state.selected_option = st.session_state.my_selectbox 
    st.session_state.title_name = st.session_state.selected_option

list_session = st.session_state.list_session     
def index_list(list_session,value):
    if value not in  list_session:
        return None
    else:
        return list_session.index(value)

# st.title(st.session_state.title_name,anchor=False)


side =  st.sidebar
def zero_session(side):
    global col1,col2
    side.button('new session',
                on_click=new_session,
                use_container_width=True,
                help="Create New Session",
                key="new_session")
    con1 = side.container(border=True,key="session_option")
    col1,col2 = con1.columns([6,1])




ref = sy.load_css('styles.css')   
st.markdown(ref,unsafe_allow_html=True)

# Set a default model
chat_con = st.container(key="chat_con")

sy.show_history(container=chat_con)


# Accept user input
if prompt := st.chat_input("What is up?",key="prompt"):
    # Add user message to chat history
    # st.session_state.messages.append({"role": "user", "content": prompt})
    # st.write(conn_db.get_history().session_name.unique().tolist())
    if st.session_state.selected_option not in conn_db.get_history().session_name.unique().tolist():
        session = prompt
        st.session_state.selected_option = session
        st.session_state.title_name = st.session_state.selected_option
        # st.session_state.my_selectbox = st.session_state.selected_option
        
    else:
        # st.session_state.selected_option = st.session_state.my_selectbox
        session = st.session_state.selected_option
        st.session_state.title_name = st.session_state.selected_option

    conn_db.insert_db(session=session,role='user',content=prompt)
    # Display user message in chat message container
    sy.show_prompt(chat_con,'user',prompt)
    # stream = dr_var.get_llm_response(
    #         input_text=prompt
    #         )
    stream = 'test response'
    sy.show_prompt(chat_con,'assistant',stream)
    # st.session_state.messages.append({"role": "assistant", "content": stream})
    conn_db.insert_db(session=session,role='assistant',content=stream)

if st.session_state.selected_option==None:
    zero_session(chat_con)
else:
    zero_session(side)
# Display chat messages from history on app rerun

con2 = side.container(key="container_sidebar_title")
# st.write(st.session_state.selected_option)
# st.write(selected_option)
col2.button('x',
            on_click=delete_session,args=[st.session_state.selected_option],
            help="delete current session")
col1.selectbox('Select Session',
               options=conn_db.get_history()['session_name'].unique().tolist(),
               index=None,
               key='my_selectbox',
               on_change=on_select,
               placeholder="Select Session History")
con2.header(f'Current Session')
con2.markdown(f'''<p1>{st.session_state.title_name}</p1>
    ''', unsafe_allow_html=True)
