import pandas as pd
import streamlit as st

from app_style import apply_app_style


st.set_page_config(
    page_title="Gurgaon Real Estate Analytics",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_summary():
    data = pd.read_csv("datasets/data_viz1.csv")
    data["price"] = pd.to_numeric(
        data["price"].astype(str).str.replace(r"[^0-9.-]", "", regex=True),
        errors="coerce",
    )
    return {
        "listings": len(data),
        "sectors": data["sector"].nunique(),
        "average_price": data["price"].mean(),
    }


summary = load_summary()
apply_app_style()

st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    .block-container {
        max-width: 1120px;
        padding-top: 2.4rem;
        padding-bottom: 2.5rem;
    }
    .home-intro {
        margin-bottom: 1.8rem;
    }
    .home-intro p {
        color: #9aa6b7;
        font-size: 1.05rem;
        margin-top: -.6rem;
    }
    [data-testid="stMetric"] {
        min-height: 112px;
        padding: 1rem 1.15rem;
        border: 1px solid #303846;
        border-radius: 12px;
        background: #171c24;
    }
    [data-testid="stMetricLabel"] {
        color: #aab5c5;
    }
    [data-testid="stMetricValue"] {
        color: #f4f7fb;
    }
    .section-heading {
        margin: 2.8rem 0 1rem;
        line-height: 1.2;
    }
    .about-copy {
        margin-bottom: 2.6rem;
    }
    .split-heading {
        margin: 0 0 .8rem;
        line-height: 1.2;
    }
    .info-card {
        max-width: 820px;
        color: #aab5c5;
        line-height: 1.55;
    }
    .feature-card {
        min-height: 172px;
        padding: 1.2rem;
        border: 1px solid #303846;
        border-radius: 12px;
        background: #171c24;
    }
    .feature-card .icon {
        font-size: 1.45rem;
    }
    .feature-card h3 {
        margin: .55rem 0 .35rem;
        font-size: 1.05rem;
    }
    .feature-card p {
        color: #9aa6b7;
        font-size: .9rem;
        line-height: 1.45;
        margin: 0;
    }
    .profile-card {
        padding: 1rem 1.2rem;
        border-left: 3px solid #2f73e8;
        border-radius: 6px;
        background: #171c24;
    }
    .profile-card p {
        color: #aab5c5;
        margin: .2rem 0 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="home-intro">
        <h1>Gurgaon Real Estate Analytics</h1>
        <p>Understand the market. Estimate prices. Find your next apartment.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_columns = st.columns(3)
metric_columns[0].metric("Property listings", f"{summary['listings']:,}")
metric_columns[1].metric("Sectors covered", f"{summary['sectors']:,}")
metric_columns[2].metric(
    "Average listed price",
    f"₹{summary['average_price']:.2f} Cr",
)

st.markdown('<h2 class="section-heading">Features</h2>', unsafe_allow_html=True)
features = [
    (
        "💰",
        "Price Predictor",
        "Estimate a property price using location, area, rooms, furnishing, and amenities.",
    ),
    (
        "📊",
        "Market Analysis",
        "Explore sector prices, listing trends, property mix, and location insights.",
    ),
    (
        "✨",
        "Apartment Recommendations",
        "Search by radius and discover apartments similar to your selected property.",
    ),
]

feature_columns = st.columns(3)
for column, (icon, title, description) in zip(feature_columns, features):
    with column:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="icon">{icon}</div>
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<h2 class="section-heading">About the project</h2>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="about-copy">
        EstateIQ combines a saved machine-learning pipeline, Gurgaon property
        data, interactive analysis, and similarity-based recommendations in one
        workspace. Use the results for research and shortlisting.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <h2 class="section-heading">Dataset</h2>
    <div class="info-card">
        The Gurgaon property dataset brings together listings across
        <strong>100+ sectors</strong>, with details such as property type, BHK,
        bathrooms, built-up area, furnishing, location, pricing, and other
        useful property characteristics.
    </div>

    <h2 class="section-heading">Technologies</h2>
    <div class="info-card">
        <code>Python</code> · <code>Streamlit</code> · <code>Pandas</code> ·
        <code>Scikit-learn</code> · <code>XGBoost</code> · <code>Plotly</code>
        <br>
        Built for practical analysis, machine-learning predictions, and
        interactive property discovery.
    </div>
    """,
    unsafe_allow_html=True,
)
