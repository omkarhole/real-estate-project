import streamlit as st


def apply_app_style():
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        [data-testid="stSidebar"] {
            background: #20212b;
        }
        [data-testid="stSidebar"] * {
            color: #e9edf5;
        }
        .block-container {
            max-width: 1120px;
            padding-top: 2.4rem;
            padding-bottom: 2.5rem;
        }
        [data-testid="stSidebar"] [data-testid="stPageLink"] {
            margin: .2rem 0;
        }
        [data-testid="stSidebar"] [data-testid="stPageLink"] a {
            min-height: 2.45rem;
            padding: .35rem .55rem;
            border: 1px solid transparent;
            border-radius: 7px;
            color: #e9edf5;
        }
        [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
            background: #2b3040;
        }
        [data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"] {
            background: #3a4053;
            border-color: #4a5268;
            font-weight: 600;
        }
        .sidebar-credit {
            margin-top: 1.6rem;
            color: #aab5c5;
            font-size: .8rem;
            line-height: 1.8;
        }
        .sidebar-credit a {
            color: #aab5c5;
            text-decoration: none;
        }
        .sidebar-credit a:hover {
            color: #ffffff;
            text-decoration: underline;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("## 🏠 EstateIQ")
        st.caption("Gurgaon Real Estate Analytics")
        st.divider()
        st.page_link("Home.py", label="Home", icon="🏠")
        st.page_link("pages/1_Price Predictor.py", label="Price Predictor", icon="💰")
        st.page_link("pages/2_Analysis App.py", label="Analysis App", icon="📊")
        st.page_link(
            "pages/3_Recommend Appartments.py",
            label="Recommend Apartments",
            icon="✨",
        )
        st.markdown(
            """
            <div class="sidebar-credit">
                Created by <strong>Omkar Hole</strong><br>
                <a href="https://github.com/omkarhole/real-estate-project"
                   target="_blank">GitHub</a>
                &nbsp;·&nbsp;
                <a href="https://www.linkedin.com/in/omkar-hole-c0der"
                   target="_blank">LinkedIn</a>
            </div>
            """,
            unsafe_allow_html=True,
        )
