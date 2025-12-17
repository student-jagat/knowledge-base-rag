import streamlit as st
import requests
import time

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Knowledge-Base Search", layout="wide", page_icon="🧠")

# --- Custom CSS for Animations & Styling ---
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Background - Deep Modern Gradient */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #ffffff;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Chat Messages - Glassmorphism */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transform-origin: bottom left;
        animation: fadeIn 0.5s ease-out forwards;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* User Message Specifics */
    div[data-testid="stChatMessage"] {
        background-color: transparent;
    }

    div[data-testid="stChatMessage"][data-test-role="user"] {
        background: rgba(60, 100, 255, 0.2) !important;
        border-left: 4px solid #4facfe;
    }
    
    div[data-testid="stChatMessage"][data-test-role="assistant"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border-left: 4px solid #00f2fe;
    }

    /* Header Styling */
    h1 {
        background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        text-shadow: 0 0 30px rgba(79, 172, 254, 0.5);
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5);
    }

    /* File Uploader */
    .stFileUploader {
        padding: 1rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border: 1px dashed rgba(255, 255, 255, 0.2);
    }

    /* Custom Loader */
    .loader-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }
    
    .quantum-spinner {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        border: 2px solid transparent;
        border-top-color: #00f2fe;
        border-bottom-color: #4facfe;
        animation: spin 1.5s linear infinite;
        position: relative;
        filter: drop-shadow(0 0 10px #00f2fe);
    }
    
    .quantum-spinner:before {
        content: '';
        position: absolute;
        top: 5px;
        left: 5px;
        right: 5px;
        bottom: 5px;
        border-radius: 50%;
        border: 2px solid transparent;
        border-left-color: #ffffff;
        border-right-color: #ffffff;
        animation: spin 3s linear infinite reverse;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

</style>
""", unsafe_allow_html=True)


# --- Application Layout ---

col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/6119/6119533.png", width=80) 
with col2:
    st.title("Knowledge-Base Search")

st.markdown("### 🤖 Ask questions from your documents")
st.divider()

# Sidebar for file upload
with st.sidebar:
    st.markdown("## 📂 Data Ingestion")
    st.markdown("Upload your knowledge base here.")
    
    uploaded_file = st.file_uploader("Choose a PDF or Text file", type=["pdf", "txt"], help="Supported formats: .pdf, .txt")
    
    if uploaded_file is not None:
        if st.button("🚀 Ingest Document", use_container_width=True):
            loader_placeholder = st.empty()
            loader_placeholder.markdown("""
                <div class="loader-container">
                    <div class="quantum-spinner"></div>
                </div>
            """, unsafe_allow_html=True)
            
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            try:
                response = requests.post(f"{API_URL}/ingest", files=files)
                loader_placeholder.empty() # Clear loader
                
                if response.status_code == 200:
                    st.balloons()
                    st.success(f"✅ Successfully absorbed: {uploaded_file.name}")
                else:
                    st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                loader_placeholder.empty()
                st.error(f"⚠️ Connection error: {e}")
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.info("Upload documents to give the AI context. Then ask any question related to them!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("✨ Ask me anything about your documents..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Custom Loader for Chat
        loader_placeholder = st.empty()
        loader_placeholder.markdown("""
            <div class="loader-container">
                <div class="quantum-spinner"></div>
            </div>
        """, unsafe_allow_html=True)
        
        try:
            response = requests.post(f"{API_URL}/query", json={"question": prompt})
            loader_placeholder.empty() # Clear loader
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "No answer found.")
                sources = data.get("sources", [])
                
                # Typing effect simulation
                for chunk in answer.split():
                    full_response += chunk + " "
                    time.sleep(0.02)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                
                # Show sources in a cool expander
                if sources:
                    with st.expander("📚 Source Documents"):
                        for s in sources:
                            st.markdown(f"- `{s}`")
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            else:
                error_msg = f"Error: {response.json().get('detail', 'Unknown error')}"
                message_placeholder.error(error_msg)
        except Exception as e:
            loader_placeholder.empty()
            message_placeholder.error(f"Connection error: {e}")
