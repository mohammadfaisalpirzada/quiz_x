import streamlit as st

def show_header(title="PEACE INTERNATIONAL SCHOOL", logo_url="https://pies.pk/wp-content/uploads/2023/10/peace-logo-min.png"):
    """
    Display a custom header at the top of the page.
    
    Parameters:
    - title: The title text to display in the header
    - logo_url: URL of the logo image
    """
    st.markdown("""
        <style>
            /* Header styling */
            .custom-header-outer {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                z-index: 999999;
                background: #e6f2ff;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }
            
            .custom-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 12px 16px;
                border-radius: 0 0 12px 12px;
                max-width: 1200px;
                margin: 0 auto;
                position: relative;
            }
            
            /* Logo styling */
            .header-logo {
                height: 64px;
                margin-right: 18px;
                transition: height 0.2s;
            }
            
            .header-left {
                display: flex;
                align-items: center;
                gap: 12px;
                flex: 0 0 auto;
            }
            
            /* Title styling */
            .header-center {
                font-size: 26px;
                color: #004080;
                font-weight: bold;
                text-align: center;
                font-family: 'Times New Roman', Times, serif;
                flex: 1 1 auto;
                text-transform: uppercase;
                letter-spacing: 2px;
                margin: 0 10px;
                min-width: 0;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            
            /* Button styling */
            .header-right {
                font-size: 18px;
                color: #004080;
                font-weight: 600;
                padding: 6px 12px;
                min-width: 60px;
                text-align: center;
                background: none;
                border: 2px solid #004080;
                border-radius: 6px;
                cursor: pointer;
                transition: background-color 0.2s, color 0.2s;
            }
            
            .header-right:hover {
                background-color: #004080;
                color: white;
            }
            
            /* Responsive styles */
            @media (max-width: 700px) {
                .custom-header {
                    flex-direction: row;
                    align-items: center;
                    justify-content: space-between;
                    gap: 0;
                    padding: 10px 4vw;
                    min-width: 100vw;
                    position: relative;
                }
                
                .header-left {
                    flex: 0 0 auto;
                    margin-bottom: 0;
                    width: auto;
                    justify-content: flex-start;
                }
                
                .header-logo {
                    height: 54px;
                    margin-right: 10px;
                }
                
                .header-center {
                    font-size: 22px;
                    margin: 0;
                    white-space: nowrap;
                    letter-spacing: 1.5px;
                    justify-content: center;
                    width: 100%;
                    flex: 1 1 auto;
                }
                
                .desktop-title { display: none !important; }
                .mobile-title { display: inline !important; text-align: center; width: 100%; }
                
                .header-right {
                    font-size: 17px;
                    min-width: 60px;
                    text-align: right;
                    margin-left: 10px;
                }
            }
            
            @media (min-width: 701px) {
                .mobile-title { display: none !important; }
                .desktop-title { display: inline !important; }
                .custom-header {
                    flex-direction: row;
                    align-items: center;
                    justify-content: center;
                }
                .header-left {
                    justify-content: flex-start;
                    margin-bottom: 0;
                    width: auto;
                }
                .header-center {
                    justify-content: center;
                    width: 100%;
                }
            }
            
            @media (max-width: 768px) {
                .custom-header {
                    padding: 10px 12px;
                }
                .header-logo {
                    height: 40px;
                }
                .header-center {
                    font-size: 18px;
                    padding: 0 10px;
                }
            }
            
            /* Adjust main app content to make room for fixed header */
            .stApp {
                padding-top: 70px !important;
                overflow-x: hidden;
            }
        </style>
        
        <div class="custom-header-outer">
            <div class="custom-header">
                <div class="header-left">
                    <img class="header-logo" src="https://pies.pk/wp-content/uploads/2023/10/peace-logo-min.png" alt="Logo">
                </div>
                <div class="header-center">
                    <span class="desktop-title">PEACE INTERNATIONAL SCHOOL</span>
                    <span class="mobile-title">PEACE<br>INTERNATIONAL<br>SCHOOL</span>                </div>
                <button class="header-right" onclick="window.location.href='/main_page';">FIRST QUIZ TEST 2025</button>
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_footer(text="Quiz powered by @mastersahub"):
    """
    Display a custom footer at the bottom of the page.
    
    Parameters:
    - text: Footer text content
    """
    st.markdown(f"""
    <style>
        /* Footer styling */
        .footer-container {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: #fff;
            box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
            z-index: 999;
        }}
        
        .footer-content {{
            padding: 10px 0;
            text-align: center;
        }}
        
        .footer-text {{
            font-size: 14px;
            color: #666;
        }}
        
        /* Add padding to main content to prevent footer overlap */
        .main-content {{
            padding-bottom: 50px;
        }}
    </style>
    
    <div class="footer-container">
        <div class="footer-content">
            <div class="footer-text">{text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Example usage
def main():
    # Show header
    show_header()
    
    # Main content area with some padding at the bottom to prevent footer overlap
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    st.title("Welcome to Peace International School")
    st.write("This is the main content of your application.")
    
    # Create simple tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Home", "About", "Quiz"])
    
    with tab1:
        st.header("Home")
        st.write("Welcome to our school's online platform.")
        
    with tab2:
        st.header("About")
        st.write("Learn more about Peace International School.")
        
    with tab3:
        st.header("Quiz Section")
        st.write("Start your quiz here")
        st.button("Begin Quiz")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show footer
    show_footer()

if __name__ == "__main__":
    main()