from components.layout import show_header, show_footer
import streamlit as st

# Hide sidebar and menu
st.set_page_config(
    page_title="Subject Selection",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={}
)

# Hide Streamlit's default elements
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="collapsedControl"] {display: none !important;}
        header {display: none !important;}
        section[data-testid="stSidebarUserContent"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

show_header()

st.markdown("""
    <style>
        .subject-title {
            text-align: center;
            font-size: 30px;
            margin-top: 30px;
            margin-bottom: 40px;
            color: #004080;
        }
        .subject-buttons {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 18px;
        }
        .subject-button {
            width: 200px;
        }
        @media (max-width: 600px) {
            .subject-title { font-size: 22px; }
            .subject-button { width: 100%; }
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="subject-title">📚 Select a Subject</div>', unsafe_allow_html=True)

st.markdown('<div class="subject-buttons">', unsafe_allow_html=True)

# Create buttons for each subject
subjects = [
    "Biology",
    "Computer",
    "Sindhi",
    "English",
    "Chemistry",
    "Physics",
    "Pakistan Studies",
    "Mathematics"
]

subject_to_page = {

    
    "Biology": "pages/biology_quiz.py",
    "Computer": "pages/comp_quiz.py",
    "Sindhi": "pages/sindhi_quiz.py",
    "English": "pages/english_quiz.py",
    "Chemistry": "pages/chemistry_quiz.py",
    "Physics": "pages/physics_quiz.py",
    "Pakistan Studies": "pages/pst_quiz.py",
    "Mathematics": "pages/math_quiz.py"
}

for subject in subjects:
    if st.button(subject, key=subject, use_container_width=True):
        st.switch_page(subject_to_page[subject])

st.markdown('</div>', unsafe_allow_html=True)

show_footer()
