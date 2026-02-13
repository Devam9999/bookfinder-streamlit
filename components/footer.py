import streamlit as st

def render_footer():
    st.markdown("""
    <div class="footer">
        <div class="footer-container">
            <div class="footer-section">
                <h3>Book Finder</h3>
                <p>AI-Powered Book Recommendation<br>Platform for discovering your<br>next favorite read.</p>
            </div>
            <div class="footer-section">
                <h3>Contact Us</h3>
                <div class="contact-details">
                    <p>📍 DA-IICT Road, Gandhinagar 382007, Gujarat (India)</p>
                    <p>✉️ amncha195@gmail.com</p>
                    <p>✉️ gandhi.devam28@gmail.com</p>
                </div>
            </div>
            <div class="footer-section">
                <h3>Project Team</h3>
                <div class="contact-details">
                    <p><a href="https://www.linkedin.com/in/aman-chauhan2001/"> 👤 Chauhan Aman Satpal </a></p>
                    <p><a href="https://www.linkedin.com/in/devam-gandhi-8b70ba252"> 👤 Devam Gandhi</a></p>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            &copy; 2026 Book Finder — AI Recommendation Platform. All rights reserved.
        </div>
    </div>
    """, unsafe_allow_html=True)
