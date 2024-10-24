import base64
import streamlit as st
import conn_db


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()



def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    ''' % bin_str
    # st.markdown(page_bg_img, unsafe_allow_html=True)
    return page_bg_img

   

# set_background('background.png')

def load_css(file_name):
    with open(file_name) as f:
        return f"{set_background('bg2.png')}{f.read()}</style>"

container = st.container()
def show_prompt(container,role,content):
    if role == 'user':
        head = ''
    else:
        head = 'Analysis'

    container.markdown(f'''
    <div class="{role}-message">
        <div class="message">{content}</div>
        
    
    ''', unsafe_allow_html=True)

# <div class="icon"></div>
    
def show_history(container):
    container.markdown('<div class="chat-container">', unsafe_allow_html=True)
    if st.session_state.selected_option in conn_db.get_history().session_name.unique().tolist():
        message = conn_db.get_history()[conn_db.get_history().session_name==st.session_state.selected_option].reset_index(drop=True)
        shape_chat = message.shape[0]
        for i in range(shape_chat):
            # if message['role'].iloc[i] == 'assistant':
                show_prompt(container,message['role'].iloc[i],message['content'].iloc[i])
            # else:
            #     sy.show_prompt(message['role'].iloc[i],message['content'].iloc[i])            
    container.markdown('</div>', unsafe_allow_html=True)