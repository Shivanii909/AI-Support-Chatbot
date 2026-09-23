import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
from datetime import datetime


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
COMPANY_NAME = os.getenv("COMPANY_NAME", "TechCorp")
SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", "support@company.com")


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title=f"{COMPANY_NAME} - AI Support",
    page_icon="🎧",
    layout="wide"
)


# =========================================================
# GEMINI API CONFIGURATION
# =========================================================

if not GOOGLE_API_KEY:
    st.error(
        "Google Gemini API key is missing. "
        "Please add GOOGLE_API_KEY to your .env file."
    )
    st.stop()


try:
    client = genai.Client(
        api_key=GOOGLE_API_KEY
    )
except Exception as e:
    st.error(f"Unable to initialize Gemini: {e}")
    st.stop()


MODEL_NAME = "gemini-3.6-flash"


# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = f"""
You are a helpful and professional customer support agent
for {COMPANY_NAME}.

Your responsibilities:

- Answer customer questions clearly and concisely.
- Be empathetic and understanding.
- Provide step-by-step solutions for technical issues.
- Offer product information and guidance.
- If you cannot resolve an issue, suggest escalating to a human agent.
- Always maintain a friendly and professional tone.
- Ask clarifying questions when needed.

Important guidelines:

- Never make promises you cannot keep.
- Admit when you don't know something.
- Always prioritize customer satisfaction.
- Keep responses concise but thorough.
- Use simple language and avoid unnecessary jargon.

If a customer seems frustrated or the issue is complex,
recommend contacting {SUPPORT_EMAIL} for personalized assistance.
"""


# =========================================================
# CUSTOM CSS - COMPLETE WHITE THEME
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       ENTIRE APPLICATION - PURE WHITE
    ===================================================== */

    html,
    body,
    .stApp,
    .main,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stHeader"],
    [data-testid="stMainBlockContainer"],
    .main .block-container {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
    }


    /* =====================================================
       MAIN PAGE
    ===================================================== */

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 8rem;
    }


    /* =====================================================
       HEADER
    ===================================================== */

    header[data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
    }

    [data-testid="stToolbar"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
    }


    /* =====================================================
       MAIN TEXT
    ===================================================== */

    .main .block-container p,
    .main .block-container span,
    .main .block-container label,
    .main .block-container h1,
    .main .block-container h2,
    .main .block-container h3,
    .main .block-container h4,
    .main .block-container h5,
    .main .block-container h6 {
        color: #111827 !important;
    }


    /* =====================================================
       MAIN HEADER
    ===================================================== */

    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #7C3AED !important;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: 0.5px;
    }


    .sub-header {
        text-align: center;
        color: #6B7280 !important;
        margin-bottom: 2rem;
        font-size: 1.05rem;
    }


    /* =====================================================
       SIDEBAR - PURE WHITE
    ===================================================== */

    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border-right: 1px solid #E5E7EB !important;
    }

    [data-testid="stSidebarContent"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
    }


    /* =====================================================
       SIDEBAR TEXT
    ===================================================== */

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] h6,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #111827 !important;
    }


    /* =====================================================
       SIDEBAR SELECT BOX
    ===================================================== */

    [data-testid="stSidebar"] [data-baseweb="select"],
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #111827 !important;
        border-radius: 10px !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] input {
        background-color: #FFFFFF !important;
        color: #111827 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] span {
        color: #111827 !important;
    }


    /* =====================================================
       BUTTONS - PURPLE
    ===================================================== */

    .stButton > button {
        background-color: #7C3AED !important;
        background: #7C3AED !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.55rem 1rem !important;
        font-weight: 600 !important;
        box-shadow: none !important;
    }

    .stButton > button p,
    .stButton > button span {
        color: #FFFFFF !important;
    }

    .stButton > button:hover {
        background-color: #6D28D9 !important;
        background: #6D28D9 !important;
        color: #FFFFFF !important;
    }


    /* =====================================================
       DOWNLOAD BUTTON
    ===================================================== */

    .stDownloadButton > button {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #111827 !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 10px !important;
    }

    .stDownloadButton > button p,
    .stDownloadButton > button span {
        color: #111827 !important;
    }


    /* =====================================================
       WELCOME / INFO BOX - WHITE
    ===================================================== */

    [data-testid="stAlert"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #111827 !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 14px !important;
        box-shadow: none !important;
    }

    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span,
    [data-testid="stAlert"] div {
        background: transparent !important;
        color: #111827 !important;
    }


    /* =====================================================
       CHAT MESSAGES - WHITE
    ===================================================== */

    [data-testid="stChatMessage"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 14px !important;
        padding: 0.8rem !important;
        margin-bottom: 0.7rem !important;
        box-shadow: none !important;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] span {
        color: #111827 !important;
    }


    /* =====================================================
       CHAT INPUT - OUTERMOST CONTAINER WHITE
    ===================================================== */

    /* Floating bottom area */
    [class*="stChatFloatingInputContainer"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: none !important;
        box-shadow: none !important;
    }


    /* Chat input parent containers */
    [data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 14px !important;
        box-shadow: none !important;
    }


    /* Every wrapper inside chat input */
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] > div > div,
    [data-testid="stChatInput"] > div > div > div,
    [data-testid="stChatInput"] form,
    [data-testid="stChatInput"] form > div,
    [data-testid="stChatInput"] form > div > div {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: none !important;
        box-shadow: none !important;
    }


    /* =====================================================
       BASEWEB CHAT INPUT
    ===================================================== */

    [data-testid="stChatInput"] [data-baseweb="base-input"],
    [data-testid="stChatInput"] [data-baseweb="base-input"] > div,
    [data-testid="stChatInput"] [data-baseweb="input"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: none !important;
        box-shadow: none !important;
    }


    /* =====================================================
       TEXT AREA - WHITE
    ===================================================== */

    [data-testid="stChatInput"] textarea {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #111827 !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        caret-color: #111827 !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #111827 !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #6B7280 !important;
        opacity: 1 !important;
    }


    /* =====================================================
       CHAT INPUT SEND BUTTON
    ===================================================== */

    [data-testid="stChatInput"] button {
        background-color: #7C3AED !important;
        background: #7C3AED !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: none !important;
    }

    [data-testid="stChatInput"] button:hover {
        background-color: #6D28D9 !important;
        background: #6D28D9 !important;
    }


    /* =====================================================
       CHAT INPUT SURROUNDING BOTTOM AREA
    ===================================================== */

    [data-testid="stBottom"],
    [data-testid="stBottomBlockContainer"],
    .stBottom,
    .stBottomBlockContainer {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: none !important;
        box-shadow: none !important;
    }


    /* =====================================================
       REMOVE SHADOW FROM CHAT INPUT
    ===================================================== */

    [data-testid="stChatInput"],
    [data-testid="stChatInput"] *,
    [class*="stChatFloatingInputContainer"] {
        box-shadow: none !important;
    }


    /* =====================================================
       DROPDOWN
    ===================================================== */

    [data-baseweb="popover"],
    [data-baseweb="menu"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
    }

    [role="option"] {
        background-color: #FFFFFF !important;
        color: #111827 !important;
    }

    [role="option"]:hover {
        background-color: #F3F4F6 !important;
        color: #111827 !important;
    }


    /* =====================================================
       SIDEBAR INFO
    ===================================================== */

    [data-testid="stSidebar"] [data-testid="stAlert"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #111827 !important;
        border: 1px solid #E5E7EB !important;
    }

    [data-testid="stSidebar"] [data-testid="stAlert"] p,
    [data-testid="stSidebar"] [data-testid="stAlert"] span,
    [data-testid="stSidebar"] [data-testid="stAlert"] div {
        color: #111827 !important;
    }


    /* =====================================================
       DIVIDERS
    ===================================================== */

    hr {
        border-color: #E5E7EB !important;
    }


    /* =====================================================
       SUCCESS MESSAGE
    ===================================================== */

    [data-testid="stNotification"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #111827 !important;
        border: 1px solid #E5E7EB !important;
    }

    [data-testid="stNotification"] p,
    [data-testid="stNotification"] span {
        color: #111827 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    f"""
    <div class="main-header">
        🎧 {COMPANY_NAME} AI Support
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="sub-header">
        Get instant help from our AI-powered assistant
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

if "satisfaction_rating" not in st.session_state:
    st.session_state.satisfaction_rating = None


# =========================================================
# GEMINI RESPONSE FUNCTION
# =========================================================

def get_ai_response(prompt):

    try:

        full_prompt = f"""
{SYSTEM_PROMPT}

Customer:
{prompt}
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=full_prompt
        )

        if response.text:
            return response.text

        return "I could not generate a response. Please try again."

    except Exception as e:

        return f"API_ERROR: {str(e)}"


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📋 Support Options")

    st.subheader("Quick Help Topics")

    quick_topics = [
        "Account Issues",
        "Billing Questions",
        "Technical Support",
        "Product Information",
        "Return & Refund"
    ]

    selected_topic = st.selectbox(
        "Select a topic:",
        [""] + quick_topics
    )


    # =====================================================
    # START CONVERSATION
    # =====================================================

    if selected_topic and st.button("🚀 Start Conversation"):

        prompt = f"I need help with: {selected_topic}"

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.spinner("Getting assistance..."):

            response_text = get_ai_response(prompt)

            if response_text.startswith("API_ERROR:"):

                error_details = response_text.replace(
                    "API_ERROR:",
                    ""
                ).strip()

                st.error(
                    f"Gemini API Error:\n\n{error_details}"
                )

                response_text = (
                    "I apologize, but I'm experiencing "
                    "technical difficulties. "
                    f"Please try again or contact "
                    f"{SUPPORT_EMAIL}."
                )

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": response_text
                }
            )

        st.rerun()


    st.markdown("---")


    # =====================================================
    # SESSION INFO
    # =====================================================

    st.subheader("📊 Session Info")

    st.info(
        f"**Session ID:** "
        f"{st.session_state.session_id}"
    )

    st.info(
        f"**Messages:** "
        f"{len(st.session_state.chat_history)}"
    )


    # =====================================================
    # NEW CONVERSATION
    # =====================================================

    if st.button("🔄 New Conversation"):

        st.session_state.chat_history = []

        st.session_state.session_id = (
            datetime.now().strftime("%Y%m%d_%H%M%S")
        )

        st.session_state.satisfaction_rating = None

        st.rerun()


    st.markdown("---")


    # =====================================================
    # CONTACT INFORMATION
    # =====================================================

    st.subheader("📞 Need More Help?")

    st.write(
        f"**Email:** {SUPPORT_EMAIL}"
    )

    st.write(
        "**Hours:** Mon-Fri, 9AM-6PM"
    )


    # =====================================================
    # EXPORT CHAT
    # =====================================================

    if len(st.session_state.chat_history) > 0:

        st.markdown("---")

        chat_export = (
            f"Support Chat - "
            f"{st.session_state.session_id}\n\n"
        )

        for msg in st.session_state.chat_history:

            role = (
                "Customer"
                if msg["role"] == "user"
                else "Agent"
            )

            chat_export += (
                f"{role}: "
                f"{msg['content']}\n\n"
            )

        st.download_button(
            label="📥 Export Conversation",
            data=chat_export,
            file_name=(
                f"support_chat_"
                f"{st.session_state.session_id}.txt"
            ),
            mime="text/plain"
        )


# =========================================================
# MAIN CHAT AREA
# =========================================================

st.markdown("---")


# =========================================================
# WELCOME MESSAGE
# =========================================================

if len(st.session_state.chat_history) == 0:

    st.info(
        f"""
👋 **Welcome to {COMPANY_NAME} Support!**

I'm your AI assistant, here to help you with:

• Account and billing questions  
• Technical troubleshooting  
• Product information and recommendations  
• Order status and shipping  
• Returns and refunds  

**How can I help you today?**
"""
    )


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# =========================================================
# USER INPUT
# =========================================================

user_input = st.chat_input(
    "Type your question here..."
)


# =========================================================
# PROCESS USER INPUT
# =========================================================

if user_input:

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):

        st.write(user_input)


    # =====================================================
    # AI RESPONSE
    # =====================================================

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            conversation_context = (
                SYSTEM_PROMPT
                + "\n\nConversation history:\n"
            )


            # Use last 6 messages

            for msg in st.session_state.chat_history[-6:]:

                role = (
                    "Customer"
                    if msg["role"] == "user"
                    else "Support Agent"
                )

                conversation_context += (
                    f"{role}: "
                    f"{msg['content']}\n"
                )


            try:

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=conversation_context
                )


                if response.text:

                    response_text = response.text

                else:

                    response_text = (
                        "I could not generate a response. "
                        "Please try again."
                    )


                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": response_text
                    }
                )


                st.write(response_text)


            except Exception as e:

                st.error(
                    f"Gemini API Error:\n\n{str(e)}"
                )


                error_msg = (
                    "I apologize, but I'm experiencing "
                    "technical difficulties.\n\n"
                    f"Please try again or contact "
                    f"{SUPPORT_EMAIL} for immediate assistance."
                )


                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": error_msg
                    }
                )


# =========================================================
# SATISFACTION SURVEY
# =========================================================

if (
    len(st.session_state.chat_history) >= 4
    and st.session_state.satisfaction_rating is None
):

    st.markdown("---")

    st.subheader(
        "📊 How satisfied are you with the support?"
    )

    col1, col2, col3, col4, col5 = st.columns(5)


    with col1:

        if st.button("😞 Very Unsatisfied"):

            st.session_state.satisfaction_rating = 1
            st.rerun()


    with col2:

        if st.button("😕 Unsatisfied"):

            st.session_state.satisfaction_rating = 2
            st.rerun()


    with col3:

        if st.button("😐 Neutral"):

            st.session_state.satisfaction_rating = 3
            st.rerun()


    with col4:

        if st.button("🙂 Satisfied"):

            st.session_state.satisfaction_rating = 4
            st.rerun()


    with col5:

        if st.button("😄 Very Satisfied"):

            st.session_state.satisfaction_rating = 5
            st.rerun()


# =========================================================
# THANK YOU MESSAGE
# =========================================================

if st.session_state.satisfaction_rating is not None:

    st.success(
        "Thank you for your feedback! "
        "Your rating helps us improve our service."
    )