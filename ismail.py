import streamlit as st
import pandas as pd
from datetime import datetime

# Using session state for data storage instead of SQLite
if 'content_data' not in st.session_state:
    st.session_state.content_data = []

# Data operations
def add_content(title, content):
    st.session_state.content_data.append({
        'id': len(st.session_state.content_data) + 1,
        'title': title,
        'content': content,
        'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def delete_content(id):
    st.session_state.content_data = [
        item for item in st.session_state.content_data if item['id'] != id
    ]

def main():
    st.set_page_config(page_title="Website Content Manager", layout="wide")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Add Content", "Edit Content", "About", "Contact"])
    
    if page == "Home":
        st.title("Welcome to Website Content Manager")
        st.write("View all your website content here")
        
        # Display all content
        for item in st.session_state.content_data:
            with st.container():
                st.subheader(item['title'])
                st.write(item['content'])
                st.write(f"Created: {item['created_date']}")
                st.divider()
    
    elif page == "Add Content":
        st.title("Add New Content")
        
        # Form for adding new content
        with st.form("new_content"):
            title = st.text_input("Title")
            content = st.text_area("Content")
            submitted = st.form_submit_button("Add Content")
            
            if submitted:
                if title and content:
                    add_content(title, content)
                    st.success("Content added successfully!")
                    st.balloons()
                else:
                    st.error("Please fill in all fields")
    
    elif page == "Edit Content":
        st.title("Edit/Delete Content")
        
        # Display all content with delete buttons
        if st.session_state.content_data:
            for item in st.session_state.content_data:
                with st.expander(f"{item['title']}"):
                    st.write(item['content'])
                    st.write(f"Created: {item['created_date']}")
                    if st.button(f"Delete", key=f"delete_{item['id']}"):
                        delete_content(item['id'])
                        st.success("Content deleted!")
                        st.experimental_rerun()
        else:
            st.write("No content available")
    
    elif page == "About":
        st.title("About Us")
        st.write("""
        This is a simple content management system built with Streamlit.
        Use this to manage your website content easily.
        """)
        
    elif page == "Contact":
        st.title("Contact Us")
        st.write("""
        Email: example@email.com
        Phone: +1234567890
        """)
        
        # Contact form
        with st.form("contact_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            message = st.text_area("Message")
            submitted = st.form_submit_button("Send Message")
            
            if submitted:
                if name and email and message:
                    st.success("Message sent successfully!")
                else:
                    st.error("Please fill in all fields")

if __name__ == '__main__':
    main()
