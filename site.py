import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime
import re
import ssl
import socket
from urllib.robotparser import RobotFileParser
import whois
import tld
from PIL import Image
import io

def check_ssl(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                return {
                    'status': 'Valid',
                    'expiry': expiry_date.strftime('%Y-%m-%d'),
                    'issuer': dict(x[0] for x in cert['issuer'])['organizationName']
                }
    except Exception as e:
        return {'status': 'Invalid/Not Found', 'expiry': 'N/A', 'issuer': 'N/A'}

def analyze_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Basic SEO Checks
        title = soup.title.string if soup.title else 'No title found'
        meta_desc = soup.find('meta', {'name': 'description'})
        meta_desc = meta_desc['content'] if meta_desc else 'No meta description found'
        
        # Get all headings
        headings = {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 7)}
        
        # Get all images and check alt text
        images = soup.find_all('img')
        images_without_alt = len([img for img in images if not img.get('alt')])
        
        # Check internal and external links
        links = soup.find_all('a')
        base_domain = urllib.parse.urlparse(url).netloc
        internal_links = len([link for link in links if link.get('href') and base_domain in link.get('href', '')])
        external_links = len([link for link in links if link.get('href') and base_domain not in link.get('href', '')])
        
        # Page size and load time
        page_size = len(response.content) / 1024  # in KB
        load_time = response.elapsed.total_seconds()
        
        return {
            'status_code': response.status_code,
            'title': title,
            'meta_description': meta_desc,
            'headings': headings,
            'total_images': len(images),
            'images_without_alt': images_without_alt,
            'internal_links': internal_links,
            'external_links': external_links,
            'page_size': round(page_size, 2),
            'load_time': round(load_time, 2),
            'content_type': response.headers.get('content-type', 'Not specified')
        }
    except Exception as e:
        return {'error': str(e)}

def main():
    st.set_page_config(page_title="Website Audit Tool", layout="wide")
    
    st.title("🔍 Website Audit Tool")
    st.write("Enter a website URL to perform a comprehensive audit")
    
    url = st.text_input("Enter Website URL", "")
    
    if st.button("Analyze Website"):
        if url:
            with st.spinner("Analyzing website..."):
                # Parse URL
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                
                domain = urllib.parse.urlparse(url).netloc
                
                # Create tabs for different analysis sections
                tab1, tab2, tab3, tab4 = st.tabs(["SEO Analysis", "Technical Analysis", "Security", "Performance"])
                
                # Get analysis results
                results = analyze_page(url)
                ssl_info = check_ssl(domain)
                
                # SEO Analysis Tab
                with tab1:
                    st.header("SEO Analysis")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Title Tag")
                        st.write(results['title'])
                        title_length = len(results['title']) if results['title'] != 'No title found' else 0
                        if title_length < 30:
                            st.warning("Title is too short (< 30 characters)")
                        elif title_length > 60:
                            st.warning("Title is too long (> 60 characters)")
                        else:
                            st.success("Title length is optimal")
                    
                    with col2:
                        st.subheader("Meta Description")
                        st.write(results['meta_description'])
                        meta_length = len(results['meta_description']) if results['meta_description'] != 'No meta description found' else 0
                        if meta_length < 120:
                            st.warning("Meta description is too short (< 120 characters)")
                        elif meta_length > 160:
                            st.warning("Meta description is too long (> 160 characters)")
                        else:
                            st.success("Meta description length is optimal")
                    
                    st.subheader("Heading Structure")
                    for h, count in results['headings'].items():
                        st.write(f"{h}: {count}")
                    
                    st.subheader("Links Analysis")
                    col3, col4 = st.columns(2)
                    with col3:
                        st.metric("Internal Links", results['internal_links'])
                    with col4:
                        st.metric("External Links", results['external_links'])
                
                # Technical Analysis Tab
                with tab2:
                    st.header("Technical Analysis")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Status Code", results['status_code'])
                    with col2:
                        st.metric("Page Size (KB)", results['page_size'])
                    with col3:
                        st.metric("Load Time (s)", results['load_time'])
                    
                    st.subheader("Images")
                    st.write(f"Total Images: {results['total_images']}")
                    st.write(f"Images without alt text: {results['images_without_alt']}")
                    
                    st.subheader("Content Type")
                    st.write(results['content_type'])
                
                # Security Tab
                with tab3:
                    st.header("Security Analysis")
                    
                    st.subheader("SSL Certificate")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Status", ssl_info['status'])
                    with col2:
                        st.metric("Expiry Date", ssl_info['expiry'])
                    with col3:
                        st.metric("Issuer", ssl_info['issuer'])
                
                # Performance Tab
                with tab4:
                    st.header("Performance Metrics")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Load Time", f"{results['load_time']}s")
                        if results['load_time'] < 2:
                            st.success("Good load time (< 2s)")
                        elif results['load_time'] < 4:
                            st.warning("Average load time (2-4s)")
                        else:
                            st.error("Slow load time (> 4s)")
                    
                    with col2:
                        st.metric("Page Size", f"{results['page_size']} KB")
                        if results['page_size'] < 1000:
                            st.success("Good page size (< 1000KB)")
                        elif results['page_size'] < 2000:
                            st.warning("Average page size (1000-2000KB)")
                        else:
                            st.error("Large page size (> 2000KB)")

if __name__ == "__main__":
    main()
