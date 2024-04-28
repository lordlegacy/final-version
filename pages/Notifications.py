import streamlit as st


st.title('Notification Settings')


notification_method = st.radio('Select Notification Method', ['Email', 'WhatsApp'])

if notification_method == 'Email':
    email_address = st.text_input('Enter Email Address')
    st.write('You will be notified via Email at:', email_address)
elif notification_method == 'WhatsApp':
    phone_number = st.text_input('Enter Phone Number')
    st.write('You will be notified via WhatsApp at:', phone_number)

