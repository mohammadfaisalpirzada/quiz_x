import streamlit as st
from components.layout import show_header, show_footer
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
MISSRUBA_PASSWORD = os.getenv("MISSRUBA_PASSWORD")
MISSREHANA_PASSWORD = os.getenv("MISSREHANA_PASSWORD")
MISSLUHNA_PASSWORD = os.getenv("MISSLUHNA_PASSWORD")
MISSNAHEED_PASSWORD = os.getenv("MISSNAHEED_PASSWORD")
MISSFATIMA_PASSWORD = os.getenv("MISSFATIMA_PASSWORD")
MISSASMA_PASSWORD = os.getenv("MISSASMA_PASSWORD")
MISSHUMA_PASSWORD = os.getenv("MISSHUMA_PASSWORD")
SIRSHAFQAT_PASSWORD = os.getenv("SIRSHAFQAT_PASSWORD")

# Function to authenticate user
def authenticate_user(user_id, password):
    if user_id == "Admin" and password == ADMIN_PASSWORD:
        return "subject_selection"  # Remove the pages/ prefix and .py extension
    elif user_id == "Miss Ruba" and password == MISSRUBA_PASSWORD:
        return "comp_quiz"  # Remove the pages/ prefix and .py extension
    elif user_id == "Miss Rehana" and password == MISSREHANA_PASSWORD:
        return "chemistry_quiz"  # Remove the pages/ prefix and .py extension
    elif user_id == "Miss Luhna" and password == MISSLUHNA_PASSWORD:
        return "pst_quiz"  # Remove the pages/ prefix and .py extension
    elif user_id == "Miss Naheed" and password == MISSNAHEED_PASSWORD:
        return "sindhi_quiz"  # Remove the pages/ prefix and .py extension
    elif user_id == "Miss Fatima" and password == MISSFATIMA_PASSWORD:
        return "english_quiz"  # Remove the pages/ prefix and .py extension
    elif user_id == "Miss Asma" and password == MISSASMA_PASSWORD:
        return "math_quiz"  # Remove the pages/ prefix and .py extension
    elif user_id == "Miss Huma" and password == MISSHUMA_PASSWORD:
        return "biology_quiz"  # Remove the pages/ prefix and .py extension
    elif user_id == "Sir Shafqat" and password == SIRSHAFQAT_PASSWORD:
        return "physics_quiz"  # Remove the pages/ prefix and .py extension
    return None

# Page settings
st.set_page_config(
    page_title="Quiz Test Program",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Show header
show_header()

# Welcome message
st.markdown(
    """
    <div style="text-align: center; margin-top: 20px;">
        <h1 style="margin: 0;">Welcome to the</h1>
        <h2 style="background-color: #1e88e5; color: white; padding: 10px; border-radius: 5px;">Quiz Program</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Login form
st.markdown("<div style='text-align: center; margin-top: 30px;'>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1], gap="medium")

# Initialize session state for entered password
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Dropdown for User ID
with col1:
    user_ids = ["Admin", "Miss Ruba", "Miss Rehana", "Miss Luhna", "Miss Naheed", "Miss Fatima", "Miss Asma", "Miss Huma", "Sir Shafqat"]
    user_id = st.selectbox("Select User ID", user_ids)

def handle_password_submit():
    st.session_state.submitted = True

# Function to handle login
def do_login(user_id, password):
    redirect_page = authenticate_user(user_id, password)
    if redirect_page:
        st.success("Login successful! Redirecting...")
        st.query_params["page"] = redirect_page
        if redirect_page == "subject_selection":
            st.switch_page("pages/subject_selection.py")
        elif redirect_page == "comp_quiz":
            st.switch_page("pages/comp_quiz.py")
        elif redirect_page == "chemistry_quiz":
            st.switch_page("pages/chemistry_quiz.py")
        elif redirect_page == "pst_quiz":
            st.switch_page("pages/pst_quiz.py")
        elif redirect_page == "sindhi_quiz":
            st.switch_page("pages/sindhi_quiz.py")
        elif redirect_page == "english_quiz":
            st.switch_page("pages/english_quiz.py")
        elif redirect_page == "math_quiz":
            st.switch_page("pages/math_quiz.py")
        elif redirect_page == "biology_quiz":
            st.switch_page("pages/biology_quiz.py")
        elif redirect_page == "physics_quiz":
            st.switch_page("pages/physics_quiz.py")
    else:
        st.error("Invalid credentials. Please try again.")

# Password input field with Enter key handling
with col2:
    password = st.text_input(
        "Password", 
        type="password",
        key="password",
        on_change=handle_password_submit
    )
    
    # Check if Enter was pressed (password submitted)
    if st.session_state.submitted:
        do_login(user_id, password)
        st.session_state.submitted = False

# Replace st.experimental_get_query_params and st.experimental_set_query_params with st.query_params
query_params = st.query_params
current_page = query_params.get("page", [None])[0]

# Replace the page switching logic
if current_page == "subject_selection":
    st.switch_page("pages/subject_selection.py")
elif current_page == "comp_quiz":
    st.switch_page("pages/comp_quiz.py")
elif current_page == "chemistry_quiz":
    st.switch_page("pages/chemistry_quiz.py")
elif current_page == "pst_quiz":
    st.switch_page("pages/pst_quiz.py")
elif current_page == "sindhi_quiz":
    st.switch_page("pages/sindhi_quiz.py")
elif current_page == "english_quiz":
    st.switch_page("pages/english_quiz.py")
elif current_page == "math_quiz":
    st.switch_page("pages/math_quiz.py")
elif current_page == "biology_quiz":
    st.switch_page("pages/biology_quiz.py")
elif current_page == "physics_quiz":
    st.switch_page("pages/physics_quiz.py")

# Login button
if st.button("Login"):
    do_login(user_id, password)

st.markdown("</div>", unsafe_allow_html=True)

# Show footer
show_footer()