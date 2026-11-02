# import streamlit as st
# import numpy as np 
# import pandas as pd
# import pickle
# import shap
# import matplotlib.pyplot as plt
# from pathlib import Path

# from app_style import apply_app_style


# # page config 

# st.set_page_config(
#     page_title="Model Insights",
#     page_icon="📊",
#     layout="wide"
# )

# apply_app_style()


# st.title("🧠 Explainable AI | SHAP Model Insights")

# st.write(
#     "Understand how different property features affect "
#     "the predicted price of a Gurgaon property."
# )


# # load saved model and dataset


# ROOT_DIR = Path(__file__).resolve().parent.parent

# @st.cache_resource
# def load_model():
#     with open(ROOT_DIR / "pipeline.pkl", "rb") as file:
#         return pickle.load(file)

# @st.cache_data
# def load_data():
#     with open(ROOT_DIR / "df.pkl", "rb") as file:
#         return pickle.load(file)


# model = load_model()
# df= load_data()



# preprocessor = model.named_steps["preprocessor"]
# regressor = model.named_steps["regressor"]


# # perpare transformed features 
# def make_dense(data):
#     if hasattr(data, "toarray"):
#         return data.toarray()
#     return np.asarray(data)

# @st.cache_data
# def get_feature_names():
#     try:
#         return preprocessor.get_feature_names_out().tolist()
#     except Exception:
#         return [
#             f"Feature {i}"
#             for i in range(
#                 make_dense(preprocessor.transform(df.iloc[:1])).shape[1]
#             )
#         ]

# feature_names = get_feature_names()



# # -----------------------------
# # Create SHAP explainer
# # -----------------------------

# @st.cache_resource
# def load_explainer():
#     return shap.TreeExplainer(regressor)


# explainer=load_explainer()

# # global Feature Importance 

# st.header("1. Overall Feature Importance")

# st.write(
#     "This chart shows which features have the biggest impact "
#     "on the model's predictions across multiple properties."
# )


# sample_size=min(300,len(df))


# X_sample = df.sample(
#     n=sample_size,
#     random_state=42
# )

# X_sample_transformed = make_dense(
#     preprocessor.transform(X_sample)
# )

# shap_global=explainer(X_sample_transformed)


# shap_global_explanation = shap.Explanation(
#     values=shap_global.values,
#     base_values=shap_global.base_values,
#     data=X_sample_transformed,
#     feature_names=feature_names
# )


# fig, ax = plt.subplots(figsize=(10, 6))

# shap.plots.bar(
#     shap_global_explanation,
#     max_display=15,
#     show=False,
# )

# st.pyplot(plt.gcf(),clear_figure=True)


# # -----------------------------
# # Individual Property Explanation
# # -----------------------------
# st.header("2. Individual Property Price Explanation")

# st.write(
#     "Select a property from your dataset to understand "
#     "why the model predicts its price."
# )


# Selected_index=st.slider('Select Property row',min_value=0,max_value=len(df)-1,value=0)

# selected_property=df.iloc[[Selected_index]]

# # Display selected property details
# st.subheader("Property Details")

# st.dataframe(
#     selected_property,
#     use_container_width=True
# )

# predicted_price=model.predict(selected_property)[0]

# st.metric(
#     label="Predicted Property Price",
#     value=f"₹{predicted_price:.2f} Cr"
# )


# # transform the selected property for SHAP analysis
# X_selected_transformed=make_dense(
#     preprocessor.transform(selected_property)
# )

# # calculate SHAP values for the selected property
# shape_single=explainer(X_selected_transformed)

# shape_single_explaination = shap.Explanation(
#     values=shape_single.values,
#     base_values=shape_single.base_values,
#     data=X_selected_transformed,
#     feature_names=feature_names
# )


# # -----------------------------
# # Waterfall Plot
# # -----------------------------
# st.subheader("SHAP Waterfall Plot")

# st.write(
#     "The waterfall plot shows how each feature moves "
#     "the prediction away from the model's base value."
# )

# shap.plots.waterfall(
#     shape_single_explaination[0],
#     max_display=15,
#     show=False
# )

# st.pyplot(plt.gcf(),clear_figure=True)




import streamlit as st
import numpy as np 
import pandas as pd
import pickle
import shap
import matplotlib.pyplot as plt
from pathlib import Path

from app_style import apply_app_style


# page config 

st.set_page_config(
    page_title="Model Insights",
    page_icon="📊",
    layout="wide"
)

apply_app_style()

st.markdown(
    """
    <style>
    .insights-hero {
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #303846;
        border-radius: 14px;
        background: linear-gradient(135deg, #1d2430 0%, #171c24 100%);
    }
    .insights-eyebrow {
        margin: 0 0 .45rem;
        color: #8ea7ff;
        font-size: .76rem;
        font-weight: 700;
        letter-spacing: .12em;
        text-transform: uppercase;
    }
    .insights-hero h1 {
        margin: 0;
        font-size: clamp(1.7rem, 3vw, 2.45rem);
        line-height: 1.1;
    }
    .insights-hero p {
        max-width: 720px;
        margin: .7rem 0 0;
        color: #aab5c5;
        font-size: 1rem;
    }
    .section-label {
        margin: 1.8rem 0 .2rem;
        color: #8ea7ff;
        font-size: .76rem;
        font-weight: 700;
        letter-spacing: .1em;
        text-transform: uppercase;
    }
    .section-copy {
        margin: 0 0 1rem;
        color: #aab5c5;
    }
    [data-testid="stMetric"] {
        min-height: 108px;
        padding: 1rem 1.1rem;
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
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <section class="insights-hero">
        <p class="insights-eyebrow">Explainable AI  | SHAP </p>
        <h1>🧠 Understand every prediction</h1>
        <p>Explore the features that influence price across the market, then inspect
        the reasoning behind an individual property prediction.</p>
    </section>
    """,
    unsafe_allow_html=True,
)


# load saved model and dataset


ROOT_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT_DIR / "pipeline.pkl"
DATA_PATH = ROOT_DIR / "df.pkl"
MODEL_CACHE_KEY = MODEL_PATH.stat().st_mtime_ns
DATA_CACHE_KEY = DATA_PATH.stat().st_mtime_ns

@st.cache_resource
def load_model(cache_key):
    with MODEL_PATH.open("rb") as file:
        return pickle.load(file)

@st.cache_resource
def load_data(cache_key):
    with DATA_PATH.open("rb") as file:
        return pickle.load(file)


model = load_model(MODEL_CACHE_KEY)
df = load_data(DATA_CACHE_KEY)



preprocessor = model.named_steps["preprocessor"]
regressor = model.named_steps["regressor"]


# perpare transformed features 
def make_dense(data):
    if hasattr(data, "toarray"):
        return data.toarray()
    return np.asarray(data)

@st.cache_data
def get_feature_names(model_cache_key, _preprocessor, _df):
    try:
        return _preprocessor.get_feature_names_out().tolist()
    except Exception:
        return [
            f"Feature {i}"
            for i in range(
                make_dense(_preprocessor.transform(_df.iloc[:1])).shape[1]
            )
        ]

feature_names = get_feature_names(MODEL_CACHE_KEY, preprocessor, df)



# -----------------------------
# Create SHAP explainer
# -----------------------------

@st.cache_resource
def load_explainer(model_cache_key, _regressor):
    return shap.TreeExplainer(_regressor)


explainer = load_explainer(MODEL_CACHE_KEY, regressor)


@st.cache_data
def prepare_global_sample(data_cache_key, _df, _preprocessor):
    sample_size = min(300, len(_df))
    sample = _df.sample(n=sample_size, random_state=42)
    return make_dense(_preprocessor.transform(sample))


@st.cache_data
def calculate_shap_values(model_cache_key, _explainer, transformed_data):
    values = _explainer(transformed_data)
    return np.asarray(values.values), np.asarray(values.base_values)

X_sample_transformed = prepare_global_sample(
    DATA_CACHE_KEY,
    df,
    preprocessor,
)
global_values, global_base_values = calculate_shap_values(
    MODEL_CACHE_KEY,
    explainer,
    X_sample_transformed,
)


shap_global_explanation = shap.Explanation(
    values=global_values,
    base_values=global_base_values,
    data=X_sample_transformed,
    feature_names=feature_names
)


# global Feature Importance

st.markdown('<p class="section-label">Market-level explanation</p>', unsafe_allow_html=True)
st.subheader("What drives property prices?")
st.markdown(
    '<p class="section-copy">Average absolute SHAP impact across a representative sample of '
    f'{len(X_sample_transformed):,} properties.</p>',
    unsafe_allow_html=True,
)

summary_col, chart_col = st.columns([1, 2.35], gap="large")
with summary_col:
    st.metric("Properties sampled", f"{len(X_sample_transformed):,}")
    st.metric("Model features", f"{len(feature_names):,}")
    st.info(
        "Longer bars indicate features with a stronger average influence on predicted price. "
        "The direction of an individual effect is shown below.",
        icon="💡",
    )

with chart_col:
    with st.container(border=True):
        fig, ax = plt.subplots(figsize=(10, 6))
        shap.plots.bar(
            shap_global_explanation,
            max_display=15,
            show=False,
        )
        st.pyplot(fig, clear_figure=True, use_container_width=True)
        plt.close(fig)


# Individual Property Explanation
st.markdown('<p class="section-label">Property-level explanation</p>', unsafe_allow_html=True)
st.subheader("Why is this property priced this way?")
st.markdown(
    '<p class="section-copy">Choose a listing to see its profile, predicted value, and the '
    'features pushing the prediction up or down.</p>',
    unsafe_allow_html=True,
)

selected_index = st.slider(
    "Select a property",
    min_value=0,
    max_value=len(df) - 1,
    value=0,
    format="Property #%d",
)

selected_property = df.iloc[[selected_index]]
predicted_price = model.predict(selected_property)[0]

X_selected_transformed = make_dense(
    preprocessor.transform(selected_property)
)
single_values, single_base_values = calculate_shap_values(
    MODEL_CACHE_KEY,
    explainer,
    X_selected_transformed,
)
baseline_price = float(np.asarray(single_base_values).reshape(-1)[0])

metric_col, baseline_col = st.columns(2)
with metric_col:
    st.metric(
        label="Predicted property price",
        value=f"₹{predicted_price:.2f} Cr",
        delta=f"{predicted_price - baseline_price:+.2f} Cr vs model baseline",
    )
with baseline_col:
    st.metric("Model baseline", f"₹{baseline_price:.2f} Cr")

profile_col, waterfall_col = st.columns([1, 1.55], gap="large")
with profile_col:
    st.markdown("#### Property profile")
    profile = selected_property.T.rename(columns={selected_property.index[0]: "Value"})
    with st.container(border=True):
        st.dataframe(
            profile,
            use_container_width=True,
            height=260,
            hide_index=False,
        )


single_explanation = shap.Explanation(
    values=single_values,
    base_values=single_base_values,
    data=X_selected_transformed,
    feature_names=feature_names
)


# Waterfall Plot
with waterfall_col:
    st.markdown("#### What changed the prediction?")
    st.caption("Features extending right increase the prediction; features extending left decrease it.")
    with st.container(border=True):
        shap.plots.waterfall(
            single_explanation[0],
            max_display=15,
            show=False,
        )
        waterfall_fig = plt.gcf()
        st.pyplot(waterfall_fig, clear_figure=True, use_container_width=True)
        plt.close(waterfall_fig)

