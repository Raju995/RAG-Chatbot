import streamlit as st
import requests
import uuid

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
API_BASE_URL = "http://localhost:8000/api"

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("📄 RAG PDF Chatbot")

# --------------------------------------------------
# SESSION MANAGEMENT
# --------------------------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# ADD THIS: Track uploaded file state
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False
if "current_file_name" not in st.session_state:
    st.session_state.current_file_name = None

# --------------------------------------------------
# SIDEBAR - PDF Upload (FIXED)
# --------------------------------------------------
st.sidebar.header("Upload PDF")

uploaded_file = st.sidebar.file_uploader(
    "Upload your PDF",
    type=["pdf"],
    key="pdf_uploader"  # Critical: Add unique key to track state
)

# ONLY PROCESS NEW UPLOADS
if uploaded_file and (
    # New file selected OR different file than last upload
    st.session_state.current_file_name != uploaded_file.name or
    # Force re-upload if previous upload failed
    not st.session_state.file_uploaded
):
    with st.sidebar:
        with st.spinner("Uploading and processing..."):
            try:
                # Reset upload state for new attempt
                st.session_state.file_uploaded = False
                
                response = requests.post(
                    f"{API_BASE_URL}/upload",
                    files={"file": uploaded_file}
                )

                if response.status_code == 200:
                    st.success("PDF processed successfully!")
                    # Track successful upload
                    st.session_state.file_uploaded = True
                    st.session_state.current_file_name = uploaded_file.name
                    # Clear chat history for new document
                    st.session_state.messages = []
                else:
                    st.error(f"Upload failed: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

# Show upload status
if st.session_state.file_uploaded:
    st.sidebar.success(f"✅ Using: {st.session_state.current_file_name}")
elif st.session_state.current_file_name:
    st.sidebar.warning("⚠️ Upload pending...")

# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------
user_input = st.chat_input("Ask a question about your document...")

if user_input:
    # Validate document is uploaded
    if not st.session_state.file_uploaded:
        st.error("Please upload a PDF first!")
        st.stop()
    
    # Show user message instantly
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send to backend
    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                f"{API_BASE_URL}/chat",
                json={
                    "question": user_input,
                    "session_id": st.session_state.session_id
                }
            )
            response.raise_for_status()  # Check for HTTP errors
            answer = response.json()["response"]
        except Exception as e:
            answer = f"⚠️ Error: {str(e)}"

    # Show assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
    with st.chat_message("assistant"):
        st.markdown(answer)