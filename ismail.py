import streamlit as st
import pandas as pd
from datetime import datetime

def main():
    st.set_page_config(
        page_title="Website Content Manager",
        page_icon="📝",
        layout="wide"
    )

    # Header
    st.title("Website Content Manager 📝")
    st.markdown("---")

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page:", ["Home", "Add Content", "View Content", "Settings"])

    if page == "Home":
        st.header("Welcome to Website Content Manager!")
        st.write("This is a simple website content management system.")
        
        # Some sample metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Posts", value="5")
        with col2:
            st.metric(label="Active Users", value="3")
        with col3:
            st.metric(label="Views", value="150")

    elif page == "Add Content":
        st.header("Add New Content")
        
        # Content Form
        with st.form("content_form"):
            title = st.text_input("Title")
            category = st.selectbox("Category", ["Blog", "News", "Tutorial"])
            content = st.text_area("Content")
            publish = st.checkbox("Publish immediately")
            
            submitted = st.form_submit_button("Submit")
            if submitted:
                st.success("Content added successfully!")
                st.balloons()

    elif page == "View Content":
        st.header("View Content")
        
        # Sample content table
        data = {
            'Title': ['First Post', 'Second Post', 'Third Post'],
            'Category': ['Blog', 'News', 'Tutorial'],
            'Date': ['2024-03-11', '2024-03-10', '2024-03-09'],
            'Status': ['Published', 'Draft', 'Published']
        }
        df = pd.DataFrame(data)
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            category_filter = st.multiselect('Filter by Category', df['Category'].unique())
        with col2:
            status_filter = st.multiselect('Filter by Status', df['Status'].unique())
        
        # Apply filters
        filtered_df = df
        if category_filter:
            filtered_df = filtered_df[filtered_df['Category'].isin(category_filter)]
        if status_filter:
            filtered_df = filtered_df[filtered_df['Status'].isin(status_filter)]
            
        st.dataframe(filtered_df, use_container_width=True)

    elif page == "Settings":
        st.header("Settings")
        
        # Settings Form
        st.subheader("General Settings")
        site_name = st.text_input("Site Name", "My Website")
        theme = st.select_slider("Theme", options=["Light", "Dark", "Auto"])
        
        st.subheader("Notification Settings")
        email_notifications = st.toggle("Email Notifications")
        desktop_notifications = st.toggle("Desktop Notifications")
        
        if st.button("Save Settings"):
            st.success("Settings saved successfully!")

    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ by Muhammad Ismail")

if __name__ == '__main__':
    main()
