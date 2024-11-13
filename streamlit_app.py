import streamlit as st
import pandas as pd
import json
import base64
import uuid
from openai import OpenAI
from firecrawl import FirecrawlApp
import requests
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="NÄGELE AI Scraper",
    page_icon="favicon.ico",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .center-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
    }
    .app-header {
        color: #0066cc;
        font-weight: bold;
        margin-top: 0;
    }
    .stButton>button {
        width: 100%;
    }
    .output-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .logo-link {
        display: block;
        text-align: center;
        margin-bottom: 20px;
    }
    .logo-link:hover {
        opacity: 0.8;
    }
    </style>
""", unsafe_allow_html=True)

# Header section - replace the existing header section with this:
st.markdown('<div class="center-container">', unsafe_allow_html=True)

# Clickable logo
try:
    st.markdown(f"""
        <a href="https://www.naegele.law/onboarding" target="_blank" class="logo-link">
            <img src="data:image/png;base64,{base64.b64encode(open('Naegele_Rechtsanwaelte.png', 'rb').read()).decode()}" width="200">
        </a>
    """, unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Logo file 'Naegele_Rechtsanwaelte.png' not found. Please ensure the file is in the same directory as the app.")
except Exception as e:
    st.error(f"Error loading logo: {str(e)}")

# App title
st.markdown('<h1 class="app-header">🕸️ Web Scraper Pro</h1>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "scraped_data" not in st.session_state:
    st.session_state.scraped_data = None
if "error_message" not in st.session_state:
    st.session_state.error_message = None

# Sidebar - API Configuration
with st.sidebar:
    st.header("🔑 API Configuration")
    
    with st.expander("API Keys", expanded=True):
        firecrawl_api_key = st.text_input(
            "Firecrawl API Key",
            type="password",
            help="Enter your Firecrawl API key",
            key="firecrawl_key"
        )
        
        openai_api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key",
            key="openai_key"
        )

    st.divider()
    st.header("⚙️ Scraping Settings")
    
    fields = st.multiselect(
        "Select Fields to Extract",
        ["Document", "deadline", "Responsibility"],
        default=["Document", "deadline", "Responsibility"],
        help="Choose the fields you want to extract from the webpage"
    )

# Main content area
url = st.text_input(
    "🌐 Enter URL to Scrape",
    value="https://www.llv.li/en/national-administration/government-chancellery-unit/consultations/ongoing-consultations",
    help="Enter the full URL of the webpage you want to scrape"
)

# Function to download dataframe
def download_dataframe(df, file_format):
    # Debug info
    print(f"Preparing download for {len(df)} records")
    
    if file_format == 'csv':
        return df.to_csv(index=False, encoding='utf-8').encode('utf-8')
    else:  # xlsx
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Scraped Data')
        return buffer.getvalue()

def scrape_and_process():
    if not firecrawl_api_key or not openai_api_key:
        st.error("⚠️ Please provide both Firecrawl and OpenAI API keys in the sidebar.")
        return

    if not url:
        st.error("⚠️ Please provide a URL to scrape.")
        return

    try:
        with st.spinner("🕷️ Scraping webpage..."):
            # Initialize Firecrawl
            app = FirecrawlApp(api_key=firecrawl_api_key)
            page_content = app.scrape_url(url=url)

        with st.spinner("🤖 Processing with AI..."):
            # Initialize OpenAI
            client = OpenAI(api_key=openai_api_key)

            system_prompt = """
            You are a helpful assistant. You receive a scraped webpage, and you extract the items and return them in valid JSON. 
            Return a list with all fields. For 'Document' and 'Responsibility' include the URL as well.
            """

            user_prompt = f"""
            The extracted webpage: {page_content}
            The fields you return: {fields}
            """

            completion = client.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                temperature=0,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )

            data = json.loads(completion.choices[0].message.content)
            
            # Process the data
            items = []
            keys = list(data.keys())
            
            # If we have a nested structure, get the actual list
            if len(keys) == 1:
                data = data[keys[0]]
            
            # Ensure data is a list
            if isinstance(data, dict):
                items = [data]
            elif isinstance(data, list):
                items = data
            else:
                raise ValueError("Unexpected data format from API")

            # Create DataFrame and ensure all data is captured
            df = pd.DataFrame(items)
            st.session_state.scraped_data = df.copy()  # Make a copy to ensure data integrity
            
            # Debug information
            st.info(f"Total records found: {len(df)}")
            
            st.success("✅ Data successfully scraped and processed!")

    except requests.exceptions.HTTPError as e:
        st.error(f"⚠️ Error during scraping: {str(e)}")
    except Exception as e:
        st.error(f"⚠️ An error occurred: {str(e)}")

# Scrape button
if st.button("🕷️ Start Scraping", type="primary"):
    scrape_and_process()

# Display and download options
if st.session_state.scraped_data is not None:
    st.divider()
    st.subheader("📊 Results")
    
    with st.expander("Preview Data", expanded=True):
        st.dataframe(st.session_state.scraped_data)
        st.info(f"Total records in table: {len(st.session_state.scraped_data)}")

    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        csv_data = download_dataframe(st.session_state.scraped_data, 'csv')
        st.download_button(
            label=f"📥 Download CSV ({len(st.session_state.scraped_data)} records)",
            data=csv_data,
            file_name=f'scraped_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv',
        )
    
    with col2:
        excel_data = download_dataframe(st.session_state.scraped_data, 'xlsx')
        st.download_button(
            label=f"📥 Download Excel ({len(st.session_state.scraped_data)} records)",
            data=excel_data,
            file_name=f'scraped_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

# Footer
st.sidebar.divider()
st.sidebar.markdown("""
    <div style='text-align: center; color: #666;'>
        <small>Web Scraper Pro v1.0<br>
        </small>
    </div>
    """, 
    unsafe_allow_html=True
)