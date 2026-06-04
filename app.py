import streamlit as st
import os
from main import run_pipeline, ask_question

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS Injection ---
def inject_custom_css():
    st.markdown("""
        <style>
            /* Base Theme overrides for Dark Theme */
            .stApp {
                background-color: #0f172a;
                color: #ffffff;
            }
            
            /* Glassmorphism Cards */
            .glass-card {
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 24px;
                margin-bottom: 24px;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            .glass-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
            }
            
            /* Gradient Accents */
            .gradient-text {
                background: linear-gradient(135deg, #3b82f6, #8b5cf6, #06b6d4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: 800;
            }
            
            /* Typography & Colors */
            h1, h2, h3, h4, h5, h6 {
                color: #ffffff !important;
                font-family: 'Inter', sans-serif;
            }
            p, span, div, li {
                color: #cbd5e1;
            }
            
            /* Checklists & Timelines */
            .action-item {
                display: flex;
                align-items: flex-start;
                margin-bottom: 12px;
                line-height: 1.5;
            }
            .action-item::before {
                content: '✅';
                margin-right: 12px;
            }
            
            .timeline-item {
                padding-left: 20px;
                border-left: 2px solid #8b5cf6;
                margin-bottom: 16px;
                position: relative;
                line-height: 1.5;
            }
            .timeline-item::before {
                content: '';
                position: absolute;
                left: -6px;
                top: 6px;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: #06b6d4;
            }
            
            .tag {
                display: inline-block;
                background: rgba(59, 130, 246, 0.15);
                color: #3b82f6;
                padding: 6px 14px;
                border-radius: 20px;
                margin: 6px;
                font-size: 14px;
                font-weight: 500;
                border: 1px solid rgba(59, 130, 246, 0.3);
                transition: all 0.2s ease;
            }
            .tag:hover {
                background: rgba(59, 130, 246, 0.25);
            }
            
            /* Metrics Override */
            [data-testid="stMetricValue"] {
                color: #3b82f6 !important;
            }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# --- Session State Initialization ---
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- Header & Hero Section ---
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'><span class='gradient-text'>✨ AI Video Assistant</span></h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-top: 10px;'>Transform Videos Into Actionable Insights</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; max-width: 800px; margin: 0 auto; margin-bottom: 40px;'>Upload a local video/audio file or paste a YouTube URL. Our AI extracts transcripts, summarizes content, captures action items, and lets you chat dynamically with your video.</p>", unsafe_allow_html=True)

# --- Input Section ---
st.markdown("### 📥 Input Source")
input_col1, input_col2 = st.columns(2)

with input_col1:
    youtube_url = st.text_input("Paste YouTube URL", placeholder="https://youtube.com/watch?v=...")
with input_col2:
    uploaded_file = st.file_uploader("Or Upload Video/Audio", type=["mp4", "mkv", "mov", "wav", "mp3"])

analyze_btn = st.button("🚀 Analyze Content", use_container_width=True, type="primary")

if analyze_btn:
    if not youtube_url and not uploaded_file:
        st.warning("⚠️ Please provide a YouTube URL or upload a file.")
    else:
        source_path = None
        temp_dir = "temp"
        
        # Determine source
        if youtube_url:
            source_path = youtube_url
        elif uploaded_file:
            # Create temp dir if not exists
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            
            # Save uploaded file to disk
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            source_path = file_path

        if source_path:
            with st.spinner("Processing video... This may take a few minutes. Grab a coffee ☕"):
                try:
                    result = run_pipeline(source_path)
                    st.session_state.processed_data = result
                    # Clear chat history when new video is loaded
                    st.session_state.messages = [{"role": "assistant", "content": "Hello! I have indexed the video transcript. Ask me anything!"}]
                    st.success("✅ Analysis Complete!")
                except Exception as e:
                    st.error(f"Error processing video: {str(e)}")
                finally:
                    # Clean up temp file
                    if uploaded_file and os.path.exists(source_path):
                        os.remove(source_path)

# --- Results Dashboard ---
if st.session_state.processed_data:
    data = st.session_state.processed_data
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("<h2 class='gradient-text'>📊 Analysis Dashboard</h2>", unsafe_allow_html=True)
    
    # Card 1: Generated Title
    st.markdown(f"""
        <div class="glass-card">
            <h4 style="color:#8b5cf6; margin-top:0;">Generated Title</h4>
            <h2 style="margin-bottom:0;">{data.get('title', 'Untitled Video')}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # --- Analytics Section ---
    st.markdown("### 📈 Key Metrics")
    m1, m2, m3, m4, m5 = st.columns(5)
    
    # Safely parse lists from text
    transcript_text = data.get('transcript', '')
    word_count = len(transcript_text.split())
    action_items_list = [i for i in data.get('action_items', '').split('\n') if i.strip()]
    decisions_list = [i for i in data.get('key_decisions', '').split('\n') if i.strip()]
    questions_list = [i for i in data.get('open_questions', '').split('\n') if i.strip()]
    
    m1.metric("Transcript Length", f"{len(transcript_text):,} chars")
    m2.metric("Word Count", f"{word_count:,} words")
    m3.metric("Action Items", len(action_items_list))
    m4.metric("Key Decisions", len(decisions_list))
    m5.metric("Open Questions", len(questions_list))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 1 Cards: Summary & Action Items
    col1, col2 = st.columns(2)
    
    with col1:
        # Card 2: AI Summary
        st.markdown(f"""
            <div class="glass-card" style="height: 100%;">
                <h4 style="color:#06b6d4; margin-top:0;">📝 AI Summary</h4>
                <p style="line-height: 1.7;">{data.get('summary', '').replace(chr(10), '<br>')}</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        # Card 3: Action Items
        action_html = "".join([f"<div class='action-item'>{item.replace('- ', '').replace('* ', '')}</div>" for item in action_items_list])
        if not action_html:
            action_html = "<p>No action items detected.</p>"
        st.markdown(f"""
            <div class="glass-card" style="height: 100%;">
                <h4 style="color:#3b82f6; margin-top:0;">✅ Action Items</h4>
                <div style="margin-top: 15px;">{action_html}</div>
            </div>
        """, unsafe_allow_html=True)

    # Row 2 Cards: Decisions & Questions
    col3, col4 = st.columns(2)
    
    with col3:
        # Card 4: Key Decisions
        timeline_html = "".join([f"<div class='timeline-item'>{item.replace('- ', '').replace('* ', '')}</div>" for item in decisions_list])
        if not timeline_html:
            timeline_html = "<p>No key decisions detected.</p>"
        st.markdown(f"""
            <div class="glass-card" style="height: 100%;">
                <h4 style="color:#8b5cf6; margin-top:0;">🔑 Key Decisions</h4>
                <div style="margin-top: 15px;">{timeline_html}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col4:
        # Card 5: Open Questions
        tags_html = "".join([f"<span class='tag'>{item.replace('- ', '').replace('* ', '')}</span>" for item in questions_list])
        if not tags_html:
            tags_html = "<p>No open questions detected.</p>"
        st.markdown(f"""
            <div class="glass-card" style="height: 100%;">
                <h4 style="color:#06b6d4; margin-top:0;">❓ Open Questions</h4>
                <div style="margin-top: 15px; display: flex; flex-wrap: wrap;">{tags_html}</div>
            </div>
        """, unsafe_allow_html=True)

    # Card 6: Full Transcript
    with st.expander("📄 View Full Transcript"):
        search_query = st.text_input("🔍 Search Transcript", placeholder="Type a keyword to highlight...")
        display_transcript = transcript_text
        
        if search_query:
            # Highlight keyword case-insensitively (simple replace for demo)
            # A more robust solution would use regex to preserve original casing, but this works well for basic needs.
            import re
            pattern = re.compile(re.escape(search_query), re.IGNORECASE)
            display_transcript = pattern.sub(lambda m: f"<span style='background-color:#3b82f6; color:#ffffff; padding:2px 4px; border-radius:4px;'>{m.group(0)}</span>", display_transcript)
            
        st.markdown(f"""
            <div style="background:rgba(0,0,0,0.2); padding:20px; border-radius:12px; height:400px; overflow-y:auto; line-height:1.7;">
                {display_transcript.replace(chr(10), '<br>')}
            </div>
        """, unsafe_allow_html=True)
        
        # Native Streamlit code block for easy copying
        st.markdown("<p style='margin-top: 10px; font-size: 14px;'>Use the button below to copy the raw text:</p>", unsafe_allow_html=True)
        st.code(transcript_text, language="text")

    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 40px 0;'>", unsafe_allow_html=True)

    # --- AI Chat Section ---
    st.markdown("<h2 class='gradient-text'>💬 Chat with the Video</h2>", unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns([10, 1])
    with col_c2:
        if st.button("🧹 Clear Chat", help="Clear conversation history"):
            st.session_state.messages = [{"role": "assistant", "content": "Hello! I have indexed the video transcript. Ask me anything!"}]
            st.rerun()
            
    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Chat Input Box
    if prompt := st.chat_input("Ask a question about the video..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = ask_question(data["rag_chain"], prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error getting answer: {e}")
