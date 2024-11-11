import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Database setup
def init_db():
    conn = sqlite3.connect('website.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS content
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  content TEXT NOT NULL,
                  created_date TIMESTAMP)''')
    conn.commit()
    conn.close()

# Database operations
def add_content(title, content):
    conn = sqlite3.connect('website.db')
    c = conn.cursor()
    c.execute('INSERT INTO content (title, content, created_date) VALUES (?, ?, ?)',
              (title, content, datetime.now()))
    conn.commit()
    conn.close()

def get_all_content():
    conn = sqlite3.connect('website.db')
    df = pd.read_sql_query('SELECT * FROM content', conn)
    conn.close()
    return df

def delete_content(id):
    conn = sqlite3.connect('website.db')
    c = conn.cursor()
    c.execute('DELETE FROM content WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Streamlit UI
def main():
    st.set_page_config(page_title="Website Content Manager", layout="wide")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Add Content", "Edit Content", "About", "Contact"])
    
    if page == "Home":
        st.title("Welcome to Website Content Manager")
        st.write("View all your website content here")
        
        # Display all content
        df = get_all_content()
        if not df.empty:
            for _, row in df.iterrows():
                with st.container():
                    st.subheader(row['title'])
                    st.write(row['content'])
                    st.write(f"Created: {row['created_date']}")
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
        df = get_all_content()
        if not df.empty:
            for _, row in df.iterrows():
                with st.expander(f"{row['title']}"):
                    st.write(row['content'])
                    st.write(f"Created: {row['created_date']}")
                    if st.button(f"Delete", key=f"delete_{row['id']}"):
                        delete_content(row['id'])
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
