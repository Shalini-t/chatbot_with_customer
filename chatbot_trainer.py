import streamlit as st
import openai
import matplotlib.pyplot as plt
import numpy as np

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

import streamlit as st

def reset_page():
    # Add custom JavaScript to reload the page
    st.session_state.messages=[]
    st.markdown(
        """
        <script>
            document.getElementById('reset-button').onclick = function() {
                location.reload();
            };
        </script>
        """,
        unsafe_allow_html=True
    )




def generate_report(example_string):
    # Dummy data for demonstration
    import re

    numeric_values = re.findall(r'\d+', example_string)
    numeric_values = [int(value) for value in numeric_values]
    if numeric_values==[]:
      numeric_values=[0,0,0,2]
    print(numeric_values)

    #st.write(example_string)
    if st.session_state.clicked:
        criteria = ['Communication Skills', 'Problem-Solving Abilities', 'Emotional Intelligence', 'Product Overall Performance']
        scores = np.array(numeric_values)
        #st.write(scores)
        # Generate charts
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.bar(criteria, scores)
        ax.set_title('User Performance Report')
        ax.set_ylabel('Scores')
        ax.set_xlabel('Criteria')
        st.pyplot(fig)

def main():
    st.title("Welcome to Customer Care Agent Training")
    st.write("This is a platform for training customer care agents.")
    # Add a reset button
    reset_button = st.button("Reset Page", key='reset-button')

    # Call the reset_page function to include JavaScript
    reset_page()
    # Redirect to new page
    # First drop-down box with 5 values
    option1 = st.selectbox('Select the field you want to be trained',('Banking', 'IT Helpdesk', 'Customer Service', 'Bookings and Travel', 'Emergency Response'))
    st.write('You selected:', option1) 

    option2 = st.selectbox('Select the type of customer to interact with',('Calm', 'Neutral', 'Angry', 'Random'))
    st.write('You selected:', option2) 
    st.session_state.messages =[{"role": "system", "content": "Consider yourself as an {} customer who is going to have a chat conversation with a me where I am going to act like customer agent from {} industry sector. This is a simulation of real world customer agent conversation so maintain your tone of conversation to be {} throughout the chat and your responses should be within 100 words and generate random details for your identity when asked. Remember you are the customer seeking help or support".format(option2, option1, option2)}]
    
    if option1 and option2:
        st.title("ChatBot Trainer")

        openai.api_key = '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'

        if "openai_model" not in st.session_state:
          st.session_state["openai_model"] = "gpt-3.5-turbo"

        if "messages" not in st.session_state:
          st.session_state.messages =[{"role": "system", "content":"Consider yourself as an {} customer who is going to have a chat conversation with a me who is going act like customer agent from {} industry sector. This is a simulation of real world customer agent conversation so maintain your tone of conversation to be {} throughout the chat and your responses should be within 100 words and generate random details for your identity when asked. Remember you are the customer seeking help or support".format(option2, option1, option2)}]
          
        # for message in st.session_state.messages:
        #   with st.chat_message(message["role"]):
        #     st.markdown(message["content"])

        if prompt := st.chat_input("What is up?"):
          st.session_state.messages.append({"role": "user", "content": prompt})
          with st.chat_message("user"):
            st.markdown(prompt)

          with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
              model=st.session_state["openai_model"],
              messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
              ],
              stream=True,
            ):
              full_response += response.choices[0].delta.get("content", "")
              message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
          st.session_state.messages.append({"role": "assistant", "content": full_response})
    if st.button('End Chat', on_click=click_button):
        message = "Generate a report on the user's performance based on the criteria Communication Skills,Problem-Solving Abilities,Emotional Intelligence,Product Overall Performance ratings and the output scores should be displayed in the form of python list with scores as shown [ Communication Skills score,Problem-Solving Abilities score,Emotional Intelligence score,Product Overall Performance score] with no extra contents and the values inside the square bracket should be numbers between 1 to 10. For example if Communication Skills score is 2,Problem-Solving Abilities score is 5,Emotional Intelligence score is 6,Product Overall Performance score is 7 give output only this [2,5,6,7]. Nothing else is required"
        st.session_state.messages.append({"role": "user", "content": message})
        # Request gpt-3.5-turbo for chat completion
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])

        # Print the response and add it to the messages list
        chat_message = response['choices'][0]['message']['content']
        print(chat_message)
        # print(f"Bot: {chat_message}")
        generate_report(chat_message)
        #st.session_state.messages=[]

if __name__ == "__main__":
    main()
