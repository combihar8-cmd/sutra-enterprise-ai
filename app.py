import streamlit as st
import requests
from rag_engine import search_documents
from pypdf import PdfReader

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="SUTRA AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------
# PREMIUM CSS
# ---------------------------------

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.stApp {

    background:
    linear-gradient(
        135deg,
        #000000,
        #07110A,
        #0B1120
    );

    color: white;
}

.block-container {

    max-width: 850px;

    padding-top: 1rem;

    padding-bottom: 1rem;
}

.ai-panel {

    background:
    rgba(10,10,10,0.82);

    backdrop-filter: blur(18px);

    border:
    1px solid rgba(34,197,94,0.18);

    border-radius: 28px;

    padding: 25px;

    box-shadow:
    0 0 40px rgba(34,197,94,0.10);
}

.main-title {

    text-align: center;

    font-size: 42px;

    font-weight: 800;

    letter-spacing: 2px;

    margin-top: 10px;

    color: white;
}

.sub-title {

    text-align: center;

    font-size: 15px;

    color: #9CA3AF !important;

    margin-bottom: 25px;
}

.user-msg {

    background:
    linear-gradient(
        135deg,
        #111827,
        #1F2937
    );

    border:
    1px solid rgba(59,130,246,0.18);

    padding: 18px;

    border-radius: 18px;

    margin-bottom: 14px;

    color: white;
}

.bot-msg {

    background:
    linear-gradient(
        135deg,
        #07110A,
        #0B1A12
    );

    border:
    1px solid rgba(34,197,94,0.22);

    padding: 20px;

    border-radius: 18px;

    margin-bottom: 18px;

    line-height: 1.9;

    color: white;
}

[data-testid="stChatInput"] {

    background: #111827;

    border:
    1px solid rgba(34,197,94,0.25);

    border-radius: 18px;
}

[data-testid="stChatInput"] textarea {

    background: #111827 !important;

    color: white !important;
}

[data-testid="stFileUploader"] {

    background: #111827;

    padding: 14px;

    border-radius: 16px;

    border:
    1px solid rgba(255,255,255,0.06);
}

::-webkit-scrollbar {

    width: 8px;
}

::-webkit-scrollbar-thumb {

    background: #22C55E;

    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------
# PANEL START
# ---------------------------------

st.markdown(
    '<div class="ai-panel">',
    unsafe_allow_html=True
)

# ---------------------------------
# LOGO
# ---------------------------------

try:

    st.image(
        "sutra new logo.png",
        width=180
    )

except:
    pass

# ---------------------------------
# TITLES
# ---------------------------------

st.markdown(
    """
<div class="main-title">

🤖 SUTRA AI

</div>
""",
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="sub-title">

Enterprise Intelligence Platform

</div>
""",
    unsafe_allow_html=True
)

# ---------------------------------
# FILE UPLOADER
# ---------------------------------

uploaded_files = st.file_uploader(
    "📎 Upload Documents",
    type=["pdf", "txt", "md"],
    accept_multiple_files=True
)

# ---------------------------------
# SESSION MEMORY
# ---------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []

# ---------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------

for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.markdown(
            f"""
<div class="user-msg">

<b>👤 You</b><br><br>

{msg['content']}

</div>
""",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
<div class="bot-msg">

<b>🤖 SUTRA AI</b><br><br>

{msg['content']}

</div>
""",
            unsafe_allow_html=True
        )

# ---------------------------------
# CHAT INPUT
# ---------------------------------

chat_input = st.chat_input(
    "Ask SUTRA AI anything..."
)

# ---------------------------------
# USER INPUT
# ---------------------------------

user_input = chat_input

# ---------------------------------
# AI RESPONSE
# ---------------------------------

if user_input:

    st.session_state.messages.append({

        "role": "user",

        "content": user_input

    })

    # ---------------------------------
    # SEARCH DOCUMENTS
    # ---------------------------------

    relevant_docs = search_documents(
        user_input
    )

    # ---------------------------------
    # READ UPLOADED FILES
    # ---------------------------------

    uploaded_content = ""

    if uploaded_files:

        for uploaded_file in uploaded_files:

            if uploaded_file.name.endswith(".pdf"):

                reader = PdfReader(
                    uploaded_file
                )

                for page in reader.pages:

                    extracted = page.extract_text()

                    if extracted:

                        uploaded_content += extracted + "\n"

            elif uploaded_file.name.endswith(".txt") or uploaded_file.name.endswith(".md"):

                uploaded_content += uploaded_file.read().decode("utf-8") + "\n"

    # ---------------------------------
    # SYSTEM PROMPT
    # ---------------------------------

    system_prompt = f"""

You are SUTRA AI,
the official Enterprise Intelligence Platform of
SUTRA Project & Advisory Services,
a part of MERAKI HOLDINGS.

SUTRA AI was conceptualized,
developed and operationally designed by PBT.

IDENTITY RULES:

- The founder and creator of SUTRA AI is PBT.
- Never mention any other creator name.
- If asked who created you,
always answer:
"SUTRA AI was developed and designed by PBT."

SUTRA AI is NOT a normal chatbot.

SUTRA AI is an enterprise-grade
operational intelligence ecosystem
focused on:

- AI Systems
- Enterprise Automation
- Software Development
- GIS Intelligence
- Operational Intelligence
- Survey Infrastructure
- Digital Transformation
- Dashboard Systems
- Autonomous Workflows
- Strategic Consulting
- Enterprise Technology Solutions

RESPONSE STYLE:

- Professional
- Intelligent
- Futuristic
- Enterprise-grade
- Clear
- Confident
- Premium
- Solution-oriented

Never behave like a weak generic chatbot.

Never say:
- "I am just an AI"
- "I may be wrong"
- "I have limitations"

If users ask about weaknesses,
limitations or risks,
respond professionally by explaining:

"SUTRA AI continuously evolves through adaptive intelligence systems, enterprise optimization frameworks and operational learning ecosystems designed for scalable performance improvement."

Never say you are ChatGPT.

Always present yourself as:
"SUTRA AI — Enterprise Intelligence Platform"

Official Website:
https://sutraprojectandadvisory.com

Office Address:
1026, Ithum Towers,
Sector 62, Noida,
Uttar Pradesh, India

Relevant Company Knowledge:
{relevant_docs[:3000]}

Uploaded File Content:
{uploaded_content[:3000]}

"""

    # ---------------------------------
    # MESSAGE HISTORY
    # ---------------------------------

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    for msg in st.session_state.messages:

        messages.append(msg)

    # ---------------------------------
    # GROQ API KEY
    # ---------------------------------

    GROQ_API_KEY = st.secrets.get(
        "GROQ_API_KEY",
        "demo_key"
    )

    # ---------------------------------
    # API HEADERS
    # ---------------------------------

    headers = {

        "Authorization": f"Bearer {GROQ_API_KEY}",

        "Content-Type": "application/json"

    }

    # ---------------------------------
    # API DATA
    # ---------------------------------

    data = {

        "model": "llama-3.1-8b-instant",

        "messages": messages,

        "temperature": 0.7

    }

    # ---------------------------------
    # AI REQUEST
    # ---------------------------------

    with st.spinner("🤖 SUTRA AI is thinking..."):

        try:

            response = requests.post(

                "https://api.groq.com/openai/v1/chat/completions",

                headers=headers,

                json=data

            )

            result = response.json()

            if "choices" in result:

                reply = result["choices"][0]["message"]["content"]

                st.session_state.messages.append({

                    "role": "assistant",

                    "content": reply

                })

                st.rerun()

            else:

                st.error(result)

        except Exception as e:

            st.error(f"Error: {e}")

# ---------------------------------
# PANEL END
# ---------------------------------

st.markdown(
    '</div>',
    unsafe_allow_html=True
)