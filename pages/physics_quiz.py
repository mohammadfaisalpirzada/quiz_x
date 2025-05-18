import streamlit as st
from components.layout import show_header
import pandas as pd
import random
from datetime import datetime
import os
import re

# Set page config
st.set_page_config(
    page_title="Physics Quiz",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Use the header component
show_header()

# Custom CSS for student info and timer
st.markdown("""
<style>
    .info-container-inline {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 30px;
        background-color: #f9f9f9;
        padding: 15px 25px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 5px solid #1e88e5;
        font-size: 1.1rem;
        font-family: Arial, sans-serif;
        text-align: center;
    }
    .info-label {
        font-weight: bold;
        color: #1e88e5;
        margin-right: 5px;
    }
    .timer-container {
        background-color: #ff5722;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 0 auto 20px auto;
        text-align: center;
        max-width: 300px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Update the header component to show student name and a dummy picture after login
def update_header_with_student_info():
    if 'std_name' in st.session_state and st.session_state.std_name:
        st.markdown(f"""
        <style>
            .custom-header .header-right {{
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .custom-header .header-right img {{
                width: 40px;
                height: 40px;
                border-radius: 50%;
                object-fit: cover;
                border: 2px solid #1e88e5;
            }}
            .custom-header .header-right span {{
                font-size: 16px;
                font-weight: bold;
                color: #1e88e5;
            }}
        </style>
        <script>
            const headerRight = document.querySelector('.custom-header .header-right');
            if (headerRight) {{
                headerRight.innerHTML = `
                    <img src="https://via.placeholder.com/40" alt="Student Picture">
                    <span>{st.session_state.std_name}</span>
                `;
            }}
        </script>
        """, unsafe_allow_html=True)

# Function to load quiz data from Excel file
def load_quiz_data(file_name, sheet_name=None):
    try:
        # Get all available sheets first
        excel_file = pd.ExcelFile(file_name)
        available_sheets = excel_file.sheet_names
        
        # If the specific sheet name isn't provided or isn't found, use the first available sheet
        if sheet_name is None or sheet_name not in available_sheets:
            if available_sheets:
                sheet_name = available_sheets[0]
            else:
                st.error("No sheets found in the Excel file")
                return None
        
        # Load the data from the selected sheet
        df = pd.read_excel(file_name, sheet_name=sheet_name)
        
        # Strip any leading/trailing spaces from column names
        df.columns = df.columns.str.strip()
        
        return df
    except Exception as e:
        st.error(f"Error loading quiz data: {str(e)}")
        return None

# Function to check if input is valid text (no numbers or special characters)
def is_valid_name(name):
    # Allow letters, spaces, and some special characters used in names
    pattern = r'^[A-Za-z\s\'\-\.]+$'
    return bool(re.match(pattern, name))

# Function to check if input is a valid roll number (numbers only)
def is_valid_roll_number(roll_num):
    pattern = r'^\d+$'
    return bool(re.match(pattern, roll_num))

# Function to check if student has already taken the quiz
def check_student_attempt(roll_num):
    score_file = "physics_score.xlsx"
    
    try:
        if os.path.exists(score_file):
            scores_df = pd.read_excel(score_file)
            
            # Check if roll number exists in the scores dataframe
            if 'roll_num' in scores_df.columns and roll_num in scores_df['roll_num'].astype(str).values:
                return True
        
        return False
    except Exception as e:
        st.error(f"Error checking previous attempts: {str(e)}")
        return False

# Function to save score to Excel file
def save_score(std_name, f_name, roll_num, question_attemp, score):
    try:
        score_file = "physics_score.xlsx"
        
        # Create new score record
        new_record = pd.DataFrame({
            "sno": [1],  # Default to 1, will update if existing records found
            "roll_num": [roll_num],
            "std_name": [std_name],
            "f_name": [f_name],
            "question_attemp": [question_attemp],
            "score": [score],
            "date_time": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        })
        
        try:
            # Check if score file exists
            if os.path.exists(score_file):
                try:
                    # Try to read the existing scores
                    existing_scores = pd.read_excel(score_file)
                    
                    # Update serial number
                    if not existing_scores.empty and 'sno' in existing_scores.columns:
                        new_record["sno"] = existing_scores["sno"].max() + 1
                    
                    # Combine existing scores with new record
                    combined_scores = pd.concat([existing_scores, new_record], ignore_index=True)
                    
                    # Write back to Excel
                    try:
                        combined_scores.to_excel(score_file, index=False)
                        return True
                    except Exception as write_err:
                        # If writing fails, try using a temp file
                        temp_file = f"temp_score_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
                        combined_scores.to_excel(temp_file, index=False)
                        st.info(f"Your score was saved to '{temp_file}' instead.")
                        return True
                        
                except Exception as read_err:
                    # If reading existing file fails, create new file with just this record
                    new_record.to_excel(score_file, index=False)
                    return True
            else:
                # Score file doesn't exist, create it
                new_record.to_excel(score_file, index=False)
                return True
                
        except Exception as e:
            # Final fallback: save to temp file
            temp_file = f"temp_score_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
            new_record.to_excel(temp_file, index=False)
            st.info(f"Your score was saved to '{temp_file}' as a fallback.")
            return True
            
    except Exception as e:
        st.error(f"Error saving score: {str(e)}")
        return False

# Function to format time as minutes:seconds
def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes):02d}:{int(seconds):02d}"

# Add the missing get_time_remaining function
def get_time_remaining():
    if 'start_time' in st.session_state and st.session_state.start_time:
        elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
        remaining = (30 * 60) - elapsed  # 30 minutes in seconds
        return max(0, remaining)
    return 30 * 60  # Default to 30 minutes if no start_time is set

# Main function to run the Streamlit app
def main():
    # Set up session state for managing application state
    if 'page' not in st.session_state:
        st.session_state.page = 'intro'  # Start with intro page
    if 'asked_questions' not in st.session_state:
        st.session_state.asked_questions = []
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = None
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'roll_verified' not in st.session_state:
        st.session_state.roll_verified = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'time_remaining' not in st.session_state:
        st.session_state.time_remaining = 30 * 60  # 30 minutes in seconds
    if 'last_update_time' not in st.session_state:
        st.session_state.last_update_time = None

    TOTAL_QUESTIONS = 25

    # Introduction page - Get user details
    if st.session_state.page == 'intro':
        st.markdown('<h2 style="text-align:center; color:#1e88e5; margin-bottom:20px;">Physics Quiz Test</h2>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Student Information</div>', unsafe_allow_html=True)

        if not st.session_state.roll_verified:
            roll_num = st.text_input("Enter Roll Number (digits only):")
            std_name = st.text_input("Student Name (letters only):")
            f_name = st.text_input("Father's Name (letters only):")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Start Quiz"):
                    if not roll_num or not std_name or not f_name:
                        st.warning("Please fill in all fields to proceed.")
                    elif not is_valid_roll_number(roll_num):
                        st.error("Roll number must contain only digits.")
                    elif not is_valid_name(std_name):
                        st.error("Student name should contain only letters, spaces, and basic name characters.")
                    elif not is_valid_name(f_name):
                        st.error("Father's name should contain only letters, spaces, and basic name characters.")
                    elif check_student_attempt(roll_num):
                        st.error(f"Student with Roll Number {roll_num} has already taken this quiz. Each student can only take the quiz once.")
                    else:
                        st.session_state.roll_num = roll_num
                        st.session_state.std_name = std_name
                        st.session_state.f_name = f_name
                        st.session_state.roll_verified = True

                        # Try to load quiz data
                        quiz_data = load_quiz_data("physics_quiz.xlsx", "table (2)")
                        if quiz_data is not None and not quiz_data.empty:
                            st.session_state.quiz_data = quiz_data
                            st.session_state.asked_questions = []
                            st.session_state.score = 0
                            st.session_state.total_questions = 0
                            st.session_state.current_question = None
                            st.session_state.page = 'quiz'
                            st.session_state.start_time = datetime.now()
                            st.session_state.time_remaining = 30 * 60
                            st.session_state.last_update_time = datetime.now()
                            st.rerun()
                        else:
                            st.error("Failed to load quiz questions. Please check the Excel file.")

            # with col2:
            #     if st.button("Back to Subject Selection"):
            #         # Use Streamlit's switch_page for navigation
            #         st.switch_page("pages/subject_selection.py")
            #         st.rerun()

        else:
            st.success("Student information verified. Starting quiz...")
            st.session_state.page = 'quiz'
            st.rerun()

    # Quiz page - Display questions one by one
    elif st.session_state.page == 'quiz':
        st.markdown('<h2 style="text-align:center; color:#1e88e5; margin-bottom:20px;">Physics Quiz Test</h2>', unsafe_allow_html=True)
        # Show student info in a single centered line
        st.markdown(f"""
        <div class="info-container-inline">
            <span><span class="info-label">Roll Number:</span> {st.session_state.roll_num}</span>
            <span><span class="info-label">Student Name:</span> {st.session_state.std_name}</span>
            <span><span class="info-label">Father's Name:</span> {st.session_state.f_name}</span>
        </div>
        """, unsafe_allow_html=True)
        # Timer display
        time_remaining = get_time_remaining()
        st.markdown(f"""
        <div class="timer-container">
            Time Remaining: {format_time(time_remaining)}
        </div>
        """, unsafe_allow_html=True)
        # End quiz if time is up
        if time_remaining <= 0:
            st.session_state.page = 'results'
            st.rerun()

        quiz_data = st.session_state.quiz_data
        
        # If quiz data loaded successfully
        if quiz_data is not None and not quiz_data.empty:
            # Get available questions (exclude already asked ones)
            available_questions = quiz_data.index.tolist()
            for q in st.session_state.asked_questions:
                if q in available_questions:
                    available_questions.remove(q)
            
            # If all questions asked or reached max questions, go to results page
            if not available_questions or st.session_state.total_questions >= TOTAL_QUESTIONS:
                st.session_state.page = 'results'
                st.rerun()
                
            # Select a random question from available questions
            if st.session_state.current_question is None:
                question_idx = random.choice(available_questions)
                st.session_state.current_question = question_idx
            else:
                question_idx = st.session_state.current_question
                
            # Display question number with styling (like the image)
            st.markdown(f"""
            <div style="display: inline-block; background-color: #1e88e5; color: white; font-weight: bold; font-size: 1.2rem; padding: 5px 10px; border-radius: 5px; margin-bottom: 10px;">
                Question {st.session_state.total_questions + 1} of {TOTAL_QUESTIONS}
            </div>
            """, unsafe_allow_html=True)
            
            # Get the question row
            row = quiz_data.iloc[question_idx]
            
            # Find the question column and value
            question_text = None
            
            # Check if there's a column named "question" or similar
            for col in quiz_data.columns:
                if col.lower() == 'question':
                    question_text = row[col]
                    break
            
            # If no "question" column found, use the first column that's not an ID
            if question_text is None:
                # Use the first column that contains text content
                for col in quiz_data.columns:
                    if pd.notna(row[col]) and isinstance(row[col], str) and len(row[col]) > 0:
                        question_text = row[col]
                        break
            
            # If still no question found, use the first column value
            if question_text is None:
                question_text = row.iloc[0]
                
            # Display the question with styling (bold and larger font size)
            if pd.notna(question_text):
                st.markdown(f"""
                <div class='info-container' style="font-size: 1.3rem; margin-top: 10px;">
                    <strong>{question_text}</strong>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"Could not find question text for question #{question_idx+1}")
            
            # Collect options - look through all columns except those that might contain answers
            options = []
            skip_cols = ['question', 'answer', 'correct', 'correct_answer', 'explanation', 'notes']
            
            for i, col in enumerate(quiz_data.columns):
                # Skip the question column and any obvious answer columns
                if (col.lower() not in skip_cols and 
                    'answer' not in col.lower() and 
                    'correct' not in col.lower() and 
                    i > 0):  # Skip first column (question)
                    
                    value = row[col]
                    if pd.notna(value) and value != '' and (isinstance(value, str) or isinstance(value, int) or isinstance(value, float)):
                        options.append(value)
                        
                    # Limit to 4 options
                    if len(options) >= 4:
                        break
            
            # Find answer column
            answer = None
            for col in quiz_data.columns:
                col_lower = col.lower()
                if (col_lower == 'answer' or col_lower == 'correct' or 
                    col_lower == 'correct_answer' or 'correct' in col_lower):
                    answer = row[col]
                    break
            
            # Display options - set index to None to avoid preselection
            if options:
                selected_option = st.radio("Choose an option:", options, key=f"q_{question_idx}", index=None)
                
                # Only one column for Submit Answer (remove Skip Question)
                col1, _ = st.columns(2)
                with col1:
                    submit_disabled = selected_option is None
                    if st.button("Submit Answer", disabled=submit_disabled):
                        st.session_state.asked_questions.append(question_idx)
                        st.session_state.total_questions += 1
                        
                        if pd.notna(answer):
                            # Check if correct answer is given as a letter (A, B, C, D) or full text
                            if isinstance(answer, str) and len(answer) == 1 and answer.upper() in ['A', 'B', 'C', 'D']:
                                # Convert letter to index (A=0, B=1, etc.)
                                answer_idx = ord(answer.upper()) - ord('A')
                                if 0 <= answer_idx < len(options):
                                    correct_answer = options[answer_idx]
                                else:
                                    correct_answer = answer
                            else:
                                correct_answer = answer
                                
                            # Show the answer result
                            if selected_option == correct_answer:
                                st.success("Correct!")
                                st.session_state.score += 1
                            else:
                                st.error(f"Wrong! The correct answer is: {correct_answer}")
                        else:
                            st.warning("Could not determine the correct answer from the data.")
                        
                        # Reset current question to select a new one
                        st.session_state.current_question = None
                        
                        # If we've asked enough questions, go to results
                        if st.session_state.total_questions >= TOTAL_QUESTIONS:
                            st.session_state.page = 'results'
                            
                        st.rerun()
            else:
                st.warning("No options found for this question. Skipping...")
                st.session_state.asked_questions.append(question_idx)
                st.session_state.current_question = None
                st.rerun()
        else:
            st.error("Failed to load quiz data. Please check the Excel file.")
            if st.button("Return to Start"):
                st.session_state.page = 'intro'
                st.rerun()
                
    # Results page - Show score and save data
    elif st.session_state.page == 'results':
        st.markdown('<div class="section-header">Quiz Results</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-container">
            <p><strong>Student Name:</strong> {st.session_state.std_name}</p>
            <p><strong>Father's Name:</strong> {st.session_state.f_name}</p>
            <p><strong>Roll Number:</strong> {st.session_state.roll_num}</p>
            <p><strong>Questions Attempted:</strong> {st.session_state.total_questions} out of {TOTAL_QUESTIONS}</p>
            <p><strong>Your Score:</strong> {st.session_state.score} out of {TOTAL_QUESTIONS}</p>
        """, unsafe_allow_html=True)
        
        # Calculate percentage based on total questions (25), not just attempted questions
        percentage = (st.session_state.score / TOTAL_QUESTIONS) * 100
        
        # Add percentage and feedback message based on score
        message = ""
        if percentage >= 80:
            message = '<p style="color: green; font-weight: bold;">Excellent! You did great!</p>'
        elif percentage >= 60:
            message = '<p style="color: green;">Good job!</p>'
        elif percentage >= 40:
            message = '<p style="color: orange;">You can do better!</p>'
        else:
            message = '<p style="color: red;">You need more practice.</p>'
            
        st.markdown(f"""
            <p><strong>Percentage:</strong> {percentage:.2f}%</p>
            {message}
        </div>
        """, unsafe_allow_html=True)
        
        # Save score to physics_score.xlsx
        save_status = save_score(
            st.session_state.std_name, 
            st.session_state.f_name,
            st.session_state.roll_num,
            st.session_state.total_questions, 
            st.session_state.score
        )
        
        if save_status:
            st.success("Your score has been saved successfully!")
            st.info("May Allah grant you success in this life and the next. آمين")
        
        # Next student button
        if st.button("Next Student (Start New Quiz)"):
            # Reset session state for next student and reload intro page
            st.session_state.page = 'intro'
            st.session_state.asked_questions = []
            st.session_state.score = 0
            st.session_state.total_questions = 0
            st.session_state.current_question = None
            st.session_state.quiz_data = None
            st.session_state.roll_verified = False
            st.session_state.start_time = None
            st.session_state.time_remaining = 30 * 60
            st.session_state.last_update_time = None
            st.rerun()
    
    # Footer at the very end (no login link)
    st.markdown("""
    <style>
        .footer-text {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 14px;
            color: #666;
            background: #fff;
            padding: 10px 0;
            box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
            z-index: 999;
        }
    </style>
    <div class="footer-text">
        Quiz powered by @mastersahub
    </div>
    """, unsafe_allow_html=True)

    # Collapse the sidebar for this page
    st.sidebar.empty()

if __name__ == "__main__":
    main()
