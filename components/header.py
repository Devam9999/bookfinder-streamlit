import streamlit as st

def render_header(set_page_callback):
    # Use a container with a custom class for the bottom border
    with st.container():
        
        # Split: 25% Brand, 75% Nav (to push nav right)
        # Using a gap to ensure separation
        col_brand, col_spacer, col_nav = st.columns([2, 2, 4])
        
        with col_brand:
            st.markdown("""
            <div class="brand-section">
                <div class="brand-text">Book Finder</div>
                <div class="brand-subtitle">AI Recommendation Platform</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_nav:
            # Align buttons to the right using columns
            # We need 4 buttons: Home, How It Works, Data Insights, About
            # Spacing: Adjusted ratios to prevent wrapping for longer texts
            n1, n2, n3, n4 = st.columns([1, 1.5, 1.5, 1.2])
            
            with n1:
                if st.button("Home", key="nav_home"): set_page_callback("Home")
            with n2:
                if st.button("How It Works", key="nav_how"): set_page_callback("How It Works")
            with n3:
                if st.button("Data Insights", key="nav_data"): set_page_callback("Data Insights")
            with n4:
                # "About" button - styled via JS below
                if st.button("About", key="nav_about"): set_page_callback("About")
        
        st.markdown('</div>', unsafe_allow_html=True)

        # JavaScript to style the 'About' button specifically and ensure alignment
        st.markdown("""
        <script>
        const styleAboutButton = () => {
            // Try both scopes to be safe
            let buttons = document.querySelectorAll('button');
            if (buttons.length === 0) {
                buttons = window.parent.document.querySelectorAll('button');
            }
            
            for (const button of buttons) {
                if (button.innerText.includes("About")) {
                    button.style.border = "1px solid #238636";
                    button.style.color = "#2ea043";
                    button.style.borderRadius = "6px";
                    button.style.padding = "0.4rem 1.2rem";
                    // Alignment Fixes: Apply same margin as CSS rule for headers
                    button.style.marginTop = "-16px"; 
                    button.style.transform = "translateY(-2px)";
                    
                    button.addEventListener('mouseover', () => {
                        button.style.backgroundColor = "rgba(46, 160, 67, 0.1)";
                        button.style.color = "#f0f6fc";
                    });
                    button.addEventListener('mouseout', () => {
                        button.style.backgroundColor = "transparent";
                        button.style.color = "#2ea043";
                    });
                }
            }
        };
        // Aggressive polling to catch Streamlit's dynamic re-renders
        styleAboutButton();
        setTimeout(styleAboutButton, 100);
        setTimeout(styleAboutButton, 500);
        setInterval(styleAboutButton, 1000);
        </script>
        """, unsafe_allow_html=True)

    # Dynamic styling for active state
    active_color = "#f0f6fc"
    inactive_color = "#8b949e"
    
    current_page = st.session_state.page
    
    # CSS to highlight specific buttons based on page state
    # We target the button text color based on the session state
    st.markdown(f"""
    <style>
        /* Home Active */
        div[data-testid="stHorizontalBlock"] button {{
            color: {inactive_color};
        }}
        
        /* Specific Active Overrides */
        /* Note: Streamlit doesn't give predictable classes for specific buttons, 
           so we rely on the order or title if available. 
           Instead, we use a simpler 'all inactive' approach above and let hover handle it.
        */
    </style>
    """, unsafe_allow_html=True)
