import streamlit as st
import agent
from IPython.display import Markdown

# Set the title of the app
st.title('VisaGPT')

# Take two inputs from the user
citizenship = st.text_input('Enter the country of your citizenship')
visiting_country = st.text_input('Enter the country you wish to visit')

# Display the output when the button is clicked
with st.spinner('Collecting Information...'):
    if st.button('Submit'):
        if citizenship and visiting_country:
            result=agent.run_crew(citizenship,visiting_country)
            st.write(result)
        

        else:
            st.write('Please enter both your Country of Citizenship and Travel Destination.')