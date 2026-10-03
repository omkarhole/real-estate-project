# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import pickle
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
# import seaborn as sns

# st.set_page_config(page_title="Plotting Demo")

# st.title('Analytics')

# new_df = pd.read_csv('datasets/data_viz1.csv')
# feature_text = pickle.load(open('datasets/feature_text.pkl','rb'))


# group_df = new_df.groupby('sector').mean()[['price','price_per_sqft','built_up_area','latitude','longitude']]

# st.header('Sector Price per Sqft Geomap')
# fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
#                   color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
#                   mapbox_style="open-street-map",width=1200,height=700,hover_name=group_df.index)

# st.plotly_chart(fig,use_container_width=True)

# st.header('Features Wordcloud')

# wordcloud = WordCloud(width = 800, height = 800,
#                       background_color ='black',
#                       stopwords = set(['s']),  # Any stopwords you'd like to exclude
#                       min_font_size = 10).generate(feature_text)

# plt.figure(figsize = (8, 8), facecolor = None)
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.tight_layout(pad = 0)
# st.pyplot()

# st.header('Area Vs Price')

# property_type = st.selectbox('Select Property Type', ['flat','house'])

# if property_type == 'house':
#     fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")

#     st.plotly_chart(fig1, use_container_width=True)
# else:
#     fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x="built_up_area", y="price", color="bedRoom",
#                       title="Area Vs Price")

#     st.plotly_chart(fig1, use_container_width=True)

# st.header('BHK Pie Chart')

# sector_options = new_df['sector'].unique().tolist()
# sector_options.insert(0,'overall')

# selected_sector = st.selectbox('Select Sector', sector_options)

# if selected_sector == 'overall':

#     fig2 = px.pie(new_df, names='bedRoom')

#     st.plotly_chart(fig2, use_container_width=True)
# else:

#     fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom')

#     st.plotly_chart(fig2, use_container_width=True)

# st.header('Side by Side BHK price comparison')

# fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')

# st.plotly_chart(fig3, use_container_width=True)


# st.header('Side by Side Distplot for property type')

# fig3 = plt.figure(figsize=(10, 4))
# sns.distplot(new_df[new_df['property_type'] == 'house']['price'],label='house')
# sns.distplot(new_df[new_df['property_type'] == 'flat']['price'], label='flat')
# plt.legend()
# st.pyplot(fig3)

# optmized version of the above code

import pickle

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud


st.set_page_config(
    page_title="Real Estate Analysis",
    page_icon=":bar_chart:",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
        border: 1px solid #60a5fa;
        padding: 1rem;
        border-radius: 12px;
    }
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: #ffffff !important;
    }
    [data-testid="stMetricLabel"] p {
        color: #dbeafe !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Real Estate Market Analysis")
st.caption("Explore prices, inventory, property mix and location trends at a glance.")

new_df = pd.read_csv("datasets/data_viz1.csv")
with open("datasets/feature_text.pkl", "rb") as feature_file:
    feature_text = pickle.load(feature_file)

numeric_columns = [
    "price",
    "price_per_sqft",
    "built_up_area",
    "latitude",
    "longitude",
]
new_df[numeric_columns] = new_df[numeric_columns].apply(
    lambda column: pd.to_numeric(
        column.astype(str).str.replace(r"[^0-9.-]", "", regex=True),
        errors="coerce",
    )
)
new_df["bedRoom"] = pd.to_numeric(new_df["bedRoom"], errors="coerce")

# Centralized dashboard filters
sector_options = ["All Sectors"] + sorted(new_df["sector"].dropna().unique().tolist())
property_types = ["All Property Types"] + sorted(
    new_df["property_type"].dropna().unique().tolist()
)


def reset_filters():
    st.session_state.dashboard_sector = "All Sectors"
    st.session_state.dashboard_property_type = "All Property Types"


with st.sidebar:
    st.header("Dashboard Filters")
    st.caption("Use these filters to update the analysis charts.")
    selected_sector = st.selectbox(
        "Sector",
        sector_options,
        key="dashboard_sector",
    )
    selected_property_type = st.selectbox(
        "Property type",
        property_types,
        key="dashboard_property_type",
    )
    st.button(
        "Reset filters",
        width="stretch",
        on_click=reset_filters,
    )

filtered_data = new_df.copy()
if selected_sector != "All Sectors":
    filtered_data = filtered_data[filtered_data["sector"] == selected_sector]
if selected_property_type != "All Property Types":
    filtered_data = filtered_data[
        filtered_data["property_type"] == selected_property_type
    ]

if filtered_data.empty:
    st.warning("No listings match the selected filters. Please choose a broader filter.")
    st.stop()

# Summary cards
average_price = filtered_data["price"].mean()
average_price_per_sqft = filtered_data["price_per_sqft"].mean()
average_area = filtered_data["built_up_area"].mean()
total_listings = len(filtered_data)

metric_columns = st.columns(4)
metric_columns[0].metric(
    "Average Price",
    f"₹{average_price:.2f} Cr" if pd.notna(average_price) else "—",
)
metric_columns[1].metric("Total Listings", f"{total_listings:,}")
metric_columns[2].metric(
    "Average Price / Sqft",
    f"₹{average_price_per_sqft:,.0f}" if pd.notna(average_price_per_sqft) else "—",
)
metric_columns[3].metric(
    "Average Built-up Area",
    f"{average_area:,.0f} sqft" if pd.notna(average_area) else "—",
)

st.divider()

# Location overview
st.header("Location and Price Overview")
group_df = (
    new_df.groupby("sector", as_index=True)[numeric_columns]
    .mean()
    .reset_index()
)
map_df = group_df.dropna(subset=["latitude", "longitude"])
map_figure = px.scatter_mapbox(
    map_df,
    lat="latitude",
    lon="longitude",
    color="price_per_sqft",
    size="built_up_area",
    hover_name="sector",
    hover_data={"price_per_sqft": ":,.0f", "built_up_area": ":,.0f"},
    color_continuous_scale=[
        [0.0, "#16a34a"],
        [0.5, "#f59e0b"],
        [1.0, "#dc2626"],
    ],
    zoom=10,
    height=520,
    mapbox_style="open-street-map",
    title="Average price per sqft by sector",
)
map_figure.update_layout(
    margin={"l": 0, "r": 0, "t": 45, "b": 0},
)
st.plotly_chart(map_figure, width="stretch")

top_sectors = (
    new_df.groupby("sector", as_index=False)
    .agg(listings=("sector", "size"), average_price=("price", "mean"))
    .sort_values("listings", ascending=False)
    .head(12)
)
top_sectors["average_price"] = top_sectors["average_price"].round(2)
sector_figure = px.bar(
    top_sectors.sort_values("listings"),
    x="listings",
    y="sector",
    orientation="h",
    color="average_price",
    color_continuous_scale="Blues",
    labels={"listings": "Listings", "sector": "Sector", "average_price": "Avg price (Cr)"},
    title="Top sectors by number of listings",
)
sector_figure.update_layout(height=430, margin={"l": 0, "r": 0, "t": 45, "b": 0})

# Wordcloud and inventory chart
st.header("Features and Inventory Insights")
wordcloud_column, inventory_column = st.columns(2, gap="large")

with wordcloud_column:
    filtered_df = filtered_data
    feature_column = next(
        (
            column
            for column in filtered_df.columns
            if column.strip().lower() in ("feature", "features")
        ),
        None,
    )
    if feature_column is None:
        filtered_feature_text = str(feature_text)
    else:
        filtered_feature_text = " ".join(
            filtered_df[feature_column].dropna().astype(str)
        )
    if not filtered_feature_text.strip():
        filtered_feature_text = "No features available"

    wordcloud = WordCloud(
        width=900,
        height=500,
        background_color="white",
        colormap="Blues",
        stopwords={"s"},
        min_font_size=10,
    ).generate(filtered_feature_text)
    wordcloud_figure, wordcloud_axis = plt.subplots(figsize=(9, 5))
    wordcloud_axis.imshow(wordcloud, interpolation="bilinear")
    wordcloud_axis.axis("off")
    wordcloud_figure.tight_layout(pad=0)
    st.pyplot(wordcloud_figure, width="stretch")
    plt.close(wordcloud_figure)

with inventory_column:
    st.plotly_chart(sector_figure, width="stretch")

# Interactive comparisons
st.header("Price and Property Comparisons")
area_column, bhk_column = st.columns(2, gap="large")

with area_column:
    property_type = selected_property_type
    area_df = filtered_data
    area_figure = px.scatter(
        area_df,
        x="built_up_area",
        y="price",
        color="bedRoom",
        hover_data=["sector", "price_per_sqft"],
        labels={
            "built_up_area": "Built-up area (sqft)",
            "price": "Price (Cr)",
            "bedRoom": "Bedrooms",
        },
        title=(
            f"{property_type.title()} price vs built-up area"
            if property_type != "All Property Types"
            else "Price vs built-up area"
        ),
        color_continuous_scale="Viridis",
    )
    area_figure.update_layout(height=430, margin={"l": 0, "r": 0, "t": 45, "b": 0})
    st.plotly_chart(area_figure, width="stretch")

with bhk_column:
    bhk_counts = (
        filtered_data["bedRoom"]
        .dropna()
        .astype(int)
        .value_counts()
        .sort_index()
        .rename_axis("bedrooms")
        .reset_index(name="listings")
    )
    # Keep very small slices out of the donut so the labels remain readable.
    total_bhk_listings = bhk_counts["listings"].sum()
    small_slice_limit = max(1, total_bhk_listings * 0.02)
    small_slices = bhk_counts["listings"] < small_slice_limit
    if small_slices.any() and (~small_slices).any():
        other_listings = bhk_counts.loc[small_slices, "listings"].sum()
        bhk_counts = bhk_counts.loc[~small_slices].copy()
        bhk_counts = pd.concat(
            [
                bhk_counts,
                pd.DataFrame([{"bedrooms": "Other", "listings": other_listings}]),
            ],
            ignore_index=True,
        )

    bhk_figure = px.pie(
        bhk_counts,
        names="bedrooms",
        values="listings",
        hole=0.55,
        title=f"BHK distribution - {selected_sector}",
        labels={"bedrooms": "Bedrooms", "listings": "Listings"},
    )
    bhk_figure.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate="<b>%{label} bedrooms</b><br>Listings: %{value:,}<br>Share: %{percent}<extra></extra>",
        sort=False,
    )
    bhk_figure.update_layout(
        height=430,
        margin={"l": 0, "r": 0, "t": 55, "b": 0},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": -0.18,
            "xanchor": "center",
            "x": 0.5,
            "font": {"size": 11},
        },
    )
    st.plotly_chart(bhk_figure, width="stretch")

# Additional charts
chart_column, distribution_column = st.columns(2, gap="large")
with chart_column:
    box_df = filtered_data[filtered_data["bedRoom"].between(1, 4)].dropna(
        subset=["bedRoom", "price"]
    )
    price_figure = px.box(
        box_df,
        x="bedRoom",
        y="price",
        color="property_type",
        points=False,
        labels={"bedRoom": "Bedrooms", "price": "Price (Cr)"},
        title="Price range by bedroom count",
    )
    price_figure.update_layout(height=430, margin={"l": 0, "r": 0, "t": 45, "b": 0})
    st.plotly_chart(price_figure, width="stretch")

with distribution_column:
    property_mix = (
        filtered_data["property_type"].value_counts()
        .rename_axis("property_type")
        .reset_index(name="listings")
    )
    mix_figure = px.bar(
        property_mix,
        x="property_type",
        y="listings",
        color="property_type",
        labels={"property_type": "Property type", "listings": "Listings"},
        title="Inventory by property type",
        text_auto=True,
    )
    mix_figure.update_layout(
        height=430,
        showlegend=False,
        margin={"l": 0, "r": 0, "t": 45, "b": 0},
    )
    st.plotly_chart(mix_figure, width="stretch")
